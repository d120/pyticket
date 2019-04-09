from __future__ import unicode_literals
from ajax_select import register, LookupChannel
from account.models import MyUser
from django.db.models import Q

# used in .forms.py
@register('look_members')
class UserLookup(LookupChannel):
    """
    Returns all participants matching the search criteria username,
    first name or last name.
    """
    model = MyUser

    def get_query(self, q, request):
        """
        param: q - the value for which the user is searching
        param: request - the request of the user
        return: list of MyUser objects which match the filter
        """
        return MyUser.objects.filter(
            Q(username__icontains=q) | Q(first_name__icontains=q) | Q(
                last_name__icontains=q)).order_by('username')

    def format_item_display(self, item):
        """
        formats the items shown below AutoCompleteSelectMultipleField
        param: item - the item which has been selected
        return: String - the items username converted to nice html
        """
        return u"<span class='tag'>%s</span>" % item.username
