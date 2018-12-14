from django.conf.urls import url
from .views import (
    post_list, post_detail, post_new, post_edit, post_draft_list, post_publish,
    post_remove,
)
urlpatterns = [
    url(r'^$', post_list, name='post_list'),
    url(r'^post/(?P<pk>\d+)/$', post_detail, name='post_detail'),
    url(r'^post/new/$', post_new, name='post_new'),
    url(r'^post/(?P<pk>\d+)/edit/$', post_edit, name='post_edit'),
    url(r'^drafts/$', post_draft_list, name='post_draft_list'),
    url(r'^post/(?P<pk>\d+)/publish/$', post_publish, name='post_publish'),
    url(r'^post/(?P<pk>\d+)/remove/$', post_remove, name='post_remove'),
]
