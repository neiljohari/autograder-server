# import uuid

from django.core import exceptions

from .autograder_test_case_base import AutograderTestCaseBase


class CompiledAutograderTestCase(AutograderTestCaseBase):
    """
    This class allows evaluating a program that will be compiled
    and then run.

    Field changes:
        compiler -- This field is REQUIRED
        executable_name -- This field is REQUIRED
    """
    class Meta:
        proxy = True

    def test_checks_compilation(self):
        return True

    def clean(self):
        if not self.compiler:
            raise exceptions.ValidationError(
                {'compiler': 'The "compiler" field must be '
                             'specified for this AG test type'})

        if not self.executable_name:
            raise exceptions.ValidationError(
                {'executable_name': 'The "executable_name" field '
                                    'cannot be empty for this AG test type.'})

    def _compile_program(self, submission, result_ref, autograder_sandbox):
        compilation_command = (
            [self.compiler] + self.compiler_flags +
            self.project_files_to_compile_together +
            self.student_files_to_compile_together
        )

        if self.compiler == 'g++' and self.executable_name:
            compilation_command += ['-o', self.executable_name]

        compile_result = autograder_sandbox.run_command(
            compilation_command, timeout=self.time_limit)
        result_ref.submission = submission
        result_ref.compilation_standard_output = compile_result.stdout
        result_ref.compilation_standard_error_output = compile_result.stderr
        result_ref.compilation_return_code = compile_result.return_code
