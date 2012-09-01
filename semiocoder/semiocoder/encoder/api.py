from xml.dom.minidom import Document
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from semiocoder.settings import LOGIN_URL
from semiocoder.core.api import getEncoders, getJobDetails, getJoblistDetails, getJoblists, getJobs, getTaskDetails, getTasks, gethistorydetails
from semiocoder.core.api import formatResult, getHistories, getEncoderDetails, setJob, setJoblist, setTask, login, logout

# TODO: developper API

@user_passes_test(lambda u: u.has_perm('encoder'), login_url=LOGIN_URL)
def api(request):
    if request.method == 'GET':
        if "format" in request.GET:
            mimetype = request.GET["format"]
            if mimetype not in ['xml', 'json']: mimetype = 'xml'
        else:
            mimetype = 'xml'
        if "action" in request.GET:
            action = request.GET["action"]
            result = None
            
            fnGetNoArg = { "getencoders": getEncoders, "getjobs":  getJobs, "getjoblists": getJoblists, "gettasks": getTasks,
                           "gethistories": getHistories, "logout": logout }
            
            fnGetOneArg = { "getencoderdetails": getEncoderDetails, "getjobdetails" : getJobDetails, "getjoblistdetails": getJoblistDetails,
                            "gettaskdetails": getTaskDetails, "gethistorydetails": gethistorydetails,
                           }
            
            if action in fnGetNoArg:
                result = formatResult(mimetype, fnGetNoArg[action]())
            else:
                if "id" in request.GET:
                    Id = request.GET["id"]
                    if action in fnGetOneArg:
                        try:
                            result = formatResult(mimetype, fnGetOneArg[action](Id))
                        except:
                            result = "bad arguments"
                    else:
                        result = "no result"
                else:
                    result = "no result"    
                    
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
            result = None
            
            fnPost = { "setjob":  setJob, "setjoblist":  setJoblist, "settask" : setTask, "login" : login, }
        
            if action in fnPost:
                result = fnPost[action](request)
            else:
                result = "no result"
                
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
    
    