from xml.dom.minidom import Document
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from semiocoder.settings import LOGIN_URL
#from semiocoder.core.api import getEncoders, getJobDetail, getJoblistDetail, getJoblists, getJobs, getTaskDetail, getTasks, getHistoryDetail
#from semiocoder.core.api import formatResult, getHistories, getEncoderDetail, setJob, setJoblist, setTask, login, logout, getExtensions, getExtensionDetail
from semiocoder.core.api import *

@login_required(login_url=LOGIN_URL)
def api(request):
    if request.method == 'GET':
        if "format" in request.GET:
            mimetype = request.GET["format"]
            if mimetype not in ['xml', 'json']: mimetype = 'xml'
        else:
            mimetype = 'xml'
        if "action" in request.GET:
            
            action = request.GET["action"]
            
            fnGetNoArg = { "getencoders": getEncoders, "getjobs":  getJobs, "getjoblists": getJoblists, "gettasks": getTasks,
                           "gethistories": getHistories, "getextensions": getExtensions, "logout": logout, }
            
            fnGetOneArg = { "getencoderdetail": getEncoderDetail, "getjobdetail" : getJobDetail, "getjoblistdetail": getJoblistDetail,
                            "gettaskdetail": getTaskDetail, "gethistorydetail": getHistoryDetail, "getextensiondetail" : getExtensionDetail,
                           }
            
            if action in fnGetNoArg:
                try:
                    result = formatResult(mimetype, fnGetNoArg[action](request.user))
                except:
                    result = "unknown error"
            elif action in fnGetOneArg:
                if "id" in request.GET:
                    try:
                        result = formatResult(mimetype, fnGetOneArg[action](request.user, request.GET['id']))
                    except:
                        result = "unknown error"
                else:
                    result = "id parameter missing"
            else:
                result = "unknown action"
                    
            if isinstance(result, Document):
                return HttpResponse(result.toprettyxml(), mimetype="text/xml")
            else:
                return HttpResponse(result)
        else:
            return render_to_response('api/api_help.html', context_instance=RequestContext(request))
        
    elif  request.method == 'POST':
        
        if "format" in request.POST:
            mimetype = request.POST["format"]
            if mimetype not in ['xml', 'json']: mimetype = 'xml'
        else:
            mimetype = 'xml'
            
        if "action" in request.POST:
            
            action = request.POST["action"]
            
            fnPost = { "setjob":  setJob, "editjob": editJob, 'deletejob': deleteJob, 
                      "setjoblist":  setJoblist, 'editjoblist': editJoblist, 'deletejoblist': deleteJoblist,
                      "settask" : setTask, 'edittask' : editTask, 'deletetask' : deleteTask, "login" : login, }
        
            if action in fnPost:
                try:
                    result = formatResult(mimetype, fnPost[action](request))
                except:
                    raise
                    result = "unknown error"
            else:
                result = "unknown action"
                
            if isinstance(result, Document):
                return HttpResponse(result.toprettyxml(), mimetype="text/xml")
            else:
                return HttpResponse(result)
        else:
            return render_to_response('api/api_help.html', context_instance=RequestContext(request))
        
    else:
        return render_to_response('api/api_help.html', context_instance=RequestContext(request))
    
    # A faire la partie set avec POST + appels vers les formulaire + save des objets
    # Login et logout
