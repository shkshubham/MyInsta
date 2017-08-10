from __future__ import absolute_import
from django.conf.urls import url
from accounts.api.views import UserListAPIView, UserDetialAPIView, UserUpdateAPIView

urlpatterns = [
    url(r'^users/$', UserListAPIView.as_view(), name='API_user_list'),
    url(r'^(?P<username>[-\w]{5,30})/$', UserDetialAPIView.as_view(), name='API_profile'),
    url(r'^(?P<username>[-\w]{5,30})/update/$', UserUpdateAPIView.as_view(), name='API_update'),
]
