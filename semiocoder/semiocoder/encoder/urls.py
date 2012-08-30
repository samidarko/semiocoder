from django.conf.urls import patterns, url
import views, api

urlpatterns = patterns('',

    #Tasks
    url(r'^task/$', views.task_list, name="tasks"),
    url(r'^task/(\d+)$', views.task_detail, name="task_detail"),
    url(r'^task/add$', views.task_create, name="task_add"),
    url(r'^task/edit/(\d+)$', views.task_update, name="task_edit"),
    url(r'^task/delete/(\d+)$', views.task_delete, name="task_delete"),
    url(r'^task/data$', views.task_data, name="task_data"),
    url(r'^task/history/$', views.task_history, name="task_history"),
    url(r'^task/history/data$', views.task_history_data, name="task_history_data"),
    url(r'^task/history/output/(\d+)$', views.task_output, name="task_output"),
    url(r'^task/history/log/(\d+)$', views.task_log, name="task_log"),
    
    
    #Joblist
    url(r'^joblist/$', views.joblist_list, name="joblists"),
    url(r'^joblist/(\d+)$', views.joblist_detail, name="joblist_detail"),
    url(r'^joblist/add$', views.joblist_create, name="joblist_add"),
    url(r'^joblist/edit/(\d+)$', views.joblist_update, name="joblist_edit"),
    url(r'^joblist/delete/(\d+)$', views.joblist_delete, name="joblist_delete"),
    url(r'^joblist/data/(\d+)$', views.joblist_jobs_data, name="joblist_jobs_data"),
    url(r'^joblist/data/\d+/(\d+)/$', views.joblist_job_detail_data, name="joblist_job_detail_data"),
    
    #Job
    url(r'^job/$', views.job_list, name="jobs"),
    url(r'^job/(\d+)$', views.job_detail, name="job_detail"),
    url(r'^job/add$', views.job_create, name="job_add"),
    url(r'^job/edit/(\d+)$', views.job_update, name="job_edit"),
    url(r'^job/delete/(\d+)$', views.job_delete, name="job_delete"),
    url(r'^job/data$', views.job_data, name="job_data"),

    #Search
    url(r'^search/$', views.search, name="search"),

    #API
    url(r'^api$', api.api, name="api$"),
    
)
