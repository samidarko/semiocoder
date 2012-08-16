import os, json
from django.db.models import Q
from django.http import HttpResponse
from django.views.generic.list_detail import object_detail
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from models import Job, Joblist, Task, TaskHistory
from semiocoder.encoder.forms import JobForm, JoblistForm, TaskForm
from semiocoder.settings import LOGIN_URL
from django.template.context import RequestContext
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.contrib import messages
from libs import getJobs, getTasks, getHistory

# TODO: documentation
# TODO: javascript pour tester les formaires ?
# TODO: centraliser les themes pour les plugin javascript


@login_required(login_url=LOGIN_URL)
def search(request): # TODO: revoir les champs de recherche
    """
    """
    query = request.GET.get('q', '')
    if query:
        qset = (
            Q(joblist__name__icontains=query) | Q(description__icontains=query)
        )
        results = Job.objects.filter(qset).distinct()
    else:
        results = []

    data =  { "results": results, "query": query }

    return render_to_response("search.html", data, context_instance=RequestContext(request))

# Delete
@login_required(login_url=LOGIN_URL)
def job_delete(request, object_id):

    if request.method == 'POST':
        obj = get_object_or_404(Job, pk=object_id, owner=request.user)
        obj.delete()
        msg = "The %(verbose_name)s was deleted." %  {"verbose_name": 'job'}
        messages.success(request, msg, fail_silently=True)
        return redirect("jobs")
    else:
        return render_to_response('encoder/confirm_delete.html', { 'element' : 'Job', 'title' : 'Job delete confirmation'}, context_instance=RequestContext(request))


@login_required(login_url=LOGIN_URL)
def joblist_delete(request, object_id):

    if request.method == 'POST':
        obj = get_object_or_404(Joblist, pk=object_id, owner=request.user)
        obj.delete()
        msg = "The %(verbose_name)s was deleted." %  {"verbose_name": 'joblist'}
        messages.success(request, msg, fail_silently=True)
        return redirect("joblists")
    else:
        return render_to_response('encoder/confirm_delete.html', { 'element' : 'Joblist', 'title' : 'Joblist delete confirmation'}, context_instance=RequestContext(request))


@login_required(login_url=LOGIN_URL)
def task_delete(request, object_id):

    if request.method == 'POST':
        obj = get_object_or_404(Task, pk=object_id, owner=request.user)
        if obj.state == 'W':
            obj.delete()
            msg = "The %(verbose_name)s was deleted." %  {"verbose_name": 'task'}
            messages.success(request, msg, fail_silently=True)
        else:
            msg = 'The %(verbose_name)s can not be deleted because state is already "Pending" or "Running".'  %  {"verbose_name": 'task'}
            messages.error(request, msg, fail_silently=True)
        return redirect("tasks")
    else:
        return render_to_response('encoder/confirm_delete.html', { 'element' : 'Task', 'title' : 'Task delete confirmation'}, context_instance=RequestContext(request))

# Update
@login_required(login_url=LOGIN_URL)
def job_update(request, object_id):
    

    obj = get_object_or_404(Job, pk=object_id, owner=request.user)

    data = { 'element': 'job', 'action' : reverse('job_edit', args=[ object_id,]), 'title' : 'Job edit', }

    if request.method == 'POST':
        form = JobForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            obj = form.save()
            msg = "The %(verbose_name)s was updated successfully." % {"verbose_name": data["element"], }
            messages.success(request, msg, fail_silently=True)
            return redirect('jobs')
    else:
        form = JobForm(instance=obj)

    data.update({'form' : form, })
    return render_to_response('encoder/encoding_form.html', data, context_instance=RequestContext(request))


@login_required(login_url=LOGIN_URL)
def joblist_update(request, object_id):

    obj = get_object_or_404(Joblist, pk=object_id, owner=request.user)
    
    data = { 'element': 'joblist', 'action' : reverse('joblist_edit', args=[ object_id,]), 'title' : 'Joblist edit', }

    if request.method == 'POST':
        form = JoblistForm(request.user, request.POST, request.FILES, instance=obj)
        if form.is_valid():
            obj = form.save()
            msg = "The %(verbose_name)s was updated successfully." % {"verbose_name": data["element"], }
            messages.success(request, msg, fail_silently=True)
            return redirect('joblists')
    else:
        form = JoblistForm(request.user, instance=obj)

    data.update({'form' : form, })
    return render_to_response('encoder/encoding_form.html', data, context_instance=RequestContext(request))
    
@login_required(login_url=LOGIN_URL)
def task_update(request, object_id):
    
    obj = get_object_or_404(Task, pk=object_id, owner=request.user)
    
    data = { 'element': 'task', 'action' : reverse('task_edit', args=[ object_id,]), 'title' : 'Task edit', }

    if request.method == 'POST':
        form = TaskForm(request.user, request.POST, request.FILES, instance=obj)
        if form.is_valid():
            obj = form.save()
            msg = "The %(verbose_name)s was updated successfully." % {"verbose_name": data["element"], }
            messages.success(request, msg, fail_silently=True)
            return redirect('tasks')
    else:
        form = TaskForm(request.user, instance=obj)

    data.update({'form' : form, })
    return render_to_response('encoder/encoding_form.html', data, context_instance=RequestContext(request))

    
# Create
@login_required(login_url=LOGIN_URL)
def job_create(request): # TODO: reprendre les messages des vues generiques pour coherence
    data = { 'element' : 'job', 'title' : "Ajout d'un job", 'action' : reverse('job_add'), }
    if request.method == 'POST':
        form = JobForm(request.POST, instance = Job(owner=request.user))
        if form.is_valid():
            form.save()
            msg = "The %(verbose_name)s was created successfully."  % {"verbose_name": data['element']}
            messages.success(request, msg, fail_silently=True)
            return redirect('jobs')
    else:
        form = JobForm()
    data.update({'form' : form, })
    return render_to_response('encoder/encoding_form.html', data, context_instance=RequestContext(request))


@login_required(login_url=LOGIN_URL)
def joblist_create(request):
    data = { 'element' : 'joblist', 'title' : "Ajout d'une joblist", 'action' : reverse('joblist_add'), }
    if request.method == 'POST':
        form = JoblistForm(request.user, request.POST, instance=Joblist(owner=request.user))
        if form.is_valid():
            form.save()
            msg = "The %(verbose_name)s was created successfully."  % {"verbose_name": data['element']}
            messages.success(request, msg, fail_silently=True)
            return redirect('joblists')
    else:
        form = JoblistForm(request.user)
    data.update({'form' : form, })
    return render_to_response('encoder/encoding_form.html', data, context_instance=RequestContext(request))


@login_required(login_url=LOGIN_URL)
def task_create(request): # TODO: empecher les dates anterieures
    data = { 'element' : 'task', 'title' : "Ajout d'une tache", 'action' : reverse('task_add'), }
    if request.method == 'POST':
        form = TaskForm(request.user, request.POST, request.FILES, instance = Task(owner=request.user))
        if form.is_valid():
            form.save()
            msg = "The %(verbose_name)s was created successfully." % {"verbose_name": data['element']}
            messages.success(request, msg, fail_silently=True)
            return redirect('tasks')
    else:
        form = TaskForm(request.user)
    data.update({'form' : form, })
    return render_to_response('encoder/encoding_form.html', data, context_instance=RequestContext(request))


# Object detail
@login_required(login_url=LOGIN_URL)
def job_detail(request, object_id):
    data = { 'element': 'job', 'id' : object_id, }
    return object_detail(request, Job.objects.filter(owner=request.user), object_id=object_id, template_name="encoder/job_detail.html", extra_context=data)
    

@login_required(login_url=LOGIN_URL)
def joblist_detail(request, object_id):
    data = { 'element': 'joblist', 'id' : object_id, 'title' : 'Detail du joblist', }
    return object_detail(request, Joblist.objects.filter(owner=request.user), object_id=object_id, template_name="encoder/joblist_detail.html", extra_context=data)
    
    
@login_required(login_url=LOGIN_URL)
def task_detail(request, object_id):
    data = { 'element': 'task', 'id' : object_id, 'title' : 'Detail du task', }
    return object_detail(request, Task.objects.filter(owner=request.user), object_id=object_id, template_name="encoder/task_detail.html", extra_context=data)
    
# Object list
@login_required(login_url=LOGIN_URL)
def job_list(request):
    return render_to_response("encoder/job.html", context_instance=RequestContext(request))

@login_required(login_url=LOGIN_URL)
def joblist_list(request): # TODO: ajouter le champ de recherche jstree + bouton pour fermer tous les noeuds
    return render_to_response("encoder/joblist.html", { 'joblist_list' : Joblist.objects.filter(owner=request.user), }, context_instance=RequestContext(request))

@login_required(login_url=LOGIN_URL)
def task_list(request):
    return render_to_response("encoder/task.html", context_instance=RequestContext(request))

# Task specific
@login_required(login_url=LOGIN_URL)
def task_history(request):
    return render_to_response("encoder/task_history.html", context_instance=RequestContext(request))

@login_required(login_url=LOGIN_URL)
def task_log(request, object_id):
    return render_to_response('encoder/task_log.html', { 'th' : get_object_or_404(TaskHistory, pk=object_id, owner=request.user), }, context_instance=RequestContext(request))

@login_required(login_url=LOGIN_URL)
def task_output(request, object_id):
    
    th = get_object_or_404(TaskHistory, pk=object_id, owner=request.user)

    try:
        files = os.listdir('media/videos/'+th.outputdir)
    except:
        return redirect('task_history')
    
    if request.method == 'POST':
        selectedfiles = request.POST.getlist('outputfiles') 
        # On supprime les fichiers selectionnes
        for f in selectedfiles:
            filename = os.path.basename(f)
            try:
                os.remove(f[1:])
                msg = '%s deleted' % filename
                messages.success(request, msg, fail_silently=True)
            except OSError:
                msg = 'impossible to delete %s ' % filename
                messages.error(request, msg, fail_silently=True)
        # si il n y a plus de fichiers on supprime le repertoire
        if len(selectedfiles) == len(files):
            os.rmdir('media/videos/'+th.outputdir)
            th.outputdir = ""
            th.save()
            return redirect('task_history')
        return redirect('task_output', object_id)
    else:
        
        data = { 'files': files, 'th': th, 'outputfiles' : files }
        return render_to_response('encoder/output_files.html', data, context_instance=RequestContext(request))


taskcol = [ "joblist", "schedule", "state", "notify", ]

@login_required(login_url=LOGIN_URL)
def task_data(request):
    
    try:
        iDisplayStart = int(request.GET["iDisplayStart"])
        iDisplayLength = int(request.GET["iDisplayLength"])
        sSearch = request.GET["sSearch"]
        sEcho = int(request.GET["sEcho"])
        try:
            column = int(request.GET["iSortCol_0"])
            ascending = (request.GET["sSortDir_0"] == "asc")
        except:
            column = 0
            ascending = True
    except:
        pass

    total_tasks, filtered_tasks, tasks = getTasks(user=request.user, first_id=iDisplayStart, 
                         last_id=iDisplayStart + iDisplayLength - 1,
                         search_str=sSearch,
                         sort_by=taskcol[column], 
                         asc=ascending)

    json_data = {
        "sEcho" : sEcho,
        "iTotalRecords" : total_tasks,
        "iTotalDisplayRecords" : filtered_tasks,
        "aaData" : tasks
    }

    return HttpResponse(json.dumps(json_data))


hiscol = [ "joblist", "state", "starttime", "endtime", ]

@login_required(login_url=LOGIN_URL)
def task_history_data(request):
    
    try:
        iDisplayStart = int(request.GET["iDisplayStart"])
        iDisplayLength = int(request.GET["iDisplayLength"])
        sSearch = request.GET["sSearch"]
        sEcho = int(request.GET["sEcho"])
        try:
            column = int(request.GET["iSortCol_0"])
            ascending = (request.GET["sSortDir_0"] == "asc")
        except:
            column = 0
            ascending = True
    except:
        pass

    total_tasks, filtered_tasks, tasks = getHistory(user=request.user, first_id=iDisplayStart, 
                         last_id=iDisplayStart + iDisplayLength - 1,
                         search_str=sSearch,
                         sort_by=hiscol[column], 
                         asc=ascending)

    json_data = {
        "sEcho" : sEcho,
        "iTotalRecords" : total_tasks,
        "iTotalDisplayRecords" : filtered_tasks,
        "aaData" : tasks
    }

    return HttpResponse(json.dumps(json_data))

# Job specific

jobcol = [ "name", "description", "encoder", "extension", ]

@login_required(login_url=LOGIN_URL)
def job_data(request):
    
    try:
        iDisplayStart = int(request.GET["iDisplayStart"])
        iDisplayLength = int(request.GET["iDisplayLength"])
        sSearch = request.GET["sSearch"]
        sEcho = int(request.GET["sEcho"])
        try:
            column = int(request.GET["iSortCol_0"])
            ascending = (request.GET["sSortDir_0"] == "asc")
        except:
            column = 0
            ascending = True
    except:
        pass

    total_jobs, filtered_jobs, jobs = getJobs(user=request.user, first_id=iDisplayStart, 
                         last_id=iDisplayStart + iDisplayLength - 1,
                         search_str=sSearch,
                         sort_by=jobcol[column], 
                         asc=ascending)

    json_data = {
        "sEcho" : sEcho,
        "iTotalRecords" : total_jobs,
        "iTotalDisplayRecords" : filtered_jobs,
        "aaData" : jobs
    }

    return HttpResponse(json.dumps(json_data))

# Joblist specific
@login_required(login_url=LOGIN_URL)
def joblist_jobs_data(request, object_id):
    
    joblist = get_object_or_404(Joblist, pk=object_id, owner=request.user)
    json_job_list = []
    
    if joblist.owner == request.user:
        for j in joblist.job.select_related():
            job = {}
            Id = "_%d_%d" % (int(object_id), j.id)
            url = reverse('job_detail', args = [ j.id, ])
            title = '<b>%s</b>' % (j.name)
            job["data"] = { "title" : title, "attr" : { "href" : url } }
            job["attr"] = { "id" : Id , "rel" : "job" , }
            job["state"] = "closed"
            json_job_list.append(job)
        return HttpResponse(json.dumps(json_job_list))
    else:
        return HttpResponse(json.dumps(json_job_list))


@login_required(login_url=LOGIN_URL)
def joblist_job_detail_data(request, object_id):
    
    job = get_object_or_404(Job, pk=object_id, owner=request.user)
    
    if job.owner == request.user:
        json_job_detail = [
                        { 'data' : '<b>encodeur</b> : <i>%s</i>' % job.encoder.name, 'attr' : { "rel" : "job_detail" , }, 'state' : 'closed', },
                        { 'data' : '<b>extension</b> : <i>%s</i>' % job.extension.name, 'attr' : { "rel" : "job_detail" , }, 'state' : 'closed', },
                        { 'data' : '<b>options</b> : <i>%s</i>' % job.options, 'attr' : { "rel" : "job_detail" , }, 'state' : 'closed', },
                        ]
        return HttpResponse(json.dumps(json_job_detail))
    else:
        return HttpResponse(json.dumps([]))




