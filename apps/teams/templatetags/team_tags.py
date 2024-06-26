from django import template

from apps.teams.roles import is_member, is_admin
from apps.teams.models import Team

register = template.Library()


@register.filter
def is_member_of(user, team_name):
    try:
        team = Team.objects.get(name=team_name)  # Retrieve the Team object
    except Team.DoesNotExist:
        return False  # Return False if the team doesn't exist

    return is_member(user, team)


@register.filter
def is_admin_of(user, team):
    return is_admin(user, team)
