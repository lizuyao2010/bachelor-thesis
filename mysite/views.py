from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.core.mail import send_mail
from django.http import HttpResponseRedirect

import datetime

import sem_classification


def hello(request):
    return HttpResponse("Hello world")

def current_datetime(request):
    now = datetime.datetime.now()
    return render_to_response('current_datetime.html',{'current_date': now})

def hours_ahead(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    #assert False
    html = "<html><body>In %s hour(s), it will be %s.</body></html>" % (offset, dt)
    return HttpResponse(html)

def search_form(request):
    return render_to_response('search_form.html')


def search(request):
    if 'q' in request.GET and request.GET['q']:
	q = request.GET['q']
	answers,new_answers = sem_classification.Query(q.encode('utf-8'))
	#for item in ls:
	    #answers.append(item[0])	
	return render_to_response('search_results.html',{'answers':answers,'new_answers':new_answers,'query':q})
    else:
        message = 'You submitted an empty form.'
    	return HttpResponse(message)

def contact(request):
    errors = []
    if request.method == 'POST':
        if not request.POST.get('subject', ''):
            errors.append('Enter a subject.')
        if not request.POST.get('message', ''):
            errors.append('Enter a message.')
        if request.POST.get('email') and '@' not in request.POST['email']:
            errors.append('Enter a valid e-mail address.')
        if not errors:
            send_mail(
                request.POST['subject'],
                request.POST['message'],
                request.POST.get('email', 'noreply@example.com'),
                ['siteowner@example.com'],
            )
            return HttpResponseRedirect('/contact/thanks/')
    return render_to_response('contact_form.html',
        {'errors': errors})

def thanks(request):
    return HttpResponse("thanks")

def surgery_form(request):
    return render_to_response('surgery_form.html')