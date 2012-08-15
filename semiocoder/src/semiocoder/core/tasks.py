import os, subprocess, datetime
from celery import task
from celery.task import periodic_task
from celery.task.schedules import crontab
from semiocoder.encoder.models import Task, TaskHistory

# TODO: verifier que le binaire est bien appelé depuis exe
# TODO: tester avec libav

@task
def taskLaucher(t):
    t.state = 'R'
    t.save()
    th = TaskHistory(joblist = t.joblist.name, owner = t.owner, starttime = datetime.datetime.now(), outputdir = t.source_file.url.split('/')[3])
    log = ""; ret = 0
    for job in t.joblist.job.select_related():
        # Creation de la log
        log += "===== Log %s =============================\n\n" % (job.name)
        
        # Preparation des params pour subprocess
        args = [ job.encoder.name, ]                                                    # encodeur
        if job.encoder.inputflag: args.append(job.encoder.inputflag)                    # option du fichier en entree
        args.append(t.source_file.url[1:])                                              # le chemin du fichier en entree
        args.extend(job.options.split())                                                # les options specifiees dans le job        
        if job.encoder.outputflag: args.append(job.encoder.outputflag)                  # option du fichier en sortie
        output_filename = datetime.datetime.now().strftime("%H%M%S")+'-'+os.path.splitext(os.path.basename(t.source_file.url))[0]+'-'+job.name+'.'+job.extension.name
        args.append('/'.join(t.source_file.url.split('/')[1:4]+[ output_filename, ]))   # chemin du fichier en sortie
        
        # Execution
        cmdp = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        cmdout,cmderr =  cmdp.communicate()
        ret += cmdp.wait()
        log += cmdout
        if cmderr: log += "<p><FONT COLOR=RED>Error log :\n" + cmderr + "</FONT></p>"
        log += '\n\n'
        
    if ret == 0:
        th.state = "C"
    else:
        th.state = "F"
        
    th.log = log
    th.endtime = datetime.datetime.now()
    th.save()
    
    # notification
#    if t.notify:
#        notify(level=t.notify, history=th.id)
        
    # suppression de la tache
    t.source_file.delete()
    t.delete()
    
    return "code retour : %d" % ret
        
        
        

@periodic_task(run_every=crontab(minute="*/5"))
def taskScheduler():
    
    tasks = Task.objects.filter(schedule__lte=datetime.datetime.now()).order_by('schedule')
    counter = 0
    for t in tasks:
        if t.state == 'W':
            t.state = 'P'
            t.save()
            taskLaucher.delay(t)
            counter += 1
    
    pluralize = 'tasks' if counter > 1 else 'task'

    return "%d %s launched" % (counter,pluralize)

    