import random
import subprocess
import time
import traceback

from django.conf import settings
from django.db import transaction

import celery

import autograder.core.models as ag_models
from autograder.security.autograder_sandbox import AutograderSandbox


@celery.shared_task
def grade_submission(submission_id):
    try:
        submission = _mark_as_being_graded(submission_id)
        _run_non_deferred_tests(submission)

        project = submission.submission_group.project
        deferred_queryset = project.autograder_test_cases.filter(deferred=True)
        signatures = (grade_ag_test.s(ag_test.pk, submission_id)
                      for ag_test in deferred_queryset)
        callback = _mark_as_finished.s(submission_id)
        celery.chord(signatures)(callback)
    except Exception:
        traceback.print_exc()
        with transaction.atomic():
            submission = ag_models.Submission.objects.select_for_update().get(
                pk=submission_id)
            submission.status = ag_models.Submission.GradingStatus.error
            submission.save()
        raise


def _mark_as_being_graded(submission_id):
    with transaction.atomic():
        submission = ag_models.Submission.objects.select_for_update().get(
            pk=submission_id)
        if (submission.status ==
                ag_models.Submission.GradingStatus.removed_from_queue):
            print('submission {} has been removed '
                  'from the queue'.format(submission.pk))
            return
        submission.status = ag_models.Submission.GradingStatus.being_graded
        submission.save()
        return submission


def _run_non_deferred_tests(submission):
        project = submission.submission_group.project
        for ag_test in project.autograder_test_cases.filter(deferred=False):
            print('running test: {}'.format(ag_test.pk))
            num_retries = 0
            while True:
                try:
                    grade_ag_test_impl(ag_test, submission)
                    break
                except subprocess.CalledProcessError:
                    if num_retries == settings.AG_TEST_MAX_RETRIES:
                        print('max retries exceeded for '
                              'non-deferred test {}'.format(ag_test.pk))
                        raise
                    num_retries += 1
                    print('retrying: {}'.format(num_retries))
                    time.sleep(
                        random.randint(settings.AG_TEST_MIN_RETRY_DELAY,
                                       settings.AG_TEST_MAX_RETRY_DELAY))

        _mark_as_waiting_for_deferred(submission.pk)


@celery.shared_task
def _mark_as_finished(results, submission_id):
    print(results, submission_id)
    print(ag_models.Submission.objects.all())
    with transaction.atomic():
        submission = ag_models.Submission.objects.select_for_update().get(
            pk=submission_id)
        submission.status = ag_models.Submission.GradingStatus.finished_grading
        submission.save()


def _mark_as_waiting_for_deferred(submission_id):
    with transaction.atomic():
        submission = ag_models.Submission.objects.select_for_update().get(
            pk=submission_id)
        if (submission.status !=
                ag_models.Submission.GradingStatus.finished_grading):
            submission.status = (
                ag_models.Submission.GradingStatus.waiting_for_deferred)
            submission.save()


# def _get_queue_name()

# Decisions to make:
#   - Use a chain (run ag tests in series)
#   - Use a chord (run ag tests in parallel)
#   - How to manage queued tests vs how many submissions are labelled as
#   "being graded"
#   -


@celery.shared_task(bind=True, max_retries=settings.AG_TEST_MAX_RETRIES)
def grade_ag_test(self, ag_test_id, submission_id):
    try:
        ag_test = ag_models.AutograderTestCaseBase.objects.get(pk=ag_test_id)
        submission = ag_models.Submission.objects.get(pk=submission_id)

        grade_ag_test_impl(ag_test, submission)
    except subprocess.CalledProcessError as e:
        self.retry(exc=e,
                   countdown=random.randint(settings.AG_TEST_MIN_RETRY_DELAY,
                                            settings.AG_TEST_MAX_RETRY_DELAY))


def grade_ag_test_impl(ag_test, submission):
    group = submission.submission_group

    sandbox = AutograderSandbox(
        name='submission{}-test{}'.format(submission.pk, ag_test.pk),
        environment_variables={
            'usernames': ' '.join(sorted(group.member_names))})

    with sandbox:
        result = ag_test.run(submission, sandbox)
        result.save()