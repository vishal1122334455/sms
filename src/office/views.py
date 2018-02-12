from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.db.models import Q
from django.contrib.auth import update_session_auth_hash

from . import forms
from account import models
from . import models as office_model



class OfficePermissionMixin(object):
    def has_permissions(self, request):
        return request.user.member_type.name == 'office'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if not self.has_permissions(request):
                return redirect('account:login')
            return super(OfficePermissionMixin, self).dispatch(
                request, *args, **kwargs)
        else:
            return redirect('account:login')



def check_user(request, pk):
    user_objects = models.UserProfile.objects.filter(pk=pk)

    user_school_id = False
    for user_obj in user_objects:
        user_school_id = user_obj.school.id

    #compare admin school id to requested user school id for same school retrive
    if user_school_id == request.user.school.id:
        return user_objects


#office home page
class Home(OfficePermissionMixin, View):
    template_name = 'office/index.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        pass


#==========================================
#==========================================
#======start member orperation view========
#==========================================
#==========================================

#office registration for other official and student, teacher, parent, librarian
class Registration(OfficePermissionMixin, View):
    template_name = 'office/registration.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        pass


#member edit view
class MemberSearch(OfficePermissionMixin, View):
    template_name = 'office/search.html'

    def get(self, request):
        search_form = forms.SearchForm()

        variables = {
            'search_form': search_form,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        search_form = forms.SearchForm(request.POST or None)

        queries = None
        count = None
        if search_form.is_valid():
            queries, count = search_form.search(request)

        variables = {
            'search_form': search_form,
            'queries': queries,
            'count': count,
        }

        return render(request, self.template_name, variables)


#member detail view
class MemberDetail(OfficePermissionMixin, View):
    template_name = 'office/member-detail.html'

    def get(self, request, pk):
        get_object_or_404(models.UserProfile, pk=pk)

        #requested user object
        user_objects = models.UserProfile.objects.filter(pk=pk)

        user_school_id = None
        viewable_user = None

        for user_obj in user_objects:
            user_school_id = user_obj.school.id

        #compare admin school id to requested user school id for same school retrive
        if user_school_id == request.user.school.id:
            viewable_user = user_objects

        variables = {
            'viewable_user': viewable_user,
        }

        return render(request, self.template_name, variables)

    def post(self, request, pk):
        pass


class MemberEdit(OfficePermissionMixin, View):
    template_name = 'office/member-edit.html'

    def get(self, request, pk):
        get_object_or_404(models.UserProfile, pk=pk)

        member_edit_form = forms.MemberEditForm(instance=models.UserProfile.objects.get(pk=pk), request=request)

        check_admin_permission = check_user(request, pk)

        viewable_user = False

        if check_admin_permission:
            viewable_user = check_admin_permission

        variables = {
            'viewable_user': viewable_user,
            'member_edit_form': member_edit_form,
        }

        return render(request, self.template_name, variables)

    def post(self, request, pk):
        get_object_or_404(models.UserProfile, pk=pk)

        member_edit_form = forms.MemberEditForm(request.POST or None, request.FILES, instance=models.UserProfile.objects.get(pk=pk), request=request)

        check_admin_permission = check_user(request, pk)

        viewable_user = False

        if check_admin_permission:
            viewable_user = check_admin_permission

            if member_edit_form.is_valid():
                member_edit_form.save()

        variables = {
            'viewable_user': viewable_user,
            'member_edit_form': member_edit_form,
        }

        return render(request, self.template_name, variables)


class MemberDelete(OfficePermissionMixin, View):
    template_name = 'office/member-delete.html'

    def get(self, request, pk):
        get_object_or_404(models.UserProfile, pk=pk)

        check_admin_permission = check_user(request, pk)

        viewable_user = False

        if check_admin_permission:
            viewable_user = check_admin_permission

        variables = {
            'viewable_user': viewable_user,
        }

        return render(request, self.template_name, variables)

    def post(self, request, pk):
        get_object_or_404(models.UserProfile, pk=pk)

        check_admin_permission = check_user(request, pk)

        viewable_user = False

        if check_admin_permission:
            viewable_user = check_admin_permission

            if request.POST.get('yes') == 'yes':
                member_id = request.POST.get('member_id')

                member_obj = models.UserProfile.objects.get(id=member_id)
                member_obj.delete()

                return redirect('office:member-search')

            elif request.POST.get('no') == 'no':
                member_id = request.POST.get('member_id')
                return redirect('office:member-detail', pk=member_id)

        variables = {
            'viewable_user': viewable_user,
        }

        return render(request, self.template_name, variables)


#office member list
class MemberList(OfficePermissionMixin, View):
    template_name = 'office/member-list.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        pass


#office member list detail
class MemberListDetail(OfficePermissionMixin, View):
    template_name = 'office/member-list-detail.html'

    def get(self, request, type):
        member_type = type

        queries = models.UserProfile.objects.filter(Q(school__id=request.user.school.id) & Q(member_type__name=type)).all()
        count = models.UserProfile.objects.filter(Q(school__id=request.user.school.id) & Q(member_type__name=type)).count()

        variables = {
            'queries': queries,
            'count': count,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        pass


#office class detail
class StudentClass(OfficePermissionMixin, View):
    template_name = 'office/student-class-list.html'

    def get(self, request):

        classes = models.Class.objects.filter(Q(school__name=request.user.school.name)).all()
        count = models.Class.objects.filter(Q(school__name=request.user.school.name)).count()

        variables = {
            'classes': classes,
            'count': count,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        pass


#office :: student list in class
class StudenListInClass(OfficePermissionMixin, View):
    template_name = 'office/student-list-in-class.html'

    def get(self, request, classes):

        students = models.UserProfile.objects.filter(Q(school__name=request.user.school.name) & Q(classes__name=classes) & Q(member_type__name='student')).all()
        count = models.UserProfile.objects.filter(Q(school__name=request.user.school.name) & Q(classes__name=classes) & Q(member_type__name='student')).count()

        variables = {
            'students': students,
            'count': count,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        pass


#office :: class wise section
class ClassWiseSection(OfficePermissionMixin, View):
    template_name = 'office/class-wise-section.html'

    def get(self, request, classes):

        sections = models.Section.objects.filter(Q(school__name=request.user.school.name) & Q(classes__name=classes)).all()
        count = models.Section.objects.filter(Q(school__name=request.user.school.name) & Q(classes__name=classes)).count()

        variables = {
            'sections': sections,
            'count': count,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        pass


#office :: section wise student
class SectionWiseStudent(OfficePermissionMixin, View):
    template_name = 'office/section-wise-student.html'

    def get(self, request, classes, section):

        students = models.UserProfile.objects.filter(Q(school__name=request.user.school.name) & Q(classes__name=classes) & Q(section__name=section) & Q(member_type__name='student')).all()
        count = models.UserProfile.objects.filter(Q(school__name=request.user.school.name) & Q(classes__name=classes) & Q(section__name=section) & Q(member_type__name='student')).count()

        variables = {
            'students': students,
            'count': count,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        pass

#==========================================
#==========================================
#=======end member orperation view=========
#==========================================
#==========================================



#==========================================
#==========================================
#=====start schedule orperation view=======
#==========================================
#==========================================


#office schedule
class Schedule(OfficePermissionMixin, View):
    template_name = 'office/schedule.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        pass


#office schedule:::class list
class ClassList(OfficePermissionMixin, View):
    template_name = 'office/class-list.html'

    def get(self, request):

        classes = models.Class.objects.filter(Q(school__name=request.user.school.name)).all()
        count = models.Class.objects.filter(Q(school__name=request.user.school.name)).count()

        variables = {
            'classes': classes,
            'count': count,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        pass


#office schedule:::section list
class SectionList(OfficePermissionMixin, View):
    template_name = 'office/section-list.html'

    def get(self, request, classes):

        sections = models.Section.objects.filter(Q(school__name=request.user.school.name) & Q(classes__name=classes)).all()
        count = models.Section.objects.filter(Q(school__name=request.user.school.name) & Q(classes__name=classes)).count()

        variables = {
            'sections': sections,
            'count': count,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        pass


#office schedule::::routine create
class RoutineCreate(OfficePermissionMixin, View):
    template_name = 'office/routine-create.html'

    def get(self, request, classes, section):

        classes_obj = models.Class.objects.get(Q(school=request.user.school) & Q(name=classes))

        class_routine_form = forms.CreateRoutineForm(request=request, classes=classes_obj)

        variables = {
            'class_routine_form': class_routine_form,
        }

        return render(request, self.template_name, variables)

    def post(self, request, classes, section):
        classes_obj = models.Class.objects.get(Q(school=request.user.school) & Q(name=classes))

        class_routine_form = forms.CreateRoutineForm(request.POST or None, request=request, classes=classes_obj)

        if class_routine_form.is_valid():
            class_routine_form.deploy(section)

        variables = {
            'class_routine_form': class_routine_form,
        }

        return render(request, self.template_name, variables)


#routine view
class RoutineView(OfficePermissionMixin, View):
    template_name = 'office/routine-view.html'

    def get(self, request, classes, section):
        classes_obj = models.Class.objects.get(Q(school=request.user.school) & Q(name=classes))
        section_obj = models.Section.objects.get(Q(school=request.user.school) & Q(classes=classes_obj) & Q(name=section))

        routines = office_model.ClassRoutine.objects.filter(Q(school=request.user.school) & Q(classes=classes_obj) & Q(section=section_obj)).all()

        variables = {
            'routines': routines,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        pass

#routine edit
class RoutineEdit(OfficePermissionMixin, View):
    template_name = 'office/routine-edit.html'

    def get(self, request, pk):
        get_object_or_404(office_model.ClassRoutine, pk=pk)



        routine_obj = office_model.ClassRoutine.objects.filter(pk=pk)
        routine_objs = office_model.ClassRoutine.objects.get(pk=pk)

        classes_obj = False
        routine_school = False
        for routines in routine_obj:
            classes_obj = routines.classes
            routine_school = routines.school.name

        routine_edit_form = False
        if routine_school == request.user.school.name:
            routine_edit_form = forms.RoutineEditForm(instance=routine_objs, request=request, classes=classes_obj)

        variables = {
            'routine_edit_form': routine_edit_form,
            'routine_obj': routine_obj,
        }

        return render(request, self.template_name, variables)

    def post(self, request, pk):
        get_object_or_404(office_model.ClassRoutine, pk=pk)

        routine_obj = office_model.ClassRoutine.objects.filter(pk=pk)
        routine_objs = office_model.ClassRoutine.objects.get(pk=pk)

        classes_obj = False
        routine_school = False
        for routines in routine_obj:
            classes_obj = routines.classes
            routine_school = routines.school.name

        routine_edit_form = forms.RoutineEditForm(request.POST or None, instance=routine_objs, request=request, classes=classes_obj)

        if routine_school == request.user.school.name:
            if routine_edit_form.is_valid():
                routine_edit_form.save()

        variables = {
            'routine_edit_form': routine_edit_form,
            'routine_obj': routine_obj,
        }

        return render(request, self.template_name, variables)


#routine delete
class RoutineDelete(OfficePermissionMixin, View):
    template_name = 'office/routine-delete.html'

    def get(self, request, pk):
        get_object_or_404(office_model.ClassRoutine, pk=pk)

        routine_obj = office_model.ClassRoutine.objects.filter(pk=pk)

        routine_school = False
        for routines in routine_obj:
            routine_school = routines.school.name

        viewable_routine = False
        if routine_school == request.user.school.name:
            viewable_routine = routine_obj

        variables = {
            'viewable_routine': viewable_routine,
        }

        return render(request, self.template_name, variables)

    def post(self, request, pk):
        get_object_or_404(models.UserProfile, pk=pk)

        routine_obj = office_model.ClassRoutine.objects.filter(pk=pk)

        routine_school = False
        routine_class = False
        routine_section = False
        for routines in routine_obj:
            routine_school = routines.school.name
            routine_class = routines.classes.name
            routine_section = routines.section.name

        viewable_routine = False
        if routine_school == request.user.school.name:
            viewable_routine = routine_obj

            if request.POST.get('yes') == 'yes':
                routine_id = request.POST.get('routine_id')

                routine_obj = office_model.ClassRoutine.objects.get(id=routine_id)
                routine_obj.delete()

                return redirect('office:routine-view', classes=routine_class, section=routine_section)

            elif request.POST.get('no') == 'no':
                return redirect('office:routine-view', classes=routine_class, section=routine_section)

        variables = {
            'viewable_routine': viewable_routine,
        }

        return render(request, self.template_name, variables)


#create exam routine
class ExamRoutineCreate(OfficePermissionMixin, View):
    template_name = 'office/exam-routine-create.html'

    def get(self, request, classes):

        classes_obj = models.Class.objects.get(Q(school=request.user.school) & Q(name=classes))

        exam_routine_form = forms.CreateExamRoutineForm(request=request, classes=classes_obj)

        variables = {
            'exam_routine_form': exam_routine_form,
        }

        return render(request, self.template_name, variables)

    def post(self, request, classes):
        classes_obj = models.Class.objects.get(Q(school=request.user.school) & Q(name=classes))

        exam_routine_form = forms.CreateExamRoutineForm(request.POST or None, request=request, classes=classes_obj)

        if exam_routine_form.is_valid():
            exam_routine_form.deploy()

        variables = {
            'exam_routine_form': exam_routine_form,
        }

        return render(request, self.template_name, variables)



#exam routine view
class ExamRoutineView(OfficePermissionMixin, View):
    template_name = 'office/exam-routine-view.html'

    def get(self, request, classes):
        classes_obj = models.Class.objects.get(Q(school=request.user.school) & Q(name=classes))

        routines = office_model.ExamRoutine.objects.filter(Q(school=request.user.school) & Q(classes=classes_obj)).all()

        variables = {
            'routines': routines,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        pass


#exam routine edit
class ExamRoutineEdit(OfficePermissionMixin, View):
    template_name = 'office/exam-routine-edit.html'

    def get(self, request, pk):
        get_object_or_404(office_model.ExamRoutine, pk=pk)

        routine_obj = office_model.ExamRoutine.objects.filter(pk=pk)
        routine_objs = office_model.ExamRoutine.objects.get(pk=pk)

        classes_obj = False
        routine_school = False
        for routines in routine_obj:
            classes_obj = routines.classes
            routine_school = routines.school.name

        exam_routine_edit_form = False
        if routine_school == request.user.school.name:
            exam_routine_edit_form = forms.ExamRoutineEditForm(instance=routine_objs, request=request, classes=classes_obj)

        variables = {
            'exam_routine_edit_form': exam_routine_edit_form,
            'routine_obj': routine_obj,
        }

        return render(request, self.template_name, variables)

    def post(self, request, pk):
        get_object_or_404(office_model.ExamRoutine, pk=pk)

        routine_obj = office_model.ExamRoutine.objects.filter(pk=pk)
        routine_objs = office_model.ExamRoutine.objects.get(pk=pk)

        classes_obj = False
        routine_school = False
        for routines in routine_obj:
            classes_obj = routines.classes
            routine_school = routines.school.name

        exam_routine_edit_form = forms.ExamRoutineEditForm(request.POST or None, instance=routine_objs, request=request, classes=classes_obj)

        if routine_school == request.user.school.name:
            if exam_routine_edit_form.is_valid():
                exam_routine_edit_form.save()

        variables = {
            'exam_routine_edit_form': exam_routine_edit_form,
            'routine_obj': routine_obj,
        }

        return render(request, self.template_name, variables)



#exam routine delete
class ExamRoutineDelete(OfficePermissionMixin, View):
    template_name = 'office/exam-routine-delete.html'

    def get(self, request, pk):
        get_object_or_404(office_model.ExamRoutine, pk=pk)

        routine_obj = office_model.ExamRoutine.objects.filter(pk=pk)

        routine_school = False
        for routines in routine_obj:
            routine_school = routines.school.name

        viewable_routine = False
        if routine_school == request.user.school.name:
            viewable_routine = routine_obj

        variables = {
            'viewable_routine': viewable_routine,
        }

        return render(request, self.template_name, variables)

    def post(self, request, pk):
        get_object_or_404(office_model.ExamRoutine, pk=pk)

        routine_obj = office_model.ExamRoutine.objects.filter(pk=pk)

        routine_school = False
        routine_class = False
        for routines in routine_obj:
            routine_school = routines.school.name
            routine_class = routines.classes.name

        viewable_routine = False
        if routine_school == request.user.school.name:
            viewable_routine = routine_obj

            if request.POST.get('yes') == 'yes':
                routine_id = request.POST.get('routine_id')

                routine_obj = office_model.ExamRoutine.objects.get(id=routine_id)
                routine_obj.delete()

                return redirect('office:exam-routine-view', classes=routine_class)

            elif request.POST.get('no') == 'no':
                return redirect('office:exam-routine-view', classes=routine_class)

        variables = {
            'viewable_routine': viewable_routine,
        }

        return render(request, self.template_name, variables)

#==========================================
#==========================================
#======end schedule orperation view========
#==========================================
#==========================================


#==========================================
#==========================================
#======start notice orperation view========
#==========================================
#==========================================


#notice schedule
class Notice(OfficePermissionMixin, View):
    template_name = 'office/notice.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        pass


#notice create
class NoticeCreate(OfficePermissionMixin, View):
    template_name = 'office/notice-create.html'

    def get(self, request):
        create_notice_form = forms.NoticeForm(request=request)

        variables = {
            'create_notice_form': create_notice_form,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        create_notice_form = forms.NoticeForm(request.POST or None, request=request)

        if create_notice_form.is_valid():
            create_notice_form.deploy(request)

        variables = {
            'create_notice_form': create_notice_form,
        }

        return render(request, self.template_name, variables)


#office notice:::class list
class NoticeClassList(OfficePermissionMixin, View):
    template_name = 'office/notice-class-list.html'

    def get(self, request):

        classes = models.Class.objects.filter(Q(school__name=request.user.school.name)).all()
        count = models.Class.objects.filter(Q(school__name=request.user.school.name)).count()

        variables = {
            'classes': classes,
            'count': count,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        pass

#office notice:::notice list
class NoticeList(OfficePermissionMixin, View):
    template_name = 'office/notice-list.html'

    def get(self, request, classes):

        notices = office_model.Notice.objects.filter(Q(school__name=request.user.school.name) & Q(classes__name=classes)).all()
        count = office_model.Notice.objects.filter(Q(school__name=request.user.school.name) & Q(classes__name=classes)).count()

        variables = {
            'notices': notices,
            'count': count,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        pass


#office notice:::notice view
class NoticeView(OfficePermissionMixin, View):
    template_name = 'office/notice-view.html'

    def get(self, request, pk):

        notices = office_model.Notice.objects.filter(Q(school__name=request.user.school.name) & Q(pk=pk)).all()

        variables = {
            'notices': notices,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        pass


#office notice:::notice edit
class NoticeEdit(OfficePermissionMixin, View):
    template_name = 'office/notice-edit.html'

    def get(self, request, pk):
        get_object_or_404(office_model.Notice, pk=pk)

        notices = office_model.Notice.objects.filter(Q(school__name=request.user.school.name) & Q(pk=pk) & Q(user=request.user))

        notice_edit_form = forms.NoticeEditForm(request=request, instance=office_model.Notice.objects.get(pk=pk))

        variables = {
            'notices': notices,
            'notice_edit_form': notice_edit_form,
        }

        return render(request, self.template_name, variables)

    def post(self, request, pk):
        get_object_or_404(office_model.Notice, pk=pk)

        notices = office_model.Notice.objects.filter(Q(school__name=request.user.school.name) & Q(pk=pk) & Q(user=request.user))

        notice_edit_form = forms.NoticeEditForm(request.POST or None, request=request, instance=office_model.Notice.objects.get(pk=pk))

        if notice_edit_form.is_valid():
            notice_edit_form.save()

        variables = {
            'notices': notices,
            'notice_edit_form': notice_edit_form,
        }

        return render(request, self.template_name, variables)


#notice delete
class NoticeDelete(OfficePermissionMixin, View):
    template_name = 'office/notice-delete.html'

    def get(self, request, pk):
        get_object_or_404(office_model.Notice, pk=pk)

        notices = office_model.Notice.objects.filter(Q(school__name=request.user.school.name) & Q(pk=pk) & Q(user=request.user))

        viewable_notice = False
        if notices:
            viewable_notice = notices

        variables = {
            'viewable_notice': viewable_notice,
        }

        return render(request, self.template_name, variables)

    def post(self, request, pk):
        get_object_or_404(office_model.Notice, pk=pk)

        notices = office_model.Notice.objects.filter(Q(school__name=request.user.school.name) & Q(pk=pk) & Q(user=request.user))

        viewable_notice = False
        if notices:
            viewable_notice = notices

            if request.POST.get('yes') == 'yes':
                routine_id = request.POST.get('notice_id')

                routine_obj = office_model.Notice.objects.get(id=routine_id)
                routine_obj.delete()

                return redirect('office:notice')

            elif request.POST.get('no') == 'no':
                return redirect('office:notice')

        variables = {
            'viewable_notice': viewable_notice,
        }

        return render(request, self.template_name, variables)


#notice search view
class NoticeSearch(OfficePermissionMixin, View):
    template_name = 'office/notice-search.html'

    def get(self, request):
        search_form = forms.NoticeSearchForm()

        variables = {
            'search_form': search_form,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        search_form = forms.NoticeSearchForm(request.POST or None)

        queries = None
        count = None
        if search_form.is_valid():
            queries, count = search_form.search(request)

        variables = {
            'search_form': search_form,
            'queries': queries,
            'count': count,
        }

        return render(request, self.template_name, variables)

#==========================================
#==========================================
#=======end notice orperation view=========
#==========================================
#==========================================


#==========================================
#==========================================
#=====start gallary orperation view========
#==========================================
#==========================================

#gallary
class Gallary(OfficePermissionMixin, View):
    template_name = 'office/gallary.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        pass


#gallary-image
class GallaryImage(OfficePermissionMixin, View):
    template_name = 'office/gallary-image.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        pass


#gallary-image-create
class GallaryImageCreate(OfficePermissionMixin, View):
    template_name = 'office/gallary-image-create.html'

    def get(self, request):
        gallary_image_form = forms.GallaryImageForm()

        variables = {
            'gallary_image_form': gallary_image_form,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        gallary_image_form = forms.GallaryImageForm(request.POST or None, request.FILES)

        if gallary_image_form.is_valid():
            gallary_image_form.deploy(request)

        variables = {
            'gallary_image_form': gallary_image_form,
        }

        return render(request, self.template_name, variables)



#gallary-image view
class GallaryImageView(OfficePermissionMixin, View):
    template_name = 'office/gallary-image-view.html'

    def get(self, request):

        images = office_model.GallaryImage.objects.filter(school=request.user.school).order_by('-id')

        variables = {
            'images': images,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        pass



#image delete
class GallaryImageDelete(OfficePermissionMixin, View):
    template_name = 'office/gallary-image-delete.html'

    def get(self, request, pk):
        get_object_or_404(office_model.GallaryImage, pk=pk)

        images = office_model.GallaryImage.objects.filter(Q(school__name=request.user.school.name) & Q(pk=pk) & Q(user=request.user))

        viewable_image = False
        if images:
            viewable_image = images

        variables = {
            'viewable_image': viewable_image,
        }

        return render(request, self.template_name, variables)

    def post(self, request, pk):
        get_object_or_404(office_model.GallaryImage, pk=pk)

        images = office_model.GallaryImage.objects.filter(Q(school__name=request.user.school.name) & Q(pk=pk) & Q(user=request.user))

        viewable_image = False
        if images:
            viewable_image = images

            if request.POST.get('yes') == 'yes':
                image_id = request.POST.get('image_id')

                image_obj = office_model.GallaryImage.objects.get(id=image_id)
                image_obj.delete()

                return redirect('office:gallary-image-view')

            elif request.POST.get('no') == 'no':
                return redirect('office:gallary-image-view')

        variables = {
            'viewable_image': viewable_image,
        }

        return render(request, self.template_name, variables)


#gallary-video
class GallaryVideo(OfficePermissionMixin, View):
    template_name = 'office/gallary-video.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        pass



#gallary-video-create
class GallaryVideoCreate(OfficePermissionMixin, View):
    template_name = 'office/gallary-video-create.html'

    def get(self, request):
        gallary_video_form = forms.GallaryVideoForm()

        variables = {
            'gallary_video_form': gallary_video_form,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        gallary_video_form = forms.GallaryVideoForm(request.POST or None)

        if gallary_video_form.is_valid():
            gallary_video_form.deploy(request)

        variables = {
            'gallary_video_form': gallary_video_form,
        }

        return render(request, self.template_name, variables)


#gallary-vidoe view
class GallaryVideoView(OfficePermissionMixin, View):
    template_name = 'office/gallary-video-view.html'

    def get(self, request):

        videos = office_model.GallaryVideo.objects.filter(school=request.user.school).order_by('-id')

        variables = {
            'videos': videos,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        pass


#video delete
class GallaryVideoDelete(OfficePermissionMixin, View):
    template_name = 'office/gallary-video-delete.html'

    def get(self, request, pk):
        get_object_or_404(office_model.GallaryVideo, pk=pk)

        videos = office_model.GallaryImage.objects.filter(Q(school__name=request.user.school.name) & Q(pk=pk) & Q(user=request.user))

        viewable_video = False
        if videos:
            viewable_video = videos

        variables = {
            'viewable_video': viewable_video,
        }

        return render(request, self.template_name, variables)

    def post(self, request, pk):
        get_object_or_404(office_model.GallaryVideo, pk=pk)

        videos = office_model.GallaryVideo.objects.filter(Q(school__name=request.user.school.name) & Q(pk=pk) & Q(user=request.user))

        viewable_video = False
        if videos:
            viewable_video = videos

            if request.POST.get('yes') == 'yes':
                video_id = request.POST.get('video_id')

                video_obj = office_model.GallaryVideo.objects.get(id=video_id)
                video_obj.delete()

                return redirect('office:gallary-video-view')

            elif request.POST.get('no') == 'no':
                return redirect('office:gallary-video-view')

        variables = {
            'viewable_video': viewable_video,
        }

        return render(request, self.template_name, variables)



#==========================================
#==========================================
#=======end gallary orperation view========
#==========================================
#==========================================




#==========================================
#==========================================
#======start classroom module view=========
#==========================================
#==========================================

#classroom
class Classroom(OfficePermissionMixin, View):
    template_name = 'office/classroom.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        pass


#office classroom:::class list
class ClassroomClasslist(OfficePermissionMixin, View):
    template_name = 'office/classroom-classlist.html'

    def get(self, request):

        classes = models.Class.objects.filter(Q(school__name=request.user.school.name)).all()
        count = models.Class.objects.filter(Q(school__name=request.user.school.name)).count()

        variables = {
            'classes': classes,
            'count': count,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        pass



#office classroom:::section list
class ClassroomSectionlist(OfficePermissionMixin, View):
    template_name = 'office/classroom-sectionlist.html'

    def get(self, request, classes):

        sections = models.Section.objects.filter(Q(school=request.user.school) & Q(classes__name=classes)).all()
        count = models.Section.objects.filter(Q(school=request.user.school) & Q(classes__name=classes)).count()

        variables = {
            'sections': sections,
            'count': count,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        pass


#classroom create
class ClassroomCreate(OfficePermissionMixin, View):
    template_name = 'office/classroom-create.html'

    def get(self, request, classes, section):
        classroom_form = forms.ClassroomForm()

        variables = {
            'classroom_form': classroom_form,
        }

        return render(request, self.template_name, variables)

    def post(self, request, classes, section):
        classroom_form = forms.ClassroomForm(request.POST or None)

        if classroom_form.is_valid():
            classroom_form.deploy(request, classes, section)

        variables = {
            'classroom_form': classroom_form,
        }

        return render(request, self.template_name, variables)



#office classroom:::view
class ClassroomView(OfficePermissionMixin, View):
    template_name = 'office/classroom-view.html'

    def get(self, request, classes, section):

        classrooms = office_model.Classroom.objects.filter(Q(school=request.user.school) & Q(classes__name=classes) & Q(section__name=section)).all()
        count = office_model.Classroom.objects.filter(Q(school=request.user.school) & Q(classes__name=classes) & Q(section__name=section)).count()

        variables = {
            'classrooms': classrooms,
            'count': count,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        pass



#office notice:::notice edit
class ClassroomEdit(OfficePermissionMixin, View):
    template_name = 'office/classroom-edit.html'

    def get(self, request, pk):
        get_object_or_404(office_model.Classroom, pk=pk)

        classrooms = office_model.Classroom.objects.filter(Q(school__name=request.user.school.name) & Q(pk=pk))

        classroom_edit_form = forms.ClassroomEditForm(instance=office_model.Classroom.objects.get(pk=pk))

        variables = {
            'classrooms': classrooms,
            'classroom_edit_form': classroom_edit_form,
        }

        return render(request, self.template_name, variables)

    def post(self, request, pk):
        get_object_or_404(office_model.Classroom, pk=pk)

        classrooms = office_model.Classroom.objects.filter(Q(school__name=request.user.school.name) & Q(pk=pk))

        classroom_edit_form = forms.ClassroomEditForm(request.POST or None, instance=office_model.Classroom.objects.get(pk=pk))

        if classroom_edit_form.is_valid():
            classroom_edit_form.save()

        variables = {
            'classrooms': classrooms,
            'classroom_edit_form': classroom_edit_form,
        }

        return render(request, self.template_name, variables)



#classroom delete
class ClassroomDelete(OfficePermissionMixin, View):
    template_name = 'office/classroom-delete.html'

    def get(self, request, pk):
        get_object_or_404(office_model.Classroom, pk=pk)

        classrooms = office_model.Classroom.objects.filter(Q(school=request.user.school) & Q(pk=pk))

        viewable_classroom = False
        if classrooms:
            viewable_classroom = classrooms

        variables = {
            'viewable_classroom': viewable_classroom,
        }

        return render(request, self.template_name, variables)

    def post(self, request, pk):
        get_object_or_404(office_model.Classroom, pk=pk)

        classrooms = office_model.Classroom.objects.filter(Q(school__name=request.user.school.name) & Q(pk=pk))

        viewable_classroom = False
        if classrooms:
            viewable_classroom = classrooms

            if request.POST.get('yes') == 'yes':
                classroom_id = request.POST.get('classroom_id')

                classroom_obj = office_model.Classroom.objects.get(id=classroom_id)
                classroom_obj.delete()

                return redirect('office:classroom-classlist')

            elif request.POST.get('no') == 'no':
                return redirect('office:classroom-classlist')

        variables = {
            'viewable_video': viewable_video,
        }

        return render(request, self.template_name, variables)



#==========================================
#==========================================
#=======end classroom module view==========
#==========================================
#==========================================


#==========================================
#==========================================
#======start event orperation view=========
#==========================================
#==========================================

#event
class Event(OfficePermissionMixin, View):
    template_name = 'office/event.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        pass


#event create
class EventCreate(OfficePermissionMixin, View):
    template_name = 'office/event-create.html'

    def get(self, request):
        event_form = forms.EventForm()

        variables = {
            'event_form': event_form,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        event_form = forms.EventForm(request.POST or None)

        if event_form.is_valid():
            event_form.deploy(request)

        variables = {
            'event_form': event_form,
        }

        return render(request, self.template_name, variables)


#office event:::list
class EventList(OfficePermissionMixin, View):
    template_name = 'office/event-list.html'

    def get(self, request):

        events = office_model.Event.objects.filter(Q(school=request.user.school)).order_by('-id').all()
        count = office_model.Event.objects.filter(Q(school=request.user.school)).count()

        variables = {
            'events': events,
            'count': count,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        pass


#office event:::list
class EventView(OfficePermissionMixin, View):
    template_name = 'office/event-view.html'

    def get(self, request, pk):

        events = office_model.Event.objects.filter(Q(school=request.user.school) & Q(pk=pk)).all()

        variables = {
            'events': events,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        pass



#office event:::edit
class EventEdit(OfficePermissionMixin, View):
    template_name = 'office/event-edit.html'

    def get(self, request, pk):
        get_object_or_404(office_model.Event, pk=pk)

        events = office_model.Event.objects.filter(Q(school=request.user.school) & Q(pk=pk))

        event_edit_form = forms.EventEditForm(instance=office_model.Event.objects.get(pk=pk))

        variables = {
            'events': events,
            'event_edit_form': event_edit_form,
        }

        return render(request, self.template_name, variables)

    def post(self, request, pk):
        get_object_or_404(office_model.Event, pk=pk)

        events = office_model.Event.objects.filter(Q(school=request.user.school) & Q(pk=pk))

        event_edit_form = forms.EventEditForm(request.POST or None, instance=office_model.Event.objects.get(pk=pk))

        if event_edit_form.is_valid():
            event_edit_form.save()

        variables = {
            'events': events,
            'event_edit_form': event_edit_form,
        }

        return render(request, self.template_name, variables)



#event delete
class EventDelete(OfficePermissionMixin, View):
    template_name = 'office/event-delete.html'

    def get(self, request, pk):
        get_object_or_404(office_model.Event, pk=pk)

        events = office_model.Event.objects.filter(Q(school=request.user.school) & Q(pk=pk))

        viewable_event = False
        if events:
            viewable_event = events

        variables = {
            'viewable_event': viewable_event,
        }

        return render(request, self.template_name, variables)

    def post(self, request, pk):
        get_object_or_404(office_model.Event, pk=pk)

        events = office_model.Event.objects.filter(Q(school=request.user.school) & Q(pk=pk))

        viewable_event = False
        if events:
            viewable_event = events

            if request.POST.get('yes') == 'yes':
                event_id = request.POST.get('event_id')

                event_obj = office_model.Event.objects.get(id=event_id)
                event_obj.delete()

                return redirect('office:event-list')

            elif request.POST.get('no') == 'no':
                return redirect('office:event-list')

        variables = {
            'viewable_event': viewable_event,
        }

        return render(request, self.template_name, variables)



#==========================================
#==========================================
#=======end event orperation view==========
#==========================================
#==========================================



#==========================================
#==========================================
#======start payment orperation view=======
#==========================================
#==========================================

#payment
class Payment(OfficePermissionMixin, View):
    template_name = 'office/payment.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        pass



#office payment:::class list
class PaymentClassList(OfficePermissionMixin, View):
    template_name = 'office/payment-class-list.html'

    def get(self, request):

        classes = models.Class.objects.filter(Q(school__name=request.user.school.name)).all()
        count = models.Class.objects.filter(Q(school__name=request.user.school.name)).count()

        variables = {
            'classes': classes,
            'count': count,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        pass



#office payment:::section list
class PaymentSectionlist(OfficePermissionMixin, View):
    template_name = 'office/payment-section-list.html'

    def get(self, request, classes):

        sections = models.Section.objects.filter(Q(school=request.user.school) & Q(classes__name=classes)).all()
        count = models.Section.objects.filter(Q(school=request.user.school) & Q(classes__name=classes)).count()

        variables = {
            'sections': sections,
            'count': count,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        pass




#payment create
class PaymentEntry(OfficePermissionMixin, View):
    template_name = 'office/payment-create.html'

    def get(self, request, classes, section):
        classes_obj = models.Class.objects.get(Q(school=request.user.school) & Q(name=classes))
        section_obj = models.Section.objects.get(Q(school=request.user.school) & Q(classes=classes_obj) & Q(name=section))

        create_payment_form = forms.PaymentForm(request=request, classes=classes_obj, section=section_obj)

        variables = {
            'create_payment_form': create_payment_form,
        }

        return render(request, self.template_name, variables)

    def post(self, request, classes, section):
        classes_obj = models.Class.objects.get(Q(school=request.user.school) & Q(name=classes))
        section_obj = models.Section.objects.get(Q(school=request.user.school) & Q(classes=classes_obj) & Q(name=section))

        create_payment_form = forms.PaymentForm(request.POST or None, request=request, classes=classes_obj, section=section_obj)

        if create_payment_form.is_valid():
            create_payment_form.deploy()

        variables = {
            'create_payment_form': create_payment_form,
        }

        return render(request, self.template_name, variables)



#==========================================
#==========================================
#=======end payment orperation view========
#==========================================
#==========================================


#==========================================
#==========================================
#======start expenses orperation view======
#==========================================
#==========================================


#expense
class Expense(OfficePermissionMixin, View):
    template_name = 'office/expense.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        pass


#expense catagory
class ExpenseCatagory(OfficePermissionMixin, View):
    template_name = 'office/expense-catagory.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        pass



#expense catagory create
class ExpenseCatagoryCreate(OfficePermissionMixin, View):
    template_name = 'office/expense-catagory-create.html'

    def get(self, request):
        expense_catagory_form = forms.ExpenseCatagoryForm()

        variables = {
            'expense_catagory_form': expense_catagory_form,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        expense_catagory_form = forms.ExpenseCatagoryForm(request.POST or None)

        if expense_catagory_form.is_valid():
            expense_catagory_form.deploy(request)

        variables = {
            'expense_catagory_form': expense_catagory_form,
        }

        return render(request, self.template_name, variables)


#office expense:::catagory view
class ExpenseCatagoryView(OfficePermissionMixin, View):
    template_name = 'office/expense-catagory-view.html'

    def get(self, request):

        expense_catagory = office_model.ExpenseCatagory.objects.filter(Q(school=request.user.school)).all()

        variables = {
            'expense_catagory': expense_catagory,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        pass


#office expense:::catagory edit
class ExpenseCatagoryEdit(OfficePermissionMixin, View):
    template_name = 'office/expense-catagory-edit.html'

    def get(self, request, pk):
        get_object_or_404(office_model.ExpenseCatagory, pk=pk)

        catagories = office_model.ExpenseCatagory.objects.filter(Q(school=request.user.school) & Q(pk=pk))

        expense_catagory_edit_form = forms.ExpenseCatagoryEditForm(instance=office_model.ExpenseCatagory.objects.get(Q(pk=pk) & Q(school=request.user.school)))

        variables = {
            'catagories': catagories,
            'expense_catagory_edit_form': expense_catagory_edit_form,
        }

        return render(request, self.template_name, variables)

    def post(self, request, pk):
        get_object_or_404(office_model.ExpenseCatagory, pk=pk)

        catagories = office_model.ExpenseCatagory.objects.filter(Q(school=request.user.school) & Q(pk=pk))

        expense_catagory_edit_form = forms.ExpenseCatagoryEditForm(request.POST or None, instance=office_model.ExpenseCatagory.objects.get(Q(pk=pk) & Q(school=request.user.school)))

        if expense_catagory_edit_form.is_valid():
            expense_catagory_edit_form.save()

        variables = {
            'catagories': catagories,
            'expense_catagory_edit_form': expense_catagory_edit_form,
        }

        return render(request, self.template_name, variables)



#expense catagory delete
class ExpenseCatagoryDelete(OfficePermissionMixin, View):
    template_name = 'office/expense-catagory-delete.html'

    def get(self, request, pk):
        get_object_or_404(office_model.ExpenseCatagory, pk=pk)

        catagories = office_model.ExpenseCatagory.objects.filter(Q(school=request.user.school) & Q(pk=pk))

        viewable_catagory = False
        if catagories:
            viewable_catagory = catagories

        variables = {
            'viewable_catagory': viewable_catagory,
        }

        return render(request, self.template_name, variables)

    def post(self, request, pk):
        get_object_or_404(office_model.ExpenseCatagory, pk=pk)

        catagories = office_model.ExpenseCatagory.objects.filter(Q(school=request.user.school) & Q(pk=pk))

        viewable_catagory = False
        if catagories:
            viewable_catagory = catagories

            if request.POST.get('yes') == 'yes':
                catagory_id = request.POST.get('catagory_id')

                catagory_obj = office_model.ExpenseCatagory.objects.get(id=catagory_id)
                catagory_obj.delete()

                return redirect('office:expense-catagory-view')

            elif request.POST.get('no') == 'no':
                return redirect('office:expense-catagory-view')

        variables = {
            'viewable_catagory': viewable_catagory,
        }

        return render(request, self.template_name, variables)



#expense entr
class ExpenseEntry(OfficePermissionMixin, View):
    template_name = 'office/expense-entry.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        pass



#expense create
class ExpenseCreate(OfficePermissionMixin, View):
    template_name = 'office/expense-create.html'

    def get(self, request):
        expense_create_form = forms.ExpenseForm(request=request)

        variables = {
            'expense_create_form': expense_create_form,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        expense_create_form = forms.ExpenseForm(request.POST or None, request=request)

        if expense_create_form.is_valid():
            expense_create_form.deploy()

        variables = {
            'expense_create_form': expense_create_form,
        }

        return render(request, self.template_name, variables)


#office expense:::expense list
class ExpenseList(OfficePermissionMixin, View):
    template_name = 'office/expense-list.html'

    def get(self, request):

        expense_catagory = office_model.ExpenseCatagory.objects.filter(Q(school=request.user.school)).all()

        variables = {
            'expense_catagory': expense_catagory,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        pass


#office expense:::expense list details
class ExpenseListDetail(OfficePermissionMixin, View):
    template_name = 'office/expense-list-details.html'

    def get(self, request, catagory):

        expenses = office_model.Expense.objects.filter(Q(school=request.user.school) & Q(catagory__name=catagory)).all()

        variables = {
            'expenses': expenses,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        pass


#office expense:::expense details
class ExpenseDetail(OfficePermissionMixin, View):
    template_name = 'office/expense-detail.html'

    def get(self, request, pk):
        get_object_or_404(office_model.Expense, pk=pk)

        expenses = office_model.Expense.objects.filter(Q(school=request.user.school) & Q(pk=pk)).all()

        variables = {
            'expenses': expenses,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        pass



#office expense:::edit
class ExpenseEdit(OfficePermissionMixin, View):
    template_name = 'office/expense-edit.html'

    def get(self, request, pk):
        get_object_or_404(office_model.Expense, pk=pk)

        catagories = office_model.Expense.objects.filter(Q(school=request.user.school) & Q(pk=pk))

        expense_edit_form = forms.ExpenseEditForm(request=request, instance=office_model.Expense.objects.get(Q(pk=pk) & Q(school=request.user.school)))

        variables = {
            'catagories': catagories,
            'expense_edit_form': expense_edit_form,
        }

        return render(request, self.template_name, variables)

    def post(self, request, pk):
        get_object_or_404(office_model.Expense, pk=pk)

        catagories = office_model.Expense.objects.filter(Q(school=request.user.school) & Q(pk=pk))

        expense_edit_form = forms.ExpenseEditForm(request.POST or None, request=request, instance=office_model.Expense.objects.get(Q(pk=pk) & Q(school=request.user.school)))

        if expense_edit_form.is_valid():
            expense_edit_form.save()

        variables = {
            'catagories': catagories,
            'expense_edit_form': expense_edit_form,
        }

        return render(request, self.template_name, variables)



#expense delete
class ExpenseDelete(OfficePermissionMixin, View):
    template_name = 'office/expense-delete.html'

    def get(self, request, pk):
        get_object_or_404(office_model.Expense, pk=pk)

        expense = office_model.Expense.objects.filter(Q(school=request.user.school) & Q(pk=pk))

        viewable_expense = False
        if expense:
            viewable_expense = expense

        variables = {
            'viewable_expense': viewable_expense,
        }

        return render(request, self.template_name, variables)

    def post(self, request, pk):
        get_object_or_404(office_model.Expense, pk=pk)

        expense = office_model.Expense.objects.filter(Q(school=request.user.school) & Q(pk=pk))

        viewable_expense = False
        if expense:
            viewable_expense = expense

            if request.POST.get('yes') == 'yes':
                expense_id = request.POST.get('expense_id')

                expense_obj = office_model.Expense.objects.get(id=expense_id)
                expense_obj.delete()

                return redirect('office:expense-list')

            elif request.POST.get('no') == 'no':
                return redirect('office:expense-list')

        variables = {
            'viewable_expense': viewable_expense,
        }

        return render(request, self.template_name, variables)

#==========================================
#==========================================
#=======end expenses orperation view=======
#==========================================
#==========================================



#==========================================
#==========================================
#========start bus orperation view=========
#==========================================
#==========================================


#bus
class Bus(OfficePermissionMixin, View):
    template_name = 'office/bus.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        pass



#bus create
class BusCreate(OfficePermissionMixin, View):
    template_name = 'office/bus-create.html'

    def get(self, request):
        bus_form = forms.BusForm()

        variables = {
            'bus_form': bus_form,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        bus_form = forms.BusForm(request.POST or None)

        if bus_form.is_valid():
            bus_form.deploy(request)

        variables = {
            'bus_form': bus_form,
        }

        return render(request, self.template_name, variables)



#bus view
class BusView(OfficePermissionMixin, View):
    template_name = 'office/bus-view.html'

    def get(self, request):

        buses = office_model.Bus.objects.filter(Q(school=request.user.school)).all()
        count = office_model.Bus.objects.filter(Q(school=request.user.school)).count()

        variables = {
            'buses': buses,
            'count': count,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        pass



#office bus:::edit
class BusEdit(OfficePermissionMixin, View):
    template_name = 'office/bus-edit.html'

    def get(self, request, pk):
        get_object_or_404(office_model.Bus, pk=pk)

        buses = office_model.Bus.objects.filter(Q(school=request.user.school) & Q(pk=pk))

        bus_edit_form = forms.BusEditForm(instance=office_model.Bus.objects.get(Q(pk=pk) & Q(school=request.user.school)))

        variables = {
            'buses': buses,
            'bus_edit_form': bus_edit_form,
        }

        return render(request, self.template_name, variables)

    def post(self, request, pk):
        get_object_or_404(office_model.Bus, pk=pk)

        catagories = office_model.Bus.objects.filter(Q(school=request.user.school) & Q(pk=pk))

        expense_edit_form = forms.BusEditForm(request.POST or None, instance=office_model.Expense.objects.get(Q(pk=pk) & Q(school=request.user.school)))

        if expense_edit_form.is_valid():
            expense_edit_form.save()

        variables = {
            'catagories': catagories,
            'expense_edit_form': expense_edit_form,
        }

        return render(request, self.template_name, variables)




#bus delete
class BusDelete(OfficePermissionMixin, View):
    template_name = 'office/bus-delete.html'

    def get(self, request, pk):
        get_object_or_404(office_model.Bus, pk=pk)

        buses = office_model.Bus.objects.filter(Q(school=request.user.school) & Q(pk=pk))

        viewable_bus = False
        if buses:
            viewable_bus = buses

        variables = {
            'viewable_bus': viewable_bus,
        }

        return render(request, self.template_name, variables)

    def post(self, request, pk):
        get_object_or_404(office_model.Bus, pk=pk)

        buses = office_model.Bus.objects.filter(Q(school=request.user.school) & Q(pk=pk))

        viewable_bus = False
        if buses:
            viewable_bus = buses

            if request.POST.get('yes') == 'yes':
                bus_id = request.POST.get('bus_id')

                bus_obj = office_model.Bus.objects.get(id=bus_id)
                bus_obj.delete()

                return redirect('office:bus-view')

            elif request.POST.get('no') == 'no':
                return redirect('office:bus-view')

        variables = {
            'viewable_class': viewable_class,
        }

        return render(request, self.template_name, variables)



#==========================================
#==========================================
#=========end bus orperation view==========
#==========================================
#==========================================



#==========================================
#==========================================
#=======start class orperation view========
#==========================================
#==========================================


#class module
class ClassHome(OfficePermissionMixin, View):
    template_name = 'office/class-home.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        pass



#class create
class ClassCreate(OfficePermissionMixin, View):
    template_name = 'office/class-create.html'

    def get(self, request):
        class_form = forms.ClassForm()

        variables = {
            'class_form': class_form,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        class_form = forms.ClassForm(request.POST or None)

        if class_form.is_valid():
            class_form.deploy(request)

        variables = {
            'class_form': class_form,
        }

        return render(request, self.template_name, variables)



#class view
class ClassListView(OfficePermissionMixin, View):
    template_name = 'office/class-list-view.html'

    def get(self, request):

        classes = models.Class.objects.filter(school=request.user.school).all()
        count = models.Class.objects.filter(school=request.user.school).count()

        variables = {
            'classes': classes,
            'count': count,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        pass



#office class:::edit
class ClassListEdit(OfficePermissionMixin, View):
    template_name = 'office/class-list-edit.html'

    def get(self, request, pk):
        get_object_or_404(models.Class, pk=pk)

        classes = models.Class.objects.filter(Q(school=request.user.school) & Q(pk=pk))

        class_edit_form = forms.ClassEditForm(instance=models.Class.objects.get(Q(pk=pk) & Q(school=request.user.school)))

        variables = {
            'classes': classes,
            'class_edit_form': class_edit_form,
        }

        return render(request, self.template_name, variables)

    def post(self, request, pk):
        get_object_or_404(models.Class, pk=pk)

        classes = models.Class.objects.filter(Q(school=request.user.school) & Q(pk=pk))

        class_edit_form = forms.ClassEditForm(request.POST or None, instance=models.Class.objects.get(Q(pk=pk) & Q(school=request.user.school)))

        if class_edit_form.is_valid():
            class_edit_form.save()

        variables = {
            'classes': classes,
            'class_edit_form': class_edit_form,
        }

        return render(request, self.template_name, variables)



#class delete
class ClassListDelete(OfficePermissionMixin, View):
    template_name = 'office/class-list-delete.html'

    def get(self, request, pk):
        get_object_or_404(models.Class, pk=pk)

        classes = models.Class.objects.filter(Q(school=request.user.school) & Q(pk=pk))

        viewable_class = False
        if classes:
            viewable_class = classes

        variables = {
            'viewable_class': viewable_class,
        }

        return render(request, self.template_name, variables)

    def post(self, request, pk):
        get_object_or_404(models.Class, pk=pk)

        classes = models.Class.objects.filter(Q(school=request.user.school) & Q(pk=pk))

        viewable_class = False
        if classes:
            viewable_class = classes

            if request.POST.get('yes') == 'yes':
                class_id = request.POST.get('class_id')

                class_obj = models.Class.objects.get(id=class_id)
                class_obj.delete()

                return redirect('office:class-list-view')

            elif request.POST.get('no') == 'no':
                return redirect('office:class-list-view')

        variables = {
            'viewable_class': viewable_class,
        }

        return render(request, self.template_name, variables)



#==========================================
#==========================================
#========end class orperation view=========
#==========================================
#==========================================




#==========================================
#==========================================
#======start section orperation view=======
#==========================================
#==========================================


#class module
class SectionHome(OfficePermissionMixin, View):
    template_name = 'office/section-home.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        pass


#class module
class SectionClassList(OfficePermissionMixin, View):
    template_name = 'office/section-class-list.html'

    def get(self, request):

        classes = models.Class.objects.filter(school=request.user.school).all()
        count = models.Class.objects.filter(school=request.user.school).count()

        variables = {
            'classes': classes,
            'count': count,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        pass




#class create
class SectionCreate(OfficePermissionMixin, View):
    template_name = 'office/section-create.html'

    def get(self, request, classes):
        section_form = forms.SectionForm()

        variables = {
            'section_form': section_form,
        }

        return render(request, self.template_name, variables)

    def post(self, request, classes):
        section_form = forms.SectionForm(request.POST or None)

        if section_form.is_valid():
            section_form.deploy(request, classes)

        variables = {
            'section_form': section_form,
        }

        return render(request, self.template_name, variables)




#section view
class SectionView(OfficePermissionMixin, View):
    template_name = 'office/section-view.html'

    def get(self, request, classes):

        sections = models.Section.objects.filter(Q(school=request.user.school) & Q(classes__name=classes)).all()
        count = models.Section.objects.filter(Q(school=request.user.school) & Q(classes__name=classes)).count()


        variables = {
            'sections': sections,
            'count': count,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        pass




#office class:::edit
class SectionEdit(OfficePermissionMixin, View):
    template_name = 'office/section-edit.html'

    def get(self, request, pk):
        get_object_or_404(models.Section, pk=pk)

        sections = models.Section.objects.filter(Q(school=request.user.school) & Q(pk=pk))

        section_edit_form = forms.SectionEditForm(instance=models.Section.objects.get(Q(pk=pk) & Q(school=request.user.school)))

        variables = {
            'sections': sections,
            'section_edit_form': section_edit_form,
        }

        return render(request, self.template_name, variables)

    def post(self, request, pk):
        get_object_or_404(models.Section, pk=pk)

        sections = models.Section.objects.filter(Q(school=request.user.school) & Q(pk=pk))

        section_edit_form = forms.SectionEditForm(request.POST or None, instance=models.Section.objects.get(Q(pk=pk) & Q(school=request.user.school)))

        if section_edit_form.is_valid():
            section_edit_form.save()

        variables = {
            'sections': sections,
            'section_edit_form': section_edit_form,
        }

        return render(request, self.template_name, variables)




#section delete
class SectionDelete(OfficePermissionMixin, View):
    template_name = 'office/section-delete.html'

    def get(self, request, pk):
        get_object_or_404(models.Section, pk=pk)

        sections = models.Section.objects.filter(Q(school=request.user.school) & Q(pk=pk))

        viewable_section = False
        if sections:
            viewable_section = sections

        variables = {
            'viewable_section': viewable_section,
        }

        return render(request, self.template_name, variables)

    def post(self, request, pk):
        get_object_or_404(models.Section, pk=pk)

        sections = models.Section.objects.filter(Q(school=request.user.school) & Q(pk=pk))

        viewable_section = False
        if sections:
            viewable_section = sections

            if request.POST.get('yes') == 'yes':
                section_id = request.POST.get('section_id')

                section_obj = models.Section.objects.get(id=section_id)
                section_obj.delete()

                return redirect('office:section-class-list')

            elif request.POST.get('no') == 'no':
                return redirect('office:section-class-list')

        variables = {
            'viewable_section': viewable_section,
        }

        return render(request, self.template_name, variables)




#==========================================
#==========================================
#=======end section orperation view========
#==========================================
#==========================================




#==========================================
#==========================================
#======start subject orperation view=======
#==========================================
#==========================================


#class module
class Subject(OfficePermissionMixin, View):
    template_name = 'office/subject.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        pass


#class module
class SubjectClassList(OfficePermissionMixin, View):
    template_name = 'office/subject-class-list.html'

    def get(self, request):

        classes = models.Class.objects.filter(Q(school=request.user.school)).all()
        count = models.Class.objects.filter(Q(school=request.user.school)).count()

        variables = {
            'classes': classes,
            'count': count,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        pass



#subject create
class SubjectCreate(OfficePermissionMixin, View):
    template_name = 'office/subject-create.html'

    def get(self, request, classes):
        subject_form = forms.SubjectForm()

        variables = {
            'subject_form': subject_form,
        }

        return render(request, self.template_name, variables)

    def post(self, request, classes):
        subject_form = forms.SubjectForm(request.POST or None)

        if subject_form.is_valid():
            subject_form.deploy(request, classes)

        variables = {
            'subject_form': subject_form,
        }

        return render(request, self.template_name, variables)




#class module
class SubjectView(OfficePermissionMixin, View):
    template_name = 'office/subject-list.html'

    def get(self, request, classes):

        subjects = models.Subject.objects.filter(Q(school=request.user.school) & Q(classes__name=classes)).all()
        count = models.Subject.objects.filter(Q(school=request.user.school) & Q(classes__name=classes)).count()


        variables = {
            'subjects': subjects,
            'count': count,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        pass




#office subject:::edit
class SubjectEdit(OfficePermissionMixin, View):
    template_name = 'office/subject-edit.html'

    def get(self, request, pk):
        get_object_or_404(models.Subject, pk=pk)

        subjects = models.Subject.objects.filter(Q(school=request.user.school) & Q(pk=pk))

        subject_edit_form = forms.SubjectEditForm(instance=models.Subject.objects.get(Q(pk=pk) & Q(school=request.user.school)))

        variables = {
            'subjects': subjects,
            'subject_edit_form': subject_edit_form,
        }

        return render(request, self.template_name, variables)

    def post(self, request, pk):
        get_object_or_404(models.Subject, pk=pk)

        subjects = models.Subject.objects.filter(Q(school=request.user.school) & Q(pk=pk))

        subject_edit_form = forms.SubjectEditForm(request.POST or None, instance=models.Subject.objects.get(Q(pk=pk) & Q(school=request.user.school)))

        if subject_edit_form.is_valid():
            subject_edit_form.save()

        variables = {
            'subjects': subjects,
            'subject_edit_form': subject_edit_form,
        }

        return render(request, self.template_name, variables)



#subject delete
class SubjectDelete(OfficePermissionMixin, View):
    template_name = 'office/subject-delete.html'

    def get(self, request, pk):
        get_object_or_404(models.Subject, pk=pk)

        subjects = models.Subject.objects.filter(Q(school=request.user.school) & Q(pk=pk))

        viewable_subject = False
        if subjects:
            viewable_subject = subjects

        variables = {
            'viewable_subject': viewable_subject,
        }

        return render(request, self.template_name, variables)

    def post(self, request, pk):
        get_object_or_404(models.Subject, pk=pk)

        subjects = models.Subject.objects.filter(Q(school=request.user.school) & Q(pk=pk))

        viewable_subject = False
        if subjects:
            viewable_subject = subjects

            if request.POST.get('yes') == 'yes':
                subject_id = request.POST.get('subject_id')

                subject_obj = models.Subject.objects.get(id=subject_id)
                subject_obj.delete()

                return redirect('office:subject-class-list')

            elif request.POST.get('no') == 'no':
                return redirect('office:subject-class-list')

        variables = {
            'viewable_subject': viewable_subject,
        }

        return render(request, self.template_name, variables)


#==========================================
#==========================================
#=======end subject orperation view========
#==========================================
#==========================================



#user profile update
class Profile(OfficePermissionMixin, View):
    template_name = 'office/profile.html'

    def get(self, request):

        pp_change_form = forms.ProfilePictureUploadForm()
        info_change_form = forms.ProfileUpdateForm(instance=models.UserProfile.objects.get(id=request.user.id))

        variables = {
            'pp_change_form': pp_change_form,
            'info_change_form': info_change_form,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        pp_change_form = forms.ProfilePictureUploadForm(request.POST or None, request.FILES, instance=models.UserProfile.objects.get(id=request.user.id))
        info_change_form = forms.ProfileUpdateForm(request.POST or None, instance=models.UserProfile.objects.get(id=request.user.id))

        if request.POST.get('pp_change') == 'pp_change':
            if pp_change_form.is_valid():
                pp_change_form.save()


        if request.POST.get('info_change') == 'info_change':
            if info_change_form.is_valid():
                info_change_form.save()
                return redirect('office:profile')


        variables = {
            'pp_change_form': pp_change_form,
            'info_change_form': info_change_form,
        }

        return render(request, self.template_name, variables)



#change password
class ChangePassword(OfficePermissionMixin, View):
    template_name = 'office/change-password.html'

    def get(self, request):
        change_password_form = forms.ChangePasswordForm(request.user)

        variables = {
            'change_password_form': change_password_form,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        change_password_form = forms.ChangePasswordForm(data=request.POST or None, user=request.user)

        if change_password_form.is_valid():
            change_password_form.save()
            update_session_auth_hash(request, change_password_form.user)

            return redirect('office:profile')

        variables = {
            'change_password_form': change_password_form,
        }

        return render(request, self.template_name, variables)
