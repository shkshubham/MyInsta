from __future__ import absolute_import
from django.conf.urls import url
from posts.views import DetailPostView, unlike_post_view, like_post_view, UpdatePostView, CreatePostView, DeletePostView

urlpatterns = [
    url(r'^create/$', CreatePostView.as_view(), name='create'),
    url(r'^(?P<slug>[\w\-]{10})/update/$', UpdatePostView.as_view(), name='update'),
    url(r'^(?P<slug>[\w\-]{10})/delete/$', DeletePostView.as_view(), name='delete'),
    url(r'^(?P<slug>[\w\-]{10})/$', DetailPostView.as_view(), name='view'),
    url(r'^(?P<slug>[\w\-]{10})/like/$', like_post_view, name='like'),
    url(r'^(?P<slug>[\w\-]{10})/unlike/$', unlike_post_view, name='unlike'),
]
