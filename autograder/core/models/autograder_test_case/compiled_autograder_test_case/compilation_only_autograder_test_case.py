from django.core.exceptions import ValidationError

from ..autograder_test_case_result import AutograderTestCaseResult

from .compiled_autograder_test_case import CompiledAutograderTestCase


class CompilationOnlyAutograderTestCase(CompiledAutograderTestCase):
    """
    This class evaulates a program by trying to compile it from source code.

    Overridden methods:
        clean()
        test_checks_compilation()
        get_type_str()
        run()
    """
    class Meta:
        proxy = True
    # objects = PolymorphicManagerWithValidateOnCreate()

    # def clean(self):
    #     errors = {}

    #     try:
    #         super().clean()
    #     except ValidationError as e:
    #         errors = e.message_dict

    #     # errors.update(self._clean_files_to_compile_together())

    #     if errors:
    #         raise ValidationError(errors)

    def test_checks_compilation(self):
        return True

    def get_type_str(self):
        return 'compilation_only_test_case'

    # -------------------------------------------------------------------------

    def run(self, submission, autograder_sandbox):
        print('running test: ' + self.name)
        result = AutograderTestCaseResult(
            test_case=self, submission=submission)
        self.add_needed_files_to_sandbox(submission, autograder_sandbox)
        self._compile_program(submission, result, autograder_sandbox)

        return result