from enum import Enum


class StudentTestSuiteFeedbackConfiguration:
    """
    Members:
        compilation_feedback_level
        student_test_validity_feedback_level
        buggy_implementations_exposed_feedback_level
    """
    def __init__(self, **kwargs):
        self.compilation_feedback_level = kwargs.get(
            'compilation_feedback_level', CompilationFeedbackLevel())

        self.student_test_validity_feedback_level = kwargs.get(
            'student_test_validity_feedback_level',
            StudentTestCaseValidityFeedbackConfiguration())

        self.buggy_implementations_exposed_feedback_level = kwargs.get(
            'buggy_implementations_exposed_feedback_level',
            BuggyImplementationsExposedFeedbackLevel())

    @property
    def compilation_feedback_level(self):
        return self._compilation_feedback_level

    @compilation_feedback_level.setter
    def compilation_feedback_level(self, value):
        self._compilation_feedback_level = CompilationFeedbackLevel(value)

    @property
    def student_test_validity_feeback_level(self):
        return self._student_test_validity_feeback_level

    @student_test_validity_feeback_level.setter
    def student_test_validity_feeback_level(self, value):
        self._compilation_feedback_level = (
            StudentTestCaseValidityFeedbackConfiguration(
                value))

    @property
    def buggy_implementations_exposed_feedback_level(self):
        return self._buggy_implementations_exposed_feedback_level

    @buggy_implementations_exposed_feedback_level.setter
    def buggy_implementations_exposed_feedback_level(self, value):
        self._compilation_feedback_level = (
            BuggyImplementationsExposedFeedbackLevel(value))


class StudentTestCaseValidityFeedbackConfiguration(Enum):
    no_feedback = 'no_feedback'
    show_valid_or_invalid = 'show_valid_or_invalid'


class BuggyImplementationsExposedFeedbackLevel(Enum):
    no_feedback = 'no_feedback'
    list_implementations_exposed = 'list_implementations_exposed'


class CompilationFeedbackLevel(Enum):
    no_feedback = 'no_feedback'
    success_or_failure_only = 'success_or_failure_only'
    show_compiler_output = 'show_compiler_output'


class ReturnCodeFeedbackLevel(Enum):
    no_feedback = 'no_feedback'
    correct_or_incorrect_only = 'correct_or_incorrect_only'
    show_expected_and_actual_values = 'show_expected_and_actual_values'


class OutputFeedbackLevel(Enum):
    no_feedback = 'no_feedback'
    correct_or_incorrect_only = 'correct_or_incorrect_only'
    show_expected_and_actual_values = 'show_expected_and_actual_values'


class PointsFeedbackLevel:
    hide = 'hide'
    # Note: When "show_total" or "show_breakdown" is chosen,
    # it will only show the
    # points from parts of the test case or suite that the
    # student receives feedback on.
    show_total = 'show_total'
    show_breakdown = 'show_breakdown'
