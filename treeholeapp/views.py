# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from models import ContentModel
from django.template import Context, loader
from django.shortcuts import render_to_response, RequestContext
from django.contrib import messages
#import datetime
from datetime import tzinfo, timedelta, datetime
from django.core.urlresolvers import reverse

MSG={
'P_NOT_VALID':'Only UI IP is allowed',
'CONTENT_TOO_LONG':'Content more than 120 words or less than 5 words',
'TOO_MANY_TIMES':'publish once per half an hour',
'PUBLISH_ERROR':'publish error',
'PUBLISH_OK':'publish successful',
}
def index(request):
    template = loader.get_template('treeholeapp/index.html')
    ipaddr = request.META.get('REMOTE_ADDR', '')
    if request.method == 'POST':
        _content = request.POST.get('content', '')
        if not checkIP(ipaddr):
            messages.error(request, MSG['IP_NOT_VALID'])
        elif not (len(_content) < 120 and len(_content) > 5):
            messages.error(request, MSG['CONTENT_TOO_LONG'])
#        elif ContentModel.objects.filter(ip=ipaddr, time__range=\
#                (datetime.now()-timedelta(minutes=30), datetime.now())).count() > 0:
#            messages.error(request, MSG['TOO_MANY_TIMES'])
        else:
            new_content = ContentModel(ip=ipaddr, 
                    time=datetime.now(),
		contentstr=_content)
            new_content.save()
            try:
                pass;
                #postStatus(_content, ContentModel.objects.count())
            except RuntimeError:
                messages.error(request, MSG['PUBLISH_ERROR'])
                logging.error('Error in ' + str(ContentModel.objects.count()))
            else:
                messages.success(request, MSG['PUBLISH_OK']);
		return HttpResponseRedirect(reverse('treeholeapp:result'));
#		return HttpResponseRedirect("result.html");

    return render_to_response('treeholeapp/index.html', \
          # {'messages':messages}, \
            context_instance=RequestContext(request))

def checkIP(ipaddr):
    return True;

def postStatus(msgcontent,numberofmessages):
    return HttpResponseRedirect(reverse('treeholeapp:result'));

def result(request):
 #   return render_to_response('treeholeapp/result.html', \
          # {'messages':messages}, \
 #           context_instance=RequestContext(request));
    template = loader.get_template('treeholeapp/result.html');
    itemline=ContentModel.objects.order_by('-time')
    context = Context({
        'itemline': itemline,
    })
    return HttpResponse(template.render(context))
