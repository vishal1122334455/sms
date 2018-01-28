from django.shortcuts import render, HttpResponse
from django.views import View


class Registration(View):
    template_name = 'account/registration.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        pass
