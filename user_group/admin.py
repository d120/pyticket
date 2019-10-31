from ajax_select.admin import AjaxSelectAdmin
from django.contrib import admin
from django.contrib.auth.models import Group

from user_group.models import GroupEmail


class GroupEmailInline(admin.StackedInline):
    model = GroupEmail
    can_delete = False

class GroupAdmin(admin.ModelAdmin):
    inlines = (GroupEmailInline,)
    list_display = ('name', 'get_group_mail')

    def get_group_mail(self, obj):
        return obj.groupemail.email

    get_group_mail.short_description = 'Gruppenemailaddresse'


class MyGroupAdmin(AjaxSelectAdmin):
    """Adds group settings to the admin page. """
    pass

admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
