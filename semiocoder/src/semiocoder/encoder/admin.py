from django.contrib import admin
from semiocoder.encoder.models import Encoder, Joblist, Job, Extension, Task, TaskHistory


class EncoderAdmin(admin.ModelAdmin):
    pass

admin.site.register(Encoder, EncoderAdmin)


class JoblistAdmin(admin.ModelAdmin):
    list_display = ( 'name', 'created_by', 'description', )
    search_fields = ('name', 'description', )

admin.site.register(Joblist, JoblistAdmin)


class JobAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'encoder', 'extension', 'created_on', 'modified_on')
    search_fields = ('name', 'description', 'options', )

admin.site.register(Job, JobAdmin)


class ExtensionAdmin(admin.ModelAdmin):
    pass

admin.site.register(Extension, ExtensionAdmin)


class TaskAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'owner', 'schedule', 'state', 'notify', )
    list_filter = ('state', 'notify', )

admin.site.register(Task, TaskAdmin)


class TaskHistoryAdmin(admin.ModelAdmin):
    list_display = ('joblist', 'owner', 'state', 'starttime', 'endtime', )
    list_filter = ('state', )
    search_fields = ('joblist', )

admin.site.register(TaskHistory, TaskHistoryAdmin)
