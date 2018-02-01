from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.hashers import make_password

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
