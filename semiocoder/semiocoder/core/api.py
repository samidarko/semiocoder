import os, json, datetime
from django.contrib.auth import views
from semiocoder.settings import VIDEO_ROOT, MEDIA_URL
from semiocoder.encoder.models import Encoder, Job, Joblist, Task, TaskHistory, Extension
from semiocoder.encoder.forms import TaskForm, JobForm, JoblistForm

from xml.dom.minidom import getDOMImplementation

def dict_to_xml(doc, el, values):

    for k, v in values.iteritems():
        
        if isinstance (v, list):
            child = doc.createElement(k)
            for item in v:
                object_type = item.keys()[0]
                child.appendChild(dict_to_xml(doc, doc.createElement(object_type), item[object_type]))
            el.appendChild(child)
        elif isinstance (v, dict):
            el.appendChild(dict_to_xml(doc, doc.createElement(k), v))
        else:
            child = doc.createElement(k)
            child.appendChild(doc.createTextNode(unicode(v)))
            el.appendChild(child)
    
    return el
    

def formatResult(formatting, result):

    if formatting == "json":
        return json.dumps(result)
    elif formatting == "xml":

        impl = getDOMImplementation()
        object_type = result.keys()[0]
        doc = impl.createDocument(None, object_type, None)
        root = doc.documentElement
        values = result[object_type]
        
        if isinstance (values, dict):
            
            doc.appendChild(dict_to_xml(doc, root, values))
            
        elif isinstance (values, list):

            for el in values:
                object_type = el.keys()[0]
                child = doc.createElement(object_type)
                root.appendChild(dict_to_xml(doc, child, el[object_type]))
            doc.appendChild(root)
        
        return doc


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
        result["options"] = obj.options
        result.update(getEncoderDetail(user, obj.encoder.id))
        result.update(getExtensionDetail(user, obj.extension.id))

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
        result["jobs"] =  [ getJobDetail(user, job.id) for job in obj.job.select_related()]
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
        result["schedule"] = obj.schedule
        result["owner"] = obj.owner
        result["state"] = obj.state
        result["source_file"] = os.path.basename(obj.source_file.name)
        result["notify"] = obj.notify
        result.update(getJoblistDetail(user, obj.joblist.id))
        
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
            result["outputdir"] = [ ]
            for filename in os.listdir(VIDEO_ROOT+"/"+obj.outputdir):
                result["outputdir"].append({'file' : { 'name' : filename, 'path' : '%svideos/%s/%s' % (MEDIA_URL,obj.outputdir,filename), } } )
                
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
        message = {'job': {'error':{ } } }
        for k, v in form.errors.iteritems():
            message['job']['error'][k] = v[0]
        return message
    

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
        message = {'job': {'error':{ } } }
        for k, v in form.errors.iteritems():
            message['job']['error'][k] = v[0]
        return message

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
        message = {'joblist': {'error':{ } } }
        for k, v in form.errors.iteritems():
            message['job']['error'][k] = v[0]
        return message

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
        message = {'joblist': {'error':{ } } }
        for k, v in form.errors.iteritems():
            message['job']['error'][k] = v[0]
        return message
    
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
        message = {'task': {'error':{ } } }
        for k, v in form.errors.iteritems():
            message['job']['error'][k] = v[0]
        return message

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
        message = {'task': {'error':{ } } }
        for k, v in form.errors.iteritems():
            message['job']['error'][k] = v[0]
        return message
    

def deleteTask(request):
    try:
        obj = Task.objects.get(owner=request.user, id=request.POST['id'])
    except:
        return {'task': {'error':"Task does not exist", } }
    obj.delete()
    return {'task': {'success':"Task deleted", } }


def deleteFiles(request):
    try:
        obj = TaskHistory.objects.get(owner=request.user, id=request.POST['id'])
    except:
        return {'task': {'error':"TaskHistory does not exist", } }
    try:
        if obj.outputdir:
            video_path = os.path.join(VIDEO_ROOT, obj.outputdir).replace('\\','/')
            files = os.listdir(video_path)
            if files:
                for filename in files:
                    os.remove(video_path+'/'+filename)
                obj.outputdir = ''
                obj.save()
        else:
            return {'task': {'error':"No files to delete", } }
    except:
        return {'task': {'error':"Files not deleted : an error has occured", } }
    
    return {'taskhistory': {'success':"TaskHistory files deleted", } }

