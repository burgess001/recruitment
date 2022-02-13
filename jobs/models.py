from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.
DEGREE_TYPE = ((u'本科', u'本科'), (u'硕士', u'硕士'), (u'博士', u'博士'))
JobTypes = [
    (0,"技术类"),
    (1,"产品类"),
    (2,'运营类'),
    (3,'设计类')
]
JobCities = (
    (0,"北京"),
    (1,"上海"),
    (2,"广州"),
    (3,"深圳")
)
class Job(models.Model):
    job_type = models.SmallIntegerField(blank=False,choices=JobTypes,verbose_name='职位类别')
    job_name = models.CharField(max_length=250,blank=False,verbose_name='职位名称')
    job_city = models.SmallIntegerField(blank=False,choices=JobCities,verbose_name='工作地点')
    job_responsibility = models.TextField(max_length=1024,verbose_name="职位职责")
    job_requirement =  models.TextField(max_length=1024,verbose_name="职位要求")
    creator = models.ForeignKey(User,verbose_name="创建人",null=True,on_delete=models.SET_NULL)
    create_date = models.DateTimeField(verbose_name='创建日期',default=datetime.now)
    modify_date = models.DateTimeField(verbose_name='修改日期',default=datetime.now)