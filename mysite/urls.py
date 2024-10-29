from django.urls import path
from mysite.views import home, user_profile_view, GroupMembershipView, InviteView, BillingView

app_name = 'mysite'
urlpatterns = [
    path('details/', user_profile_view, name='user_profile'),
    path("groups/", GroupMembershipView.as_view(), name="group_membership"),
    path("invites/", InviteView.as_view(), name="invites"),
    path("billing/", BillingView.as_view(), name="billing"),
    # path('projects/update/<int:pk>/', ProjectUpdateView.as_view(), name='project_update'),
]
