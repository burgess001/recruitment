from django.conf.urls import url
from jobs import views
from django.urls import path

urlpatterns = [
    path("", views.job_list,name="joblist"),
    url(r"^job/(?P<job_id>\d+)/$",views.detail,name="detail")
]