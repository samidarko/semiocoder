import os, json, datetime
from django.contrib.auth import views
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


def login(request):
    views.login(request, redirect_field_name='/api')
    

def getEncoderDetail(user, object_id):
    
    result = {}
    try:
        obj = Encoder.objects.get(id=object_id)
        result["id"] = obj.id
        result["name"] = obj.name
        result["inputflag"] = obj.inputflag
        result["outputflag"] = obj.outputflag
    except:
        result.update({ 'error' : "Encoder does not exist", 'id' : object_id, })

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
    try:
        obj = Extension.objects.get(id=object_id)
        result["id"] = obj.id
        result["name"] = obj.name
    except:
        result.update({ 'error' : "Extension does not exist", 'id' : object_id, })

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
    try:
        obj = Job.objects.get(owner=user, id=object_id)
        result["id"] = obj.id
        result["name"] = obj.name
        result["description"] = obj.description
        result["owner"] = obj.owner
        result["created_on"] = obj.created_on
        result["modified_on"] = obj.modified_on
        result["encoder"] = obj.encoder.id
        result["options"] = obj.options
        result["extension"] = obj.extension.id
    except:
        result.update({ 'error' : "Job does not exist", 'id' : object_id, })
    
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
    try:
        obj = Joblist.objects.get(owner=user, id=object_id)
        result["id"] = obj.id
        result["name"] = obj.name
        result["description"] = obj.description
        result["owner"] = obj.owner
        result["created_on"] = obj.created_on
        result["modified_on"] = obj.modified_on
        result["job"] =  [ item.name for item in obj.job.select_related()]
    except:
        result.update({ 'error' : "Joblist does not exist", 'id' : object_id, })
    
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
    try:
        obj = Task.objects.get(owner=user, id=object_id)
        result["id"] = obj.id
        result["joblist"] = obj.joblist.name
        result["schedule"] = obj.schedule
        result["owner"] = obj.owner
        result["state"] = obj.state
        result["source_file"] = os.path.basename(obj.source_file.name)
        result["notify"] = obj.notify
    except:
        result.update({ 'error' : "Task does not exist", 'id' : object_id, })
    
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
    
    try:
        obj = TaskHistory.objects.get(owner=user, id=object_id)
        result["id"] = obj.id
        result["joblist"] = obj.joblist
        result["owner"] = obj.owner
        result["state"] = obj.state
        result["starttime"] = obj.starttime
        result["endtime"] = obj.endtime
        if obj.outputdir:
            result["outputdir"] = [ '%svideos/%s/%s' % (MEDIA_URL,obj.outputdir,f) for f in os.listdir(VIDEO_ROOT+"/"+obj.outputdir)]
        else:
            result["outputdir"]=['No Files']
        result["log"] = obj.log
    except:
        result.update({ 'error' : "Task does not exist", 'id' : object_id, })

    return { 'history' : result }
    

def getHistories(user):
    result = {}
    result["histories"] = []
    histories = TaskHistory.objects.filter(owner=user)
    for history in histories:
        result["histories"].append(getHistoryDetail(user, history.id))
    return result


def setJob(request):
    obj = Job(owner=request.user)
    form = JobForm(request.POST, instance=obj)
    if form.is_valid(): 
        obj = form.save()
        return getJobDetail(request.user, obj.id)
    else:
        return {'job': {'error':"Job could not be created", } }
    

def editJob(request):
    try:
        obj = Job.objects.get(owner=request.user, id=request.POST['id'])
    except:
        return {'job': {'error':"Job does not exist", } }
    
    form = JobForm(request.POST, instance=obj)
    if form.is_valid(): 
        obj = form.save()
        return getJobDetail(request.user, obj.id)
    else:
        return {'job': {'error':"Job could not be modified", } }

def deleteJob(request):
    try:
        obj = Job.objects.get(owner=request.user, id=request.POST['id'])
    except:
        return {'job': {'error':"Job does not exist", } }
    obj.delete()
    return {'job': {'success':"Job deleted", } }

def setJoblist(request):
    obj = Joblist(owner=request.user)
    form = JoblistForm(request.user, request.POST, instance=obj)
    if form.is_valid(): 
        obj = form.save()
        return getJoblistDetail(request.user, obj.id)
    else:
        return {'joblist': {'error':"Joblist could not be created", } }

def editJoblist(request):
    try:
        obj = Joblist.objects.get(owner=request.user, id=request.POST['id'])
    except:
        return {'joblist': {'error':"Joblist does not exist", } }
    
    form = JoblistForm(request.user, request.POST, instance=obj)
    if form.is_valid(): 
        obj = form.save()
        return getJoblistDetail(request.user, obj.id)
    else:
        return {'joblist': {'error':"Joblist could not be modified", } }
    
def deleteJoblist(request):
    try:
        obj = Joblist.objects.get(owner=request.user, id=request.POST['id'])
    except:
        return {'joblist': {'error':"Joblist does not exist", } }
    obj.delete()
    return {'joblist': {'success':"Joblist deleted", } }

def setTask(request):
    obj = Task(owner=request.user)
    form = TaskForm(request.user, request.POST, request.FILES, instance=obj)
    if form.is_valid(): 
        obj = form.save()
        return getTaskDetail(request.user, obj.id)
    else:
        # [ item for item in form.errors.iteritems() ]
        # [('schedule', [u'Merci de ne pas planifier pour hier'])]
        return {'task': {'error':"Task could not be created", } }

def editTask(request):
    try:
        obj = Task.objects.get(owner=request.user, id=request.POST['id'])
    except:
        return {'joblist': {'error':"Joblist does not exist", } }
    
    form = TaskForm(request.user, request.POST, request.FILES, instance=obj)
    if form.is_valid(): 
        obj = form.save()
        return getTaskDetail(request.user, obj.id)
    else:
        return {'joblist': {'error':"Joblist could not be modified", } }
    

def deleteTask(request):
    try:
        obj = Task.objects.get(owner=request.user, id=request.POST['id'])
    except:
        return {'task': {'error':"Task does not exist", } }
    obj.delete()
    return {'task': {'success':"Task deleted", } }

