from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    #API
    url(r'^api$', views.api, name="api$"),
    
)