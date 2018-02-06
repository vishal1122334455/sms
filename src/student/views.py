from django.shortcuts import render, redirect
from django.views import View


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
