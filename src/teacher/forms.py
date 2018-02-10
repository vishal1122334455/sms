from django import forms
from . import models
from django.db.models import Q

from account import models as account_model


#create class test exam time
class ClassTestExamTimeForm(forms.Form):
    exam_name = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate'}))
    date = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate datepicker'}))
    time = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate timepicker'}))

    def clean(self):
        exam_name = self.cleaned_data.get('exam_name')
        date = self.cleaned_data.get('date')
        time = self.cleaned_data.get('time')

        if str(exam_name) == 0:
            forms.ValidationError('Enter Exam Name!')
        else:
            if str(date) == 0:
                raise forms.ValidationError('Select Exam date!')
            else:
                if str(time) == 0:
                    raise forms.ValidationError('Select Exam time!')


    def deploy(self, request, classes, section, subject_id):
        date = self.cleaned_data.get('date')
        time = self.cleaned_data.get('time')

        classes_obj = account_model.Class.objects.get(Q(school=request.user.school) & Q(name=classes))
        section_obj = account_model.Section.objects.get(Q(school=request.user.school) & Q(classes=classes_obj) & Q(name=section))
        subject_obj = account_model.Subject.objects.get(Q(school=request.user.school) & Q(classes=classes_obj) & Q(id=subject_id))

        deploy = models.ClassTestExamTime(school=request.user.school, classes=classes_obj, section=section_obj, subject=subject_obj, teachers=request.user, date=date, time=time)
        deploy.save()

