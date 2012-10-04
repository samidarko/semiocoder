import os, json, datetime
from django.contrib.auth import views
from django.shortcuts import get_object_or_404
from semiocoder.settings import VIDEO_ROOT, MEDIA_URL
from semiocoder.encoder.models import Encoder, Job, Joblist, Task, TaskHistory, Extension
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


def logout(user):
    return { 'semiocoder' : { 'logout' :  datetime.datetime.now(), } }


def login(r):
    views.login(r, redirect_field_name='/api')
    
#============ Ensemble des fonctions get ===========================

def getEncoderDetail(user, object_id):
    result = {}
    encoder = get_object_or_404(Encoder, pk=object_id)
    result["id"] = encoder.id
    result["name"] = encoder.name
    result["inputflag"] = encoder.inputflag
    result["outputflag"] = encoder.outputflag
    return { 'encoder' : result }


def getEncoders(user):
    result = {}
    result["encoders"] = []
    encoders = Encoder.objects.all()
    for encoder in encoders:
        result["encoders"].append(getEncoderDetail(user, encoder.id))
    return result
   

def getExtensionDetail(user, object_id):
    result = {}
    encoder = get_object_or_404(Extension, pk=object_id)
    result["id"] = encoder.id
    result["name"] = encoder.name
    return { 'extension' : result }


def getExtensions(user):
    result = {}
    result["extensions"] = []
    extensions = Extension.objects.all()
    for extension in extensions:
        result["extensions"].append(getExtensionDetail(user, extension.id))
    return result
    


def getJobDetail(user, object_id):
    result = {}
    job = get_object_or_404(Job, owner=user, pk=object_id)
    result["id"] = job.id
    result["name"] = job.name
    result["description"] = job.description
    result["owner"] = job.owner
    result["created_on"] = job.created_on
    result["modified_on"] = job.modified_on
    result["encoder"] = job.encoder.name
    result["options"] = job.options
    return { 'job' : result }


def getJobs(user):
    result = {}
    result["jobs"] = []
    jobs = Job.objects.filter(owner=user)
    for job in jobs:
        result["jobs"].append(getJobDetail(user, job.id))
    return result


def getJoblistDetail(user, object_id):
    result = {}
    joblist = get_object_or_404(Joblist, owner=user, pk=object_id)
    result["id"] = joblist.id
    result["name"] = joblist.name
    result["description"] = joblist.description
    result["owner"] = joblist.owner
    result["created_on"] = joblist.created_on
    result["modified_on"] = joblist.modified_on
    result["job"] =  [ item.id for item in joblist.job.select_related()]
    return { 'joblist' : result }


def getJoblists(user):
    result = {}
    result["joblists"] = []
    joblists = Joblist.objects.filter(owner=user)
    for joblist in joblists:
        result["joblists"].append(getJoblistDetail(user, joblist.id))
    return result


def getTaskDetail(user, object_id):
    result = {}
    task = get_object_or_404(Task, owner=user, pk=object_id)
    result["id"] = task.id
    result["joblist"] = task.joblist.name
    result["schedule"] = task.schedule
    result["owner"] = task.owner
    result["state"] = task.state
    result["source_file"] = os.path.basename(task.source_file.name)
    result["notify"] = task.notify
    return { 'task' : result }


def getTasks(user):
    result = {}
    result["tasks"] = []
    tasks = Task.objects.filter(owner=user)
    for task in tasks:
        result["tasks"].append(getTaskDetail(user, task.id))
    return result


def getHistoryDetail(user, object_id):
    result = {}
    history = get_object_or_404(TaskHistory, owner=user, pk=object_id)
    result["id"] = history.id
    result["joblist"] = history.joblist
    result["owner"] = history.owner
    result["state"] = history.state
    result["starttime"] = history.starttime
    result["endtime"] = history.endtime
    if history.outputdir:
        result["outputdir"] = [ '%svideos/%s/%s' % (MEDIA_URL,history.outputdir,f) for f in os.listdir(VIDEO_ROOT+"/"+history.outputdir)]
    else:
        result["outputdir"]=['No Files']
    result["log"] = history.log
    return { 'history' : result }
    

def getHistories(user):
    result = {}
    result["histories"] = []
    histories = TaskHistory.objects.filter(owner=user)
    for history in histories:
        result["histories"].append(getHistoryDetail(user, history.id))
    return result

#============ Ensemble des fonctions add ===========================

def addJob(req):
    j = Job(owner=req.user)
    form = JobForm(req.POST, instance=j)
    if form.is_valid(): 
        obj = form.save()
        return getJobDetail(req.user,obj.id)
    else:
        return { 'job' : form.errors }


def addJoblist(req):
    jl = Joblist(owner=req.user)
    form = JoblistForm(req.user, req.POST, instance=jl)
    if form.is_valid(): 
        obj = form.save()
        return getJoblistDetail(req.user,obj.id)
    else:
        return { 'joblist' : form.errors }


def addTask(req):
    t = Task(owner=req.user)
    form = TaskForm(req.user, req.POST, req.FILES, instance=t)
    if form.is_valid():
        obj = form.save()
        return getTaskDetail(req.user,obj.id)
    else:
        return { 'task' : form.errors }

#============ Ensemble des fonctions edit ===========================

def editJob(req):
    try:
        j = Job.objects.get(id=req.POST['id'],owner=req.user)
    except:
        return { 'job' : { 'exception' : 'DoesNotExist' } } 
    form = JobForm(req.POST, instance=j)
    if form.is_valid(): 
        obj = form.save()
        return getJobDetail(req.user,obj.id)
    else:
        return { 'job' : form.errors }


def editJoblist(req):
    try:
        jl = Joblist.objects.get(id=req.POST['id'],owner=req.user)
    except:
        return { 'joblist' : { 'exception' : 'DoesNotExist' } } 
    form = JoblistForm(req.user, req.POST, instance=jl)
    if form.is_valid(): 
        obj = form.save()
        return getJoblistDetail(req.user,obj.id)
    else:
        return { 'joblist' : form.errors }

#============ Ensemble des fonctions delete ===========================

def deleteJob(req):
    try:
        j = Job.objects.get(id=req.POST['id'],owner=req.user)
    except:
        return { 'job' : { 'exception' : 'DoesNotExist' } } 
    
    try:
        j.delete()
        return { 'job' : { 'status' : 'success' } }
    except:
        return { 'job' : { 'status' : 'fail' } }


def deleteJoblist(req):
    try:
        jl = Joblist.objects.get(id=req.POST['id'],owner=req.user)
    except:
        return { 'joblist' : { 'exception' : 'DoesNotExist' } } 
    
    try:
        jl.delete()
        return { 'job' : { 'status' : 'success' } }
    except:
        return { 'job' : { 'status' : 'fail' } }
    
    
def deleteTask(req):
    try:
        t = Task.objects.get(id=req.POST['id'],owner=req.user)
    except:
        return { 'task' : { 'exception' : 'DoesNotExist' } } 
    
    try:
        t.delete()
        return { 'job' : { 'status' : 'success' } }
    except:
        return { 'job' : { 'status' : 'fail' } }
