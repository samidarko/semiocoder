# -*- coding: utf-8 -*-
"""
.. module:: views
   :platform: Unix, Windows
   :synopsis: Module de configuration de la partie administration de l'encodeur

.. moduleauthor:: Samuel Darko <samidarko@gmail.com>

"""
from django.contrib import admin
from semiocoder.encoder.models import Encoder, Joblist, Job, Extension, Task, TaskHistory


class EncoderAdmin(admin.ModelAdmin):
    """Classe d'administration de l'objet Encoder
    """

admin.site.register(Encoder, EncoderAdmin)


class JoblistAdmin(admin.ModelAdmin):
    """Classe d'administration de l'objet Joblist
    """
    list_display = ( 'name', 'owner', 'description', )
    search_fields = ('name', 'description', )

admin.site.register(Joblist, JoblistAdmin)


class JobAdmin(admin.ModelAdmin):
    """Classe d'administration de l'objet Job
    """
    list_display = ('name', 'owner', 'encoder', 'extension', 'created_on', 'modified_on')
    search_fields = ('name', 'description', 'options', )

admin.site.register(Job, JobAdmin)


class ExtensionAdmin(admin.ModelAdmin):
    """Classe d'administration de l'objet Extension
    """

admin.site.register(Extension, ExtensionAdmin)


class TaskAdmin(admin.ModelAdmin):
    """Classe d'administration de l'objet Task
    """
    list_display = ('__unicode__', 'owner', 'schedule', 'state', 'notify', )
    list_filter = ('state', 'notify', )

admin.site.register(Task, TaskAdmin)


class TaskHistoryAdmin(admin.ModelAdmin):
    """Classe d'administration de l'objet TaskHistory
    """
    list_display = ('joblist', 'owner', 'state', 'starttime', 'endtime', 'outputdir', )
    list_filter = ('state', )
    search_fields = ('joblist', )

admin.site.register(TaskHistory, TaskHistoryAdmin)
