from django.contrib import admin
from jobs.models import Job,Resume
# Register your models here.
# from 


class JobAdmin(admin.ModelAdmin):
    exclude = ('creator','create_date','modify_date')
    list_display = ('job_name','job_type','job_city','creator','create_date','modify_date')
    def save_model(self,request,obj,form,change):
        obj.creator = request.user
        super().save_model(request,obj,form,change)


class ResumeAdmin(admin.ModelAdmin):
    
    # actions = (enter_interview_process,)

    # def image_tag(self, obj):              
    #     if obj.picture:
    #         return format_html('<img src="{}" style="width:100px;height:80px;"/>'.format(obj.picture.url))
    #     return ""
    # image_tag.allow_tags = True
    # image_tag.short_description = 'Image'

    list_display = ('username', 'applicant', 'city', 'apply_position', 'bachelor_school', 'master_school', 'major','created_date')

    readonly_fields = ('applicant', 'created_date', 'modified_date',)

    fieldsets = (
        (None, {'fields': (
            "applicant", ("username", "city", "phone"),
            ("email", "apply_position", "born_address", "gender", ), ("picture", "attachment",),
            ("bachelor_school", "master_school"), ("major", "degree"), ('created_date', 'modified_date'),
            "candidate_introduction", "work_experience","project_experience",)}),
    )

    def save_model(self, request, obj, form, change):
        obj.applicant = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Job,JobAdmin)
admin.site.register(Resume, ResumeAdmin)