from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.http import Http404
from django.template import  loader
from jobs.models import Job
from jobs.models import JobCities,JobTypes

def job_list(request):
    job_list = Job.objects.order_by("job_type")
    template = loader.get_template("joblist.html")
    context = {'job_list': job_list}
    for job in job_list:
        job.city_name = JobCities[job.job_city][1]
        job.job_type = JobTypes[job.job_type][1]
    # return HttpResponse(template.render(context))
    return render(request,'joblist.html',context)

def detail(request,job_id):
    try:
        job = Job.objects.get(pk=job_id)
        job.city_name =  JobCities[job.job_city][1]
    except Job.DoesNotExist:
        raise Http404("Job does not exist")
    return render(request,'job.html',{'job':job})