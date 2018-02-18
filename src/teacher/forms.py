from django import forms
from . import models
from django.db.models import Q
import re

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



#create notice
class NoticeForm(forms.Form):
    def __init__(self,*args,**kwargs):
        self.request = kwargs.pop('request')
        super(NoticeForm, self).__init__(*args,**kwargs)

        self.fields['classes'].queryset = account_model.Class.objects.filter(Q(school=self.request.user.school))


    classes = forms.ModelChoiceField(queryset=account_model.Class.objects.all(), required=False,widget=forms.Select(attrs={'class':'input-field browser-default'}))
    title = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate'}))
    description = forms.CharField( required=False, max_length= 1000 ,widget=forms.Textarea(attrs={'class': 'validate materialize-textarea'}) )


    def clean(self):
        classes = self.cleaned_data.get('classes')
        title = self.cleaned_data.get('title')
        description = self.cleaned_data.get('description')

        if classes == None:
            raise forms.ValidationError('Select Class!')
        else:
            if len(title) == 0:
                raise forms.ValidationError('Write Title!')
            else:
                if len(description) == 0:
                    raise forms.ValidationError('Write description!')

    def deploy(self, request):
        classes = self.cleaned_data.get('classes')
        title = self.cleaned_data.get('title')
        description = self.cleaned_data.get('description')

        deploy = models.Notice(school=request.user.school, classes=classes, user=request.user, title=title, description=description)
        deploy.save()



#edit notice
class NoticeEditForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        self.request = kwargs.pop('request')
        super(NoticeEditForm, self).__init__(*args,**kwargs)

        self.fields['classes'].queryset = account_model.Class.objects.filter(Q(school=self.request.user.school))


    classes = forms.ModelChoiceField(queryset=account_model.Class.objects.all(), required=False,widget=forms.Select(attrs={'class':'input-field browser-default'}))
    title = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate'}))
    description = forms.CharField( required=False, max_length= 1000 ,widget=forms.Textarea(attrs={'class': 'validate materialize-textarea'}) )


    class Meta:
        model = models.Notice
        fields = ('classes', 'title', 'description')



# notice search form
class NoticeSearchForm(forms.Form):
    search_text = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate'}))

    def clean(self):
        search_text = self.cleaned_data.get('search_text')

    def search(self, request):
        search_text = self.cleaned_data.get('search_text')

        count = models.Notice.objects.filter(Q(id=search_text) & Q(school=request.user.school)).count()
        query = models.Notice.objects.filter(Q(id=search_text) & Q(school=request.user.school)).all()

        return query, count





#student search form
class SearchForm(forms.Form):
    search_text = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate'}))

    def clean(self):
        search_text = self.cleaned_data.get('search_text')

    def identify_username_or_email(self, search_text):
        is_email = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', search_text)

        if is_email:
            type = 'email'
        else:
            type = 'username'

        return type


    def search(self, request):
        search_text = self.cleaned_data.get('search_text')

        #admin school id for search in same school
        admin_school_id = request.user.school.id

        check_email_or_username = self.identify_username_or_email(search_text)

        count = None
        query = None
        if check_email_or_username == 'email':
            count = account_model.UserProfile.objects.filter(Q(email__contains=search_text) & Q(school__id=admin_school_id) & Q(member_type__name='student')).count()
            query = account_model.UserProfile.objects.filter(Q(email__contains=search_text) & Q(school__id=admin_school_id) & Q(member_type__name='student')).all()
        elif check_email_or_username == 'username':
            count = account_model.UserProfile.objects.filter(Q(username__contains=search_text) & Q(school__id=admin_school_id) & Q(member_type__name='student')).count()
            query = account_model.UserProfile.objects.filter(Q(username__contains=search_text) & Q(school__id=admin_school_id) & Q(member_type__name='student')).all()

        return query, count
