from django.db import models
from autograder.core.fields import EnumField
import autograder.core.models as ag_models
from django.core import validators
from enum import Enum


class PointsStyle(Enum):
    start_at_zero_and_add = "start_at_zero_and_add",
    start_at_max_and_subtract = "start_at_max_and_subtract"


class HandgradingRubric(ag_models.AutogarderModel):
    """
    The rubric which is linked to the project and adds or subtracts points from or to the total.
    """
    points_style = EnumField(PointsStyle)

    max_points = models.IntegerField(
        validators=[validators.MinValueValidator(0)])

    show_grades_and_rubric_to_students = models.BooleanField()

    handgraders_can_leave_comments = models.BooleanField()

    handgraders_can_apply_arbitrary_points = models.BooleanField()

    project = models.ForeignKey(
        ag_models.Project,
        on_delete=models.CASCADE)



class Criterion(ag_models.AutograderModel):
    short_description = models.TextField()

    long_description = models.TextField()

    points = models.FloatField()

    handgrading_rubric = models.ForeignKey(
        HandgradingRubric,
        on_delete=models.CASCADE)


class Annotation(ag_models.AutograderModel):
    short_description = models.TextField()

    long_description = models.TextField()

    points = models.FloatField()

    handgrading_rubric = models.ForeignKey(
        HandgradingRubric,
        on_delete=models.CASCADE)


class HandgradingResult(ag_models.AutograderModel):
    submission = models.OneToOneField(
        ag_models.Submission,
        on_delete=models.CASCADE)


class CriterionResult(ag_models.AutograderModel):
    selected = models.BooleanField()

    criterion = models.ForeignKey(
        Criterion,
        on_delete=models.CASCADE)

    handgrading_result = models.ForeignKey(
        HandgradingResult,
        on_delete=models.CASCADE)


class AppliedAnnotation(ag_models.AutograderModel):
    comment = models.TextField(
        null=True,
        blank=True,
        default=None)

    location = models.OneToOneField(
        Location,
        on_delete=models.CASCADE)

    annotation = models.ForeignKey(
        Annotation,
        on_delete=models.CASCADE)

    handgrading_result = models.ForeignKey(
        HandgradingResult,
        on_delete=models.CASCADE)


class Comment(ag_models.AutograderModel):
    location = models.OneToOneField(
        Location,
        on_delete=models.CASCADE)

    text = models.TextField()

    handgrading_result = models.ForeignKey(
        HandgradingResult,
        on_delete=models.CASCADE)


class ArbitraryPoints(ag_models.AutograderModel):
    location = models.OneToOneField(
        Location,
        on_delete=models.CASCADE)

    text = models.TextField(
        null=True,
        blank=True,
        default=None)

    points = models.FloatField()

    handgrading_result = models.ForeignKey(
        HandgradingResult,
        on_delete=models.CASCADE)


class Location(ag_models.AutograderModel):
    """how to ensure the following things in the comments?"""
    first_line = models.IntegerField()

    last_line = models.IntegerField()
    '''last line must be >= first line'''

    file_name = models.TextField(
        null=True,
        blank=True,
        default=None)
    '''should be out of the files submitted'''
