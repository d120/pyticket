from django.contrib import admin
from datetime import datetime

# Register your models here.
from .models import Ticket, Comment, TicketLog, Log


class TicketAdmin(admin.ModelAdmin):
    """
    custom ModelAdmin for Ticket
    """
    def save_model(self, request, obj, form, change):
        """
        custom logic for saving a ticket on django admin
        """
        # if assigned_user has been changed an not to null
        if 'assigned_user' in form.changed_data and form.data['assigned_user']:
            # time_assign_user gets updated to now
            obj.time_assign_user = datetime.now()
        # if no creator_user is given
        if not obj.creator_user:
            # update the creator_user to the requested user
            obj.creator_user = request.user
        return super(TicketAdmin, self).save_model(request, obj, form, change)

admin.site.register(Ticket, TicketAdmin)
admin.site.register(Comment)
admin.site.register(TicketLog)
admin.site.register(Log)
