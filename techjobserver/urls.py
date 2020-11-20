from django.conf.urls import url 
from django.urls import path
from .views import scrape, job_list, job_detail

urlpatterns = [
    path('scrape/', scrape, name='Home'),
    path('alljobs/', job_list, name='Latest Tech Jobs'),
    url(r'^alljobs/(?P<pk>[0-9]+)$', job_detail, name='Tech Job'),
]