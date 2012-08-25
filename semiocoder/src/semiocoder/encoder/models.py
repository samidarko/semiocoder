# -*- coding: utf-8 -*-
"""
.. module:: models
   :platform: Unix, Windows
   :synopsis: description du modèle de données l'application encodeur

.. moduleauthor:: Samuel Darko <samidarko@gmail.com>

"""
import os
from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import Collector
from django.db import router
from django.core.urlresolvers import reverse


class Encoder(models.Model):
    name = models.CharField(max_length=10)
    path = models.FilePathField(path='static/exe')
    inputflag = models.CharField(max_length=10, blank=True, null=True)
    outputflag = models.CharField(max_length=10, blank=True, null=True)

    def __unicode__(self):
        return "encoder: %s" % (self.name)   
    
class Extension(models.Model):
    name = models.CharField(max_length=5)
    
    def __unicode__(self):
        return ".%s" % (self.name)

class Job(models.Model):
    name = models.CharField("nom", max_length=30)
    description = models.CharField("description", max_length=100, null=True, blank=True)
    owner = models.ForeignKey(User)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now = True)
    encoder = models.ForeignKey(Encoder, verbose_name="encodeur")
    options = models.CharField(max_length=240)
    extension = models.ForeignKey(Extension)
    
    def __unicode__(self):
        return "%s" % (self.name)
    
    def get_absolute_url(self):        
        return reverse('job_detail', args = [ self.id, ])



class Joblist(models.Model):
    name = models.CharField("nom", max_length=30)
    description = models.CharField(max_length=100, null=True, blank=True)
    owner = models.ForeignKey(User)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now = True)
    job = models.ManyToManyField(Job)

    def __unicode__(self):
        return "%s" % (self.name)
    
    def get_absolute_url(self):        
        return reverse('joblist_detail', args = [ self.id, ])



class Task(models.Model):
    joblist = models.ForeignKey(Joblist)
    schedule = models.DateTimeField("planification")
    owner = models.ForeignKey(User)
    state = models.CharField(max_length=1, choices=(('W','Waiting'),('P','Pending'),('R','Running'),), default='W')
    source_file = models.FileField("fichier source", upload_to="videos/%Y%m%d_%H%M%S")
    notify = models.BooleanField("notification")
    
    def __unicode__(self):
        return "task %d" % (self.id)
    
    def get_absolute_url(self):        
        return reverse('task_detail', args = [ self.id, ])
    
    def delete(self, using=None):
        """Surcharge de la methode save pour supprimer le fichier source avant l objet
        """
        using = using or router.db_for_write(self.__class__, instance=self)
        assert self._get_pk_val() is not None, "%s object can't be deleted because its %s attribute is set to None." % (self._meta.object_name, self._meta.pk.attname)
        
        if self.source_file:
            tab_path = self.source_file.name.split('/') # decoupage du chemin vers le fichier source
            rep_path = os.path.join("media",tab_path[0],tab_path[1]) # recomposition du chemin du repertoire du fichier source 
            self.source_file.delete() # suppression du fichier source
            if len(os.listdir(rep_path)) == 0: # si le repertoire du fichier source est vide
                try:
                    os.rmdir(rep_path) # suppression du repertoire
                except:
                    pass # Si un probleme survient on ne fait rien
                
        collector = Collector(using=using)
        collector.collect([self])
        collector.delete()


class TaskHistory(models.Model):
    joblist = models.CharField(max_length=30)
    owner = models.ForeignKey(User)
    state = models.CharField(max_length=1, choices=(('C','Completed'),('F','Failed'),))
    starttime = models.DateTimeField()
    endtime = models.DateTimeField()
    outputdir = models.CharField(max_length=20)
    log = models.TextField(null=True, blank=True)
    
    def __unicode__(self):
        return "task history %d" % (self.id)

    
    

    
    
