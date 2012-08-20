import os
import json
from django.contrib.auth import views
from django.http import HttpResponseRedirect
from semiocoder.settings import LOGOUT_URL
from semiocoder.encoder.models import Encoder, Job, Joblist, Task, TaskHistory
from semiocoder.encoder.forms import TaskForm, JobForm, JoblistForm
from xml.dom.minidom import Document


def formatResult(formatting, result):
    if formatting == "json":
        return json.dumps(result)
    elif formatting == "xml":
        document = Document()
        root = document.createElement(result.keys()[0])
        elements = result.values()[0]
        if isinstance (elements, dict):
            for k, v in elements.iteritems():
                child1 = document.createElement(k)
                child1.appendChild(document.createTextNode(str(v)))
                root.appendChild(child1)
            document.appendChild(root)
        elif isinstance (elements, list):
            for el in elements:
                child1 = document.createElement(el.keys()[0])
                for k, v in el.values()[0].iteritems():
                    child2 = document.createElement(k)
                    child2.appendChild(document.createTextNode(str(v)))
                    child1.appendChild(child2)
                root.appendChild(child1)
            document.appendChild(root)
        return document

def logout():
    return HttpResponseRedirect(LOGOUT_URL)

def login(r):
    views.login(r, redirect_field_name='/api')


def getEncoderDetails(encoder):
    result = {}
    encoder = Encoder.objects.get(pk=encoder)
    result["id"] = encoder.id
    result["name"] = encoder.name
    result["inputflag"] = encoder.inputflag
    result["outputflag"] = encoder.outputflag
    return { 'encoder' : result }

    

def getEncoders():
    result = {}
    result["encoders"] = []
    encoders = Encoder.objects.all()
    for encoder in encoders:
        result["encoders"].append(getEncoderDetails(encoder.id))
    return result

def getJobDetails(job):
    result = {}
    job = Job.objects.get(pk=job)
    result["id"] = job.id
    result["name"] = job.name
    result["description"] = job.description
    result["created_by"] = job.created_by
    result["created_on"] = job.created_on.strftime('%Y-%m-%d %H:%M:%S')
    result["modified_by"] = job.created_by
    result["modified_on"] = job.modified_on.strftime('%Y-%m-%d %H:%M:%S')
    result["encoder"] = job.encoder.name
    result["options"] = job.options
    result["outputfilename"] = job.outputfilename
    return { 'job' : result }


def getJobs():
    result = {}
    result["jobs"] = []
    jobs = Job.objects.all()
    for job in jobs:
        result["jobs"].append(getJobDetails(job.id))
    return result

def getJoblistDetails(joblist):
    result = {}
    joblist = Joblist.objects.get(pk=joblist)
    result["id"] = joblist.id
    result["name"] = joblist.name
    result["description"] = joblist.description
    result["created_by"] = joblist.created_by
    result["created_on"] = joblist.created_on.strftime('%Y-%m-%d %H:%M:%S')
    result["modified_by"] = joblist.created_by
    result["modified_on"] = joblist.modified_on.strftime('%Y-%m-%d %H:%M:%S')
    result["modified_on"] = joblist.modified_on.strftime('%Y-%m-%d %H:%M:%S')
    result["job"] =  [ item.name for item in joblist.job.select_related()]
    return { 'joblist' : result }


def getJoblists():
    result = {}
    result["joblists"] = []
    joblists = Joblist.objects.all()
    for joblist in joblists:
        result["joblists"].append(getJoblistDetails(joblist.id))
    return result

def getTaskDetails(task):
    result = {}
    task = Task.objects.get(pk=task)
    result["id"] = task.id
    result["joblist"] = task.joblist.name
    result["schedule"] = task.schedule.strftime('%Y-%m-%d %H:%M:%S')
    result["owner"] = task.owner
    result["state"] = task.state
    result["source_file"] = os.path.basename(task.source_file.name)
    result["notify"] = task.notify
    return { 'task' : result }

def getTasks():
    result = {}
    result["tasks"] = []
    tasks = Task.objects.all()
    for task in tasks:
        result["tasks"].append(getTaskDetails(task.id))
    return result

def gethistorydetails(history):
    result = {}
    history = TaskHistory.objects.get(pk=history)
    result["id"] = history.id
    result["joblist"] = history.joblist
    result["owner"] = history.owner
    result["state"] = history.state
    result["starttime"] = history.starttime.strftime('%Y-%m-%d %H:%M:%S')
    result["endtime"] = history.endtime.strftime('%Y-%m-%d %H:%M:%S')   
    result["outputdir"] = [ '/static/videos/%s/%s' % (history.outputdir,f) for f in os.listdir("media/videos/"+history.outputdir)]
    if len(result["outputdir"])==0: result["outputdir"]=['No Files']
    result["log"] = history.log
    return { 'history' : result }
    

def getHistories():
    result = {}
    result["histories"] = []
    histories = TaskHistory.objects.all()
    for history in histories:
        result["histories"].append(gethistorydetails(history.id))
    return result


def setJob(r):
    username = r.user.username
    j = Job(created_by=username, modified_by=username)
    form = JobForm(r.POST, instance=j)
    if form.is_valid(): 
        form.save()
        result = "Job created"
    else:
        result = "The job could not be created"
    return result



def setJoblist(r):
    username = r.user.username
    jl = Joblist(created_by=username, modified_by=username)
    form = JoblistForm(r.POST, instance=jl)
    if form.is_valid(): 
        form.save()
        result = "Joblist created"
    else:
        result = "The joblist could not be created"
    return result

def setTask(r):
    username = r.user.username
    t = Task(owner=username, state="idle")
    form = TaskForm(r.POST, r.FILES, instance=t)
    if form.is_valid():
        form.save()
        result = "Task created"
    else:
        result = "The task could not be created"
    return result


        
        
        

        



    