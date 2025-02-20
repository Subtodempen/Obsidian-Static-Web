from django.urls import path
from . import views

urlpatterns = [
    path('', views.members, name='bl'),
    path('refresh', views.refreshModel, name='r'),

    # Opens a folder or a file
    path('vault/<path:blogTitle>',
         views.dynamicFileRouter, name='blogName'),

    # uses regex, opens a file when .md extenstion is present
    # re_path(r'^(?P<filename>.*\.md)$',
    #        views.openNote, name='blogTitle'),
]
