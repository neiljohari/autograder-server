import itertools

from django.contrib.auth.models import User
from django.core import exceptions
from django.db import models, transaction

from .. import ag_model_base
from .. project import Project
from autograder.utilities import fields as ag_fields

from . import verification


class SubmissionGroupInvitationManager(ag_model_base.AutograderModelManager):
    def validate_and_create(self, invitation_creator, invited_users, **kwargs):
        with transaction.atomic():
            verification.verify_users_can_be_in_group(
                tuple(itertools.chain(invited_users, (invitation_creator,))),
                kwargs['project'], 'invited_users')

            invitation = self.model(
                invitation_creator=invitation_creator, **kwargs)
            invitation.save()
            invitation.invited_users.add(*invited_users)
            invitation.full_clean()
            return invitation


class SubmissionGroupInvitation(ag_model_base.AutograderModel):
    """
    This class stores an invitation for a set of users to create a
    SubmissionGroup together.
    """
    DEFAULT_INCLUDE_FIELDS = [
        'invitation_creator',
        'project',
        'invited_usernames',
        'invitees_who_accepted',
    ]

    invited_users = models.ManyToManyField(
        User, related_name='group_invitations_received',
        help_text="""The Users that the invitation_creator has invited
            to form a submission group together.
            This field is REQUIRED.
            This field may not be empty.""")

    invitation_creator = models.ForeignKey(
        User, related_name='group_invitations_sent',
        help_text="""The User who created this invitation.
            This field is REQUIRED.""")

    _invitees_who_accepted = ag_fields.StringArrayField(
        default=list, blank=True)

    project = models.ForeignKey(Project)

    objects = SubmissionGroupInvitationManager()

    def clean(self):
        super().clean()
        if not self.invited_users.count():
            raise exceptions.ValidationError(
                {'invited_users': 'This field may not be empty'})

    @property
    def invited_usernames(self):
        """
        The usernames of the Users that will receive this invitation.
        """
        return (user.username for user in self.invited_users.all())

    @property
    def invitees_who_accepted(self):
        """
        A list of usernames indicating which invitees have accepted
        this invitation.
        This field is READ ONLY.
        """
        return tuple(self._invitees_who_accepted)

    @property
    def all_invitees_accepted(self):
        """
        Returns True if all invited users have accepted the invitation.
        """
        return set(self.invited_usernames) == set(self._invitees_who_accepted)

    def invitee_accept(self, user):
        """
        Marks the given user as having accepted the group invitation.
        """
        if user == self.invitation_creator:
            return

        if user in self.invitees_who_accepted:
            return

        self._invitees_who_accepted.append(user.username)
        self.save()

    def to_dict(self, **kwargs):
        result = super().to_dict(**kwargs)

        if 'invitation_creator' in result:
            result['invitation_creator'] = self.invitation_creator.username

        return result