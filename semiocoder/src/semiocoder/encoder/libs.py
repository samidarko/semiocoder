from django.db.models import Q
from django.core.urlresolvers import reverse
from semiocoder.settings import STATIC_URL
from models import Job, Task, TaskHistory

def getJobs(user, first_id, last_id, search_str=None, sort_by="name", asc=True):
    
    sort_col = "%s"
    if not asc:
        sort_col = "-" + sort_col
    sort_col = sort_col % sort_by
    
    jobs = Job.objects.filter(owner=user).order_by(sort_col)
    
    if search_str:
        total_jobs = len(jobs)
        search_args = Q(name__icontains=search_str)
        
        jobs = jobs.filter(search_args)
        filtered_jobs = len(jobs)
    else:
        total_jobs = filtered_jobs = len(jobs)
    jobs = jobs[first_id:last_id]
    
    job_list = []
    for j in jobs:
        job = [ '<a href=%s>%s</a>' % (reverse('job_detail', args = [ j.id, ]), j.name),
                 j.description, j.encoder.name, j.extension.name,
                ]
        job_list.append(job)
    return total_jobs, filtered_jobs, job_list


def getTasks(user, first_id, last_id, search_str=None, sort_by="name", asc=True):
    
    sort_col = "%s"
    if not asc:
        sort_col = "-" + sort_col
    sort_col = sort_col % sort_by
    
    tasks = Task.objects.filter(owner=user).order_by(sort_col)
    
    if search_str:
        total_tasks = len(tasks)
        search_args = Q(schedule__icontains=search_str)
        
        tasks = tasks.filter(search_args)
        filtered_tasks = len(tasks)
    else:
        total_tasks = filtered_tasks = len(tasks)
    tasks = tasks[first_id:last_id]
    
    tasks_list = []
    for t in tasks:
        notify = "enabled" if t.notify else "disabled"
        state = "waiting"
        if t.state == 'P':
            state = "pending"
        elif t.state == 'R':
            state = "running"
        task = [ 
                '<a href=%s>%s</a>' % (reverse('task_detail', args = [t.id, ]), "task %d" % t.id),
                '<a href=%s>%s</a>' % (reverse('joblist_detail', args = [t.joblist.id, ]), t.joblist.name),
                t.schedule.strftime('%Y-%m-%d %H:%M:%S'),
                state,
                notify,
                '<a href=%s><img src=%simages/edit.png></a>' % (reverse('task_edit', args = [ t.id, ]), STATIC_URL),
                '<a href=%s><img src=%simages/delete.png></a>' % (reverse('task_delete', args = [ t.id, ],), STATIC_URL),
             ]
        tasks_list.append(task)
    return total_tasks, filtered_tasks, tasks_list


def getHistory(user, first_id, last_id, search_str=None, sort_by="name", asc=True):
    
    sort_col = "%s"
    if not asc:
        sort_col = "-" + sort_col
    sort_col = sort_col % sort_by
    
    tasks = TaskHistory.objects.filter(owner=user).order_by(sort_col)
    
    if search_str:
        total_tasks = len(tasks)
        search_args = Q(schedule__icontains=search_str)
        
        tasks = tasks.filter(search_args)
        filtered_tasks = len(tasks)
    else:
        total_tasks = filtered_tasks = len(tasks)
    tasks = tasks[first_id:last_id]
    
    tasks_list = []
    for t in tasks:
        if t.outputdir:
            outputdir = '<a href="%s">output</a>' % (reverse('task_output', args = [ t.id, ]))
        else:
            outputdir = "No Files"
        state = "completed" if t.state == 'C' else "failed"
        task = [ t.joblist,
            state,
            t.starttime.strftime('%Y-%m-%d %H:%M:%S'),
            t.endtime.strftime('%Y-%m-%d %H:%M:%S'),
            outputdir,
            '<a href="%s">log</a>' % (reverse('task_log', args = [ t.id, ])),
             ]
        tasks_list.append(task)
    return total_tasks, filtered_tasks, tasks_list






