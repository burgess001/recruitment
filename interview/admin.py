from django.contrib import admin
from interview.models import Candidate
# Register your models here.
from django.http import HttpResponse
from django.db.models import Q
import csv
from datetime import datetime
import logging
from interview import candidate_field as cf

logger = logging.getLogger(__name__)

exportable_fields = ('username','city','phone','bachelor_school','master_school','degree','first_result',
        'first_interviewer_user','second_result','second_interviewer_user','hr_result','hr_score','hr_remark','hr_interviewer_user')

def export_model_as_csv(modeladmin,request,queryset):
    response = HttpResponse(content_type="text/csv")
    field_list = exportable_fields
    response['Content-Disposition'] = 'attachment; filename=recruitment-candidates-list-%s.csv'% (
        datetime.now().strftime('%Y-%m-%d-%H-%M-%s'),
    )

    ### 写入表头
    writer = csv.writer(response)
    writer.writerow(
        [queryset.model._meta.get_field(f).verbose_name.title() for f in field_list]
    )
    for obj in queryset:
        csv_line_values = []
        for field in field_list:
            field_object = queryset.model._meta.get_field(field)
            field_value = field_object.value_from_object(obj)
            csv_line_values.append(field_value)
        writer.writerow(csv_line_values)
    logger.error(" %s has exported %s candidate records" % (request.user.username, len(queryset)))

    return response

export_model_as_csv.short_description = u'导出为csv文件'
export_model_as_csv.allowed_permissions = ('export',)
# 候选人管理类
class CandidateAdmin(admin.ModelAdmin):

    #create 和 modify 时不显示这些字段
    exclude = ('creator', 'created_date', 'modified_date')

    actions = [export_model_as_csv,]

    # 当前用户是否有导出权限：
    def has_export_permission(self, request):
        opts = self.opts
        return request.user.has_perm('%s.%s' % (opts.app_label, "export"))

    #list页面显示的内容
    list_display = (
        'username', 'city', 'bachelor_school', 'first_score', 'first_result', 'first_interviewer_user', 'second_score',
        'second_result', 'second_interviewer_user', 'hr_score', 'hr_result', 'hr_interviewer_user',)
    #搜索字段
    search_fields = ('username', 'phone', 'email', 'bachelor_school')

    #筛选条件
    list_filter = ("city","first_result","second_result","hr_result","first_interviewer_user","second_interviewer_user","hr_interviewer_user")

    #排序
    ordering = ("hr_result","second_result","first_result")
    # list_editable = ('first_interviewer_user','second_interviewer_user',)
    def get_list_editable(self,request):
        group_names = self.get_group_names(request.user)

        if request.user.is_superuser or 'hr' in group_names:
            return ('first_interviewer_user','second_interviewer_user',)
        return ()
    # readonly_fields = ('first_interviewer_user','second_interviewer_user',)
    def get_group_names(self, user):
        group_names = []
        for g in user.groups.all():
            group_names.append(g.name)
        return group_names
     
    def get_readonly_fields(self, request, obj):
        group_names = self.get_group_names(request.user)

        if 'interviewer' in group_names:
            logger.info("interviewer is in user's group for %s" % request.user.username)
            return ('first_interviewer_user','second_interviewer_user',)
        return ()
    #admin页面 分组展示
    #fieldsets 里每一个元组是一个组
    #修改布局，fields里再分元组，每个元组可以展示在一行
    # fieldsets = (
    #     (None,{'fields':("userid", ("username", "city", "phone"), ("email", "apply_position", "born_address"), ("gender", "candidate_remark"), ("bachelor_school", "master_school", "doctor_school"), ("major","degree"), ("test_score_of_general_ability","paper_score"), "last_editor",)}),
    #     ("第一轮面试记录",{'fields':("first_score", "first_learning_ability", "first_professional_competency", "first_advantage", "first_disadvantage", "first_result", "first_recommend_position", "first_interviewer_user", "first_remark",)}),
    #     ("第二轮专业复试记录",{'fields':("second_score", "second_learning_ability", "second_professional_competency", "second_pursue_of_excellence", "second_communication_ability", "second_pressure_score", "second_advantage", "second_disadvantage", "second_result", "second_recommend_position", "second_interviewer_user", "second_remark",)}),
    #     ("HR复试记录",{'fields':("hr_score", "hr_responsibility", "hr_communication_ability", "hr_logic_ability", "hr_potential", "hr_stability", "hr_advantage", "hr_disadvantage", "hr_result", "hr_interviewer_user", "hr_remark",)}),
    # )
     # 一面面试官仅填写一面反馈， 二面面试官可以填写二面反馈
    def get_fieldsets(self, request, obj=None):
        group_names = self.get_group_names(request.user)

        if 'interviewer' in group_names and obj.first_interviewer_user == request.user:
            return cf.default_fieldsets_first
        if 'interviewer' in group_names and obj.second_interviewer_user == request.user:
            return cf.default_fieldsets_second
        return cf.default_fieldsets

    # 对于非管理员，非HR，获取自己是一面面试官或者二面面试官的候选人集合:s
    def get_queryset(self, request):  # show data only owned by the user
        qs = super(CandidateAdmin, self).get_queryset(request)

        group_names = self.get_group_names(request.user)
        if request.user.is_superuser or 'hr' in group_names:
            return qs
        return Candidate.objects.filter(Q(first_interviewer_user=request.user) | Q(second_interviewer_user=request.user))
admin.site.register(Candidate,CandidateAdmin)