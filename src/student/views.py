from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Q

from account import models
from office import models as office_model
from teacher import models as teacher_model


#student dashboard access permission mixin
class StudentPermissionMixin(object):
    def has_permissions(self, request):
        return request.user.member_type.name == 'student'

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permissions(request):
            return redirect('account:login')
        return super(StudentPermissionMixin, self).dispatch(
            request, *args, **kwargs)



#student dashboard
class Home(StudentPermissionMixin, View):
    template_name = 'student/index.html'

    def get(self, request):
        return render(request, self.template_name)




#==========================================
#==========================================
#=====start schedule orperation view=======
#==========================================
#==========================================


#office schedule
class Schedule(StudentPermissionMixin, View):
    template_name = 'student/schedule.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        pass



#routine view
class RoutineView(StudentPermissionMixin, View):
    template_name = 'student/routine-view.html'

    def get(self, request):
        routines = office_model.ClassRoutine.objects.filter(Q(school=request.user.school) & Q(classes=request.user.classes) & Q(section=request.user.section)).all()

        variables = {
            'routines': routines,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        pass



#exam routine view
class ExamRoutineView(StudentPermissionMixin, View):
    template_name = 'student/exam-routine-view.html'

    def get(self, request):
        routines = office_model.ExamRoutine.objects.filter(Q(school=request.user.school) & Q(classes=request.user.classes)).all()

        variables = {
            'routines': routines,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        pass


#class test exam time and date
class ClassTestRoutineView(StudentPermissionMixin, View):
    template_name = 'student/class-test-exam-time-list.html'

    def get(self, request):

        exam_lists = teacher_model.ClassTestExamTime.objects.filter(Q(school=request.user.school) & Q(classes=request.user.classes) & Q(section=request.user.section)).order_by('-date').all()
        count = teacher_model.ClassTestExamTime.objects.filter(Q(school=request.user.school) & Q(classes=request.user.classes) & Q(section=request.user.section)).count()


        variables = {
            'exam_lists': exam_lists,
            'count': count,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        pass


#==========================================
#==========================================
#======end schedule orperation view========
#==========================================
#==========================================
