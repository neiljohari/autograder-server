import os

from django.db import models
from django.core.validators import MinLengthValidator

from autograder.models.model_validatable_on_save import ModelValidatableOnSave
from autograder.models import Course

import autograder.shared.global_constants as gc
import autograder.shared.utilities as ut


class Semester(ModelValidatableOnSave):
    """
    Represents a semester or term in which a course takes place.


    Fields:
        name -- The name used to identify this Semester.
                Must be non-empty and non-null.
                Must be unique among Semesters associated with a given Course.

        course -- The Course that this semester is associated with.

    Overridden member functions:
        save()
    """
    class Meta:
        unique_together = ('name', 'course')

    name = models.CharField(
        max_length=gc.MAX_CHAR_FIELD_LEN,
        validators=[MinLengthValidator(1, "Name can't be empty")])
    course = models.ForeignKey(Course)

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        semester_root_dir = ut.get_semester_root_dir(self)
        if not os.path.isdir(semester_root_dir):
            # Since the database is in charge or validating the uniqueness
            # of this semester, we can assume at this point that creating
            # the semester directory will succeed. If for some reason it fails,
            # this will be considered a more severe error, and the OSError
            # thrown by os.makedirs will be handled at a higher level.

            os.makedirs(semester_root_dir)
