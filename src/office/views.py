from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.db.models import Q

from administration.views import AdminPermission

from . import forms
from account import models


def check_user(request, pk):
    user_objects = models.UserProfile.objects.filter(pk=pk)

    user_school_id = False
    for user_obj in user_objects:
        user_school_id = user_obj.school.id

    #compare admin school id to requested user school id for same school retrive
    if user_school_id == request.user.school.id:
        return user_objects


#office home page
class Home(AdminPermission, View):
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
class Registration(AdminPermission, View):
    template_name = 'office/registration.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        pass


#member edit view
class MemberSearch(AdminPermission, View):
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
class MemberDetail(AdminPermission, View):
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


class MemberEdit(AdminPermission, View):
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


class MemberDelete(AdminPermission, View):
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
class MemberList(AdminPermission, View):
    template_name = 'office/member-list.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        pass


#office member list detail
class MemberListDetail(AdminPermission, View):
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
class StudentClass(AdminPermission, View):
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
class StudenListInClass(AdminPermission, View):
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
class ClassWiseSection(AdminPermission, View):
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
class SectionWiseStudent(AdminPermission, View):
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
class Schedule(AdminPermission, View):
    template_name = 'office/schedule.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        pass


#==========================================
#==========================================
#======end schedule orperation view========
#==========================================
#==========================================
