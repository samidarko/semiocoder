from django.db import models
from django.contrib.auth.models import User


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
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100, null=True, blank=True)
    owner = models.ForeignKey(User)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now = True)
    encoder = models.ForeignKey(Encoder)
    options = models.CharField(max_length=240)
    extension = models.ForeignKey(Extension)
    
    def __unicode__(self):
        return "%s" % (self.name)
    
    def getDetails(self):
        details = {}
        for name in self.__dict__:
            if not name.startswith('_'):
                details[name] =  self.__dict__[name]
        return details

class Joblist(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100, null=True, blank=True)
    owner = models.ForeignKey(User)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now = True)
    job = models.ManyToManyField(Job)

    def __unicode__(self):
        return "%s" % (self.name)
    
    def getDetails(self):
        details = {}
        for name in self.__dict__:
            if not name.startswith('_'):
                details[name] =  self.__dict__[name]
        return details
    
# TODO: si on supprime purger source_file 
class Task(models.Model):
    joblist = models.ForeignKey(Joblist)
    schedule = models.DateTimeField()
    owner = models.ForeignKey(User)
    state = models.CharField(max_length=1, choices=(('W','Waiting'),('P','Pending'),('R','Running'),), default='W')
    source_file = models.FileField(upload_to="videos/%Y%m%d_%H%M%S")
    notify = models.BooleanField()
    
    def __unicode__(self):
        return "task %d" % (self.id)
    
    def getDetails(self):
        details = {}
        for name in self.__dict__:
            if not name.startswith('_'):
                details[name] =  self.__dict__[name]
        return details

class TaskHistory(models.Model):
    joblist = models.CharField(max_length=30)
    owner = models.ForeignKey(User)
    state = models.CharField(max_length=1, choices=(('C','Completed'),('F','Failed'),))
    starttime = models.DateTimeField()
    endtime = models.DateTimeField()
    outputdir = models.CharField(max_length=20)
    log = models.TextField(null=True, blank=True)
    

    
    
