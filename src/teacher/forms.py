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
        exam_name = self.cleaned_data.get('exam_name')
        date = self.cleaned_data.get('date')
        time = self.cleaned_data.get('time')

        classes_obj = account_model.Class.objects.get(Q(school=request.user.school) & Q(name=classes))
        section_obj = account_model.Section.objects.get(Q(school=request.user.school) & Q(classes=classes_obj) & Q(name=section))
        subject_obj = account_model.Subject.objects.get(Q(school=request.user.school) & Q(classes=classes_obj) & Q(id=subject_id))

        deploy = models.ClassTestExamTime(school=request.user.school, classes=classes_obj, section=section_obj, subject=subject_obj, teachers=request.user, exam_name=exam_name, date=date, time=time)
        deploy.save()




#edit class test exam time
class EditClassTestExamTimeForm(forms.ModelForm):
    exam_name = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate'}))
    date = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate datepicker'}))
    time = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate timepicker'}))

    class Meta:
        model = models.ClassTestExamTime
        fields = ('exam_name', 'date', 'time', )



#publish exam marks
class ClassTestExamMarkForm(forms.Form):
    def __init__(self,*args,**kwargs):
        self.request = kwargs.pop('request')
        self.classes = kwargs.pop('classes')
        self.section = kwargs.pop('section')
        self.subject = kwargs.pop('subject')
        self.exam = kwargs.pop('exam')
        super(ClassTestExamMarkForm, self).__init__(*args,**kwargs)


    roll = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate'}))
    mark = forms.FloatField(required=False, widget=forms.TextInput(attrs={'class': 'validate'}))


    def clean(self):
        roll = self.cleaned_data.get('roll')
        mark = self.cleaned_data.get('mark')


        if roll == None:
            raise forms.ValidationError('Enter Student roll!')
        else:
            roll_exists = account_model.UserProfile.objects.filter(Q(school=self.request.user.school) & Q(classes__name=self.classes) & Q(section__name=self.section) & Q(student__roll=roll)).exists()

            if not roll_exists:
                raise forms.ValidationError('Enter Valid Roll!')
            else:
                if mark == None:
                    raise forms.ValidationError('Enter Marks!')
                else:
                    student_obj = account_model.UserProfile.objects.get(Q(school=self.request.user.school) & Q(classes__name=self.classes) & Q(section__name=self.section) & Q(student__roll=roll))

                    student_exist_in_exam_marks = models.ClassTestExamMark.objects.filter(Q(school=self.request.user.school) & Q(classes__name=self.classes) & Q(section__name=self.section) & Q(subject__id=self.subject) & Q(exam__id=self.exam) & Q(student=student_obj)).exists()

                    if student_exist_in_exam_marks:
                        raise forms.ValidationError('This student marks for this exam is allready exists!')




    def deploy(self):
        roll = self.cleaned_data.get('roll')
        mark = self.cleaned_data.get('mark')

        classes_obj = account_model.Class.objects.get(Q(school=self.request.user.school) & Q(name=self.classes))
        section_obj = account_model.Section.objects.get(Q(school=self.request.user.school) & Q(classes=classes_obj) & Q(name=self.section))
        subject_obj = account_model.Subject.objects.get(Q(school=self.request.user.school) & Q(classes=classes_obj) & Q(id=self.subject))

        student_obj = account_model.UserProfile.objects.get(Q(school=self.request.user.school) & Q(classes__name=self.classes) & Q(section__name=self.section) & Q(student__roll=roll))

        exam_obj = models.ClassTestExamTime.objects.get(id=self.exam)


        deploy = models.ClassTestExamMark(school=self.request.user.school, classes=classes_obj, section=section_obj, subject=subject_obj, teachers=self.request.user, student=student_obj, exam=exam_obj, mark=mark)

        deploy.save()



#edit exam marks
class EditClassTestExamMarkForm(forms.ModelForm):
    mark = forms.FloatField(required=False, widget=forms.TextInput(attrs={'class': 'validate'}))


    class Meta:
        model = models.ClassTestExamMark
        fields = ('mark', )
