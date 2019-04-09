from django.urls import path
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from ajax_select import urls as ajax_select_urls


from .views import NewGroupView, RemoveUserGroupView, EditGroupView, DashboardGroupView

admin.autodiscover()

urlpatterns = [
    path('', DashboardGroupView.as_view(), name="group"),
    path('edit/<int:group_id>/', EditGroupView.as_view(), name="edit_group"),
    path('delete/<int:group_id>/', RemoveUserGroupView.as_view(), name="delete_group"),
    path('group/<int:group_id>/', DashboardGroupView.as_view(), name="dashboard_group"),
    url(r'^new_group/',    view=NewGroupView.as_view(), name='new_group'),
    url(r'^admin/lookups/', include(ajax_select_urls)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
