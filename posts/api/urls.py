from __future__ import absolute_import
from django.conf.urls import url
from posts.api.views import (
    LikeAPIView,
    PostListAPIView,
    PostDetailAPIView,
    PostDeleteAPIView,
    PostUpdateAPIView,
    PostCreateAPIView
)
urlpatterns = [

    url(r'^create/$', PostCreateAPIView.as_view(), name='APIcreate'),
    url(r'^$', PostListAPIView.as_view(), name='APIList'),
    url(r'^(?P<slug>[\w\-]{10})/$', PostDetailAPIView.as_view(), name='APIDetail'),
    url(r'^(?P<slug>[\w\-]{10})/update/$', PostUpdateAPIView.as_view(), name='APIupdate'),
    url(r'^(?P<slug>[\w\-]{10})/delete/$', PostDeleteAPIView.as_view(), name='APIdelete'),
    url(r'^(?P<slug>[\w\-]{10})/$', PostDetailAPIView.as_view(), name='APIview'),
    url(r'^(?P<slug>[\w\-]{10})/like/$', LikeAPIView.as_view(), name='APIlike'),
    #url(r'^(?P<slug>[\w\-]{10})/unlike/$', unlike_post_view, name='unlike'),
]
