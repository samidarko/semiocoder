# -*- coding: utf-8 -*-
"""
.. module:: views
   :platform: Unix, Windows
   :synopsis: Module des vues de l'encodeur

.. moduleauthor:: Samuel Darko <samidarko@gmail.com>

"""
import os, json, shutil
from django.db.models import Q
from django.http import HttpResponse
from django.views.generic.list_detail import object_detail
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from models import Job, Joblist, Task, TaskHistory
from semiocoder.encoder.forms import JobForm, JoblistForm, TaskForm
from semiocoder.settings import LOGIN_URL, VIDEO_ROOT
from django.template.context import RequestContext
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.contrib import messages
from django.utils.translation import ugettext
from libs import getJobs, getTasks, getHistory
from django.http import Http404

# TODO: doctest
# TODO: Faire les tests unitaires
# TODO: ajouter la recherche dans les taches (date)
# TODO: securiser iptable ?
# TODO: controle de l'espace (faire une partition separee au niveau du serveur)
# TODO: ameliorer les champs de recherche des datatable
# TODO: revoir le nom des fichiers en sortie
# TODO: control client : verifier la longueur des champs + options exclure le nom du fichier a la fin
# TODO: dans le formulaire de selection de fichier ajouter une case "select all"

@login_required(login_url=LOGIN_URL)
def search(request):
    """Affichage du formulaire de recherche du site
    
    :param request: Paramètres de la requête HTTP
    :type request: HttpRequest
    
    :returns: HttpResponse
    """
    query = request.POST.get('q', '')
    results = []
    if query:
        results.extend(Joblist.objects.filter(Q(owner__exact=request.user),Q(name__icontains=query) | Q(description__icontains=query)).distinct())
        results.extend(Job.objects.filter(Q(owner__exact=request.user),Q(name__icontains=query) | Q(description__icontains=query)).distinct())
        results.extend(Task.objects.filter(Q(owner__exact=request.user),Q(joblist__name__icontains=query)).distinct())
        results.sort()
    data =  { "results": results, "query": query }

    return render_to_response("search.html", data, context_instance=RequestContext(request))

# Delete
@login_required(login_url=LOGIN_URL)
def job_delete(request, object_id):
    """Supression d'un objet job
    
    :param request: Paramètres de la requête HTTP
    :type request: HttpRequest
    :param object_id: Identifiant de l'objet job à supprimer
    :type object_id: int
    
    :returns: HttpResponse
    """
    obj = get_object_or_404(Job, pk=object_id, owner=request.user)
    if request.method == 'POST':
        obj.delete()
        msg = ugettext("The %(verbose_name)s was deleted.") %  {"verbose_name": 'job'}
        messages.success(request, msg, fail_silently=True)
        return redirect("jobs")
    else:
        return render_to_response('encoder/confirm_delete.html', { 'element' : 'job', 'obj' : obj,}, context_instance=RequestContext(request))


@login_required(login_url=LOGIN_URL)
def joblist_delete(request, object_id):
    """Supression d'un objet joblist
    
    :param request: Paramètres de la requête HTTP
    :type request: HttpRequest
    :param object_id: Identifiant de l'objet joblist à supprimer
    :type object_id: int
    
    :returns: HttpResponse
    """
    obj = get_object_or_404(Joblist, pk=object_id, owner=request.user)
    if request.method == 'POST':
        obj.delete()
        msg = ugettext("The %(verbose_name)s was deleted.") %  {"verbose_name": 'joblist'}
        messages.success(request, msg, fail_silently=True)
        return redirect("joblists")
    else:
        return render_to_response('encoder/confirm_delete.html', { 'element' : 'joblist', 'obj' : obj,}, context_instance=RequestContext(request))


@login_required(login_url=LOGIN_URL)
def task_delete(request, object_id):
    """Supression d'un objet task
    
    :param request: Paramètres de la requête HTTP
    :type request: HttpRequest
    :param object_id: Identifiant de l'objet task à supprimer
    :type object_id: int
    
    :returns: HttpResponse
    """
    obj = get_object_or_404(Task, pk=object_id, owner=request.user)
    if request.method == 'POST':
        if obj.state == 'W':
            obj.delete()
            msg = ugettext("The %(verbose_name)s was deleted.") %  {"verbose_name": 'task'}
            messages.success(request, msg, fail_silently=True)
        else:
            msg = 'The %(verbose_name)s can not be deleted because state is already "Pending" or "Running".'  %  {"verbose_name": 'task'}
            messages.error(request, msg, fail_silently=True)
        return redirect("tasks")
    else:
        return render_to_response('encoder/confirm_delete.html', { 'element' : 'task', 'obj' : obj,}, context_instance=RequestContext(request))

# Update
@login_required(login_url=LOGIN_URL)
def job_update(request, object_id):
    """Mise à jour d'un objet job
    
    :param request: Paramètres de la requête HTTP
    :type request: HttpRequest
    :param object_id: Identifiant de l'objet job à mettre à jour
    :type object_id: int
    
    :returns: HttpResponse
    """

    obj = get_object_or_404(Job, pk=object_id, owner=request.user)

    data = { 'element': 'job', 'action' : reverse('job_edit', args=[ object_id,]), 'title' : 'Job edit', }

    if request.method == 'POST':
        form = JobForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            obj = form.save()
            msg = ugettext("The %(verbose_name)s was updated successfully.") % {"verbose_name": data["element"], }
            messages.success(request, msg, fail_silently=True)
            return redirect('jobs')
    else:
        form = JobForm(instance=obj)

    data.update({'form' : form, })
    return render_to_response('encoder/encoding_edit_form.html', data, context_instance=RequestContext(request))


@login_required(login_url=LOGIN_URL)
def joblist_update(request, object_id):
    """Mise à jour d'un objet joblist
    
    :param request: Paramètres de la requête HTTP
    :type request: HttpRequest
    :param object_id: Identifiant de l'objet joblist à mettre à jour
    :type object_id: int
    
    :returns: HttpResponse
    """

    obj = get_object_or_404(Joblist, pk=object_id, owner=request.user)
    
    data = { 'element': 'joblist', 'action' : reverse('joblist_edit', args=[ object_id,]), 'title' : 'Joblist edit', }

    if request.method == 'POST':
        form = JoblistForm(request.user, request.POST, request.FILES, instance=obj)
        if form.is_valid():
            obj = form.save()
            msg = ugettext("The %(verbose_name)s was updated successfully.") % {"verbose_name": data["element"], }
            messages.success(request, msg, fail_silently=True)
            return redirect('joblists')
    else:
        form = JoblistForm(request.user, instance=obj)

    data.update({'form' : form, })
    return render_to_response('encoder/encoding_edit_form.html', data, context_instance=RequestContext(request))
    
@login_required(login_url=LOGIN_URL)
def task_update(request, object_id):
    """Mise à jour d'un objet task
    
    :param request: Paramètres de la requête HTTP
    :type request: HttpRequest
    :param object_id: Identifiant de l'objet task à mettre à jour
    :type object_id: int
    
    :returns: HttpResponse
    """
    
    obj = get_object_or_404(Task, pk=object_id, owner=request.user)
    
    data = { 'element': 'task', 'action' : reverse('task_edit', args=[ object_id,]), 'title' : 'Task edit', }

    if request.method == 'POST':
        form = TaskForm(request.user, request.POST, request.FILES, instance=obj)
        if form.is_valid():
            obj = form.save()
            msg = ugettext("The %(verbose_name)s was updated successfully.") % {"verbose_name": data["element"], }
            messages.success(request, msg, fail_silently=True)
            return redirect('tasks')
    else:
        form = TaskForm(request.user, instance=obj)

    data.update({'form' : form, })
    return render_to_response('encoder/encoding_edit_form.html', data, context_instance=RequestContext(request))

    
# Create
@login_required(login_url=LOGIN_URL)
def job_create(request):
    """Création d'un objet job
    
    :param request: Paramètres de la requête HTTP
    :type request: HttpRequest
    
    :returns: HttpResponse
    """
    
    data = { 'element' : 'job', 'title' : "Ajout d'un job", 'action' : reverse('job_add'), }
    if request.method == 'POST':
        form = JobForm(request.POST, instance = Job(owner=request.user))
        if form.is_valid():
            form.save()
            msg = ugettext("The %(verbose_name)s was created successfully.")  % {"verbose_name": data['element']}
            messages.success(request, msg, fail_silently=True)
            return redirect('jobs')
    else:
        form = JobForm()
    data.update({'form' : form, })
    return render_to_response('encoder/encoding_form.html', data, context_instance=RequestContext(request))


@login_required(login_url=LOGIN_URL)
def joblist_create(request):
    """Création d'un objet joblist
    
    :param request: Paramètres de la requête HTTP
    :type request: HttpRequest
    
    :returns: HttpResponse
    """
    
    data = { 'element' : 'joblist', 'title' : "Ajout d'une joblist", 'action' : reverse('joblist_add'), }
    if request.method == 'POST':
        form = JoblistForm(request.user, request.POST, instance=Joblist(owner=request.user))
        if form.is_valid():
            form.save()
            msg = ugettext("The %(verbose_name)s was created successfully.")  % {"verbose_name": data['element']}
            messages.success(request, msg, fail_silently=True)
            return redirect('joblists')
    else:
        form = JoblistForm(request.user)
    data.update({'form' : form, })
    return render_to_response('encoder/encoding_form.html', data, context_instance=RequestContext(request))


@login_required(login_url=LOGIN_URL)
def task_create(request):
    """Création d'un objet task
    
    :param request: Paramètres de la requête HTTP
    :type request: HttpRequest
    
    :returns: HttpResponse
    """
    
    data = { 'element' : 'task', 'title' : "Ajout d'une tache", 'action' : reverse('task_add'), }
    if request.method == 'POST':
        form = TaskForm(request.user, request.POST, request.FILES, instance = Task(owner=request.user))
        if form.is_valid():
            form.save()
            msg = ugettext("The %(verbose_name)s was created successfully.") % {"verbose_name": data['element']}
            messages.success(request, msg, fail_silently=True)
            return redirect('tasks')
    else:
        form = TaskForm(request.user)
    data.update({'form' : form, })
    return render_to_response('encoder/encoding_form.html', data, context_instance=RequestContext(request))


# Object detail
@login_required(login_url=LOGIN_URL)
def job_detail(request, object_id):
    """Affichages des détails d'un objet job
    
    :param request: Paramètres de la requête HTTP
    :type request: HttpRequest
    :param object_id: Identifiant de l'objet job à afficher
    :type object_id: int
    
    :returns: HttpResponse
    """
    
    data = { 'element': 'job', 'id' : object_id, }
    return object_detail(request, Job.objects.filter(owner=request.user), object_id=object_id, template_name="encoder/job_detail.html", extra_context=data)
    

@login_required(login_url=LOGIN_URL)
def joblist_detail(request, object_id):
    """Affichages des détails d'un objet joblist
    
    :param request: Paramètres de la requête HTTP
    :type request: HttpRequest
    :param object_id: Identifiant de l'objet joblist à afficher
    :type object_id: int
    
    :returns: HttpResponse
    """
    
    data = { 'element': 'joblist', 'id' : object_id, 'title' : 'Detail du joblist', }
    return object_detail(request, Joblist.objects.filter(owner=request.user), object_id=object_id, template_name="encoder/joblist_detail.html", extra_context=data)
    
    
@login_required(login_url=LOGIN_URL)
def task_detail(request, object_id):
    """Affichages des détails d'un objet task
    
    :param request: Paramètres de la requête HTTP
    :type request: HttpRequest
    :param object_id: Identifiant de l'objet task à afficher
    :type object_id: int
    
    :returns: HttpResponse
    """
    
    data = { 'element': 'task', 'id' : object_id, 'title' : 'Detail du task', }
    return object_detail(request, Task.objects.filter(owner=request.user), object_id=object_id, template_name="encoder/task_detail.html", extra_context=data)
    
# Object list
@login_required(login_url=LOGIN_URL)
def job_list(request):
    """Affichages de la liste des objets job
    
    :param request: Paramètres de la requête HTTP
    :type request: HttpRequest
    
    :returns: HttpResponse
    """
    
    return render_to_response("encoder/job.html", context_instance=RequestContext(request))

@login_required(login_url=LOGIN_URL)
def joblist_list(request): # TODO: ajouter le champ de recherche jstree + bouton pour fermer tous les noeuds
    """Affichages de la liste des objets joblist
    
    :param request: Paramètres de la requête HTTP
    :type request: HttpRequest
    
    :returns: HttpResponse
    """
    
    return render_to_response("encoder/joblist.html", { 'joblist_list' : Joblist.objects.filter(owner=request.user), }, context_instance=RequestContext(request))

@login_required(login_url=LOGIN_URL)
def task_list(request):
    """Affichages de la liste des objets task
    
    :param request: Paramètres de la requête HTTP
    :type request: HttpRequest
    
    :returns: HttpResponse
    """
    return render_to_response("encoder/task.html", context_instance=RequestContext(request))

# Task specific
@login_required(login_url=LOGIN_URL)
def task_history(request):
    """Affichages de l'historique des objets tâches
    
    :param request: Paramètres de la requête HTTP
    :type request: HttpRequest
    
    :returns: HttpResponse
    """
    return render_to_response("encoder/task_history.html", context_instance=RequestContext(request))

@login_required(login_url=LOGIN_URL)
def task_log(request, object_id):
    """Affichages de la log d'une tâche
    
    :param request: Paramètres de la requête HTTP
    :type request: HttpRequest
    :param object_id: Identifiant de l'objet historique de tâche à afficher
    :type object_id: int
    
    :returns: HttpResponse
    """
    return render_to_response('encoder/task_log.html', { 'th' : get_object_or_404(TaskHistory, pk=object_id, owner=request.user), }, context_instance=RequestContext(request))

@login_required(login_url=LOGIN_URL)
def task_output(request, object_id):
    """Affichages de la sortie (fichiers générés) d'une tâche
    
    :param request: Paramètres de la requête HTTP
    :type request: HttpRequest
    :param object_id: Identifiant de l'objet historique de tâche à afficher
    :type object_id: int
    
    :returns: HttpResponse
    """
    
    th = get_object_or_404(TaskHistory, pk=object_id, owner=request.user)

    try:
        video_path = os.path.join(VIDEO_ROOT, th.outputdir).replace('\\','/')
        files = os.listdir(video_path)
    except:
        raise Http404()
    
    if request.method == 'POST':
        selectedfiles = request.POST.getlist('outputfiles') 
        # On supprime les fichiers selectionnes
        for f in selectedfiles:
            filename = os.path.basename(f)
            try:
                os.remove(video_path+'/'+filename)
                msg = ugettext("The %(verbose_name)s was deleted.") %  {"verbose_name": 'fichier %s' % filename}
                messages.success(request, msg, fail_silently=True)
            except OSError:
                msg = 'impossible to delete %s ' % filename
                messages.error(request, msg, fail_silently=True)
        # si il n y a plus de fichiers on supprime le repertoire
        if len(selectedfiles) == len(files):
            shutil.rmtree(video_path)
            th.outputdir = ''
            th.save()
            return redirect('task_history')
        return redirect('task_output', object_id)
    else:
        
        data = { 'files': files, 'th': th, 'outputfiles' : files }
        return render_to_response('encoder/output_files.html', data, context_instance=RequestContext(request))


taskcol = [ "joblist", "schedule", "state", "notify", ]

@login_required(login_url=LOGIN_URL)
def task_data(request):
    """Renvoi les données nécéssaires à l'affichage du tableau (plugin dataTable) pour la liste des tâches en format JSON
    
    :param request: Paramètres de la requête HTTP
    :type request: HttpRequest
    
    :returns: HttpResponse
    """
    
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
    """Renvoi les données nécéssaires à l'affichage du tableau (plugin dataTable) pour la liste des objets historiques de tâche en format JSON
    
    :param request: Paramètres de la requête HTTP
    :type request: HttpRequest
    
    :returns: HttpResponse
    """
    
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
    """Renvoi les données nécéssaires à l'affichage du tableau (plugin dataTable) pour la liste des jobs en format JSON
    
    :param request: Paramètres de la requête HTTP
    :type request: HttpRequest
    
    :returns: HttpResponse
    """
    
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
    """Renvoi les données nécéssaires à l'arborescence joblist (plugin jsTree) pour le contenu des jobs d'un joblist
    
    :param request: Paramètres de la requête HTTP
    :type request: HttpRequest
    
    :returns: HttpResponse
    """
    
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
    """Renvoi les données nécéssaires à l'arborescence joblist (plugin jsTree) pour le détail d'un job contenu d'un joblist
    
    :param request: Paramètres de la requête HTTP
    :type request: HttpRequest
    
    :returns: HttpResponse
    """
    
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




