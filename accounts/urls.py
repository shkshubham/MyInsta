from __future__ import absolute_import
from django.conf.urls import url
from django.contrib import admin
from accounts.views import (validate_username,
                            LoginView,
                            SignUpView,
                            LogoutView,
                            DetailAccountView,
                            UpdateAccountView,
                            FollowersListView,
                            FollowingListView,
                            ListAccountView,
                            follow_view,
                            unfollow_view
                        )
urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView, name='logout'),
    url(r'^signup/$', SignUpView.as_view(), name='signup'),
    url(r'^users/$', ListAccountView.as_view(), name='user_list'),
    url(r'^(?P<username>[-\w]{5,30})/$', DetailAccountView.as_view(), name='profile'),
    url(r'^(?P<username>[-\w]{5,30})/update/$', UpdateAccountView.as_view(), name='update'),
    url(r'^(?P<username>[-\w]{5,30})/followers$', FollowersListView.as_view(), name='followers'),
    url(r'^(?P<username>[-\w]{5,30})/following$', FollowingListView.as_view(), name='following'),
    url(r'^(?P<username>[-\w]{5,30})/follow/$',follow_view,name='follow'),
    url(r'^(?P<username>[-\w]{5,30})/unfollow/$',unfollow_view,name='unfollow'),
    url(r'^ajax/validate_username/$',validate_username,name='validate_username'),
]
