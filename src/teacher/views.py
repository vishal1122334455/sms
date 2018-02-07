from django.shortcuts import render, redirect
from django.views import View


#student dashboard access permission mixin
class TeacherPermissionMixin(object):
    def has_permissions(self, request):
        return request.user.member_type.name == 'teacher'

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permissions(request):
            return redirect('account:login')
        return super(TeacherPermissionMixin, self).dispatch(
            request, *args, **kwargs)



#teacher dashboard
class Home(TeacherPermissionMixin, View):
    template_name = 'teacher/index.html'

    def get(self, request):
        return render(request, self.template_name)
