from django import template
register = template.Library()

@register.filter
def to_timestamp(datetime_obj):
    """Convert datetime to unix timestamp"""
    return int(datetime_obj.timestamp())

@register.filter
def filter_invite(invites, meeting):
    """
    Given a queryset/list of invites and a meeting, return the invite that belongs to that meeting,
    if found, otherwise returns None.
    """
    # If invites is a queryset, we can use the filter method directly.
    if hasattr(invites, 'filter'):
        return invites.filter(meeting=meeting).first()
    
    # If it's a list, iterate and check manually.
    for invite in invites:
        if invite.meeting == meeting:
            return invite
    return None

@register.simple_tag
def get_attendees(meeting, exclude_user, include_organiser=False):
    return meeting.get_confirmed_attendees(exclude_user=exclude_user,include_organiser=include_organiser)



@register.filter
def filter_invitations(meetings, user):
    """
    Filters out meetings where the invitation for the given user has a status of True.

    Usage in template:
      {% load meeting_extras %}
      {% for meeting in meetings|filter_invitations:request.user %}
          <!-- display meeting -->
      {% endfor %}
    """
    try:
        # Exclude meetings where the invitation for the given user is True.
        return meetings.exclude(invitations__user=user, invitations__status=True)
    except Exception:
        # If something goes wrong (e.g. not a QuerySet), just return the original meetings.
        return meetings