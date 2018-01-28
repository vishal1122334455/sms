from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.views import login, logout

from . import forms

#logout
def logout_request(request):
    logout(request)
    return redirect('account:login')


#registration functionality
class Registration(View):
    template_name = 'account/registration.html'

    def get(self, request):
        regForm = forms.RegistrationForm()

        variables = {
            'regForm': regForm,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        regForm = forms.RegistrationForm(request.POST or None, request.FILES)

        if regForm.is_valid():
            regForm.registration()

        variables = {
            'regForm': regForm,
        }

        return render(request, self.template_name, variables)


class Login(View):
    template_name = 'account/login.html'

    def get(self, request):
        loginForm = forms.LoginForm()

        variables = {
            'loginForm': loginForm,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        loginForm = forms.LoginForm(request.POST or None)

        if loginForm.is_valid():
            user = loginForm.login()
            if user:
                login(request, user)
                return redirect('administration:home')

        variables = {
            'loginForm': loginForm,
        }

        return render(request, self.template_name, variables)


#registration for teacher
#class RegistrationTeacher(View):
 #   pass
