from django import forms
from django.db.models import Q

import re

from account import models
from .models import ClassRoutine, ExamRoutine, Notice, GallaryImage, GallaryVideo
from . import models as office_model


#search form
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
            count = models.UserProfile.objects.filter(Q(email__contains=search_text) & Q(school__id=admin_school_id)).count()
            query = models.UserProfile.objects.filter(Q(email__contains=search_text) & Q(school__id=admin_school_id)).all()
        elif check_email_or_username == 'username':
            count = models.UserProfile.objects.filter(Q(username__contains=search_text) & Q(school__id=admin_school_id)).count()
            query = models.UserProfile.objects.filter(Q(username__contains=search_text) & Q(school__id=admin_school_id)).all()

        return query, count


#member edit form
class MemberEditForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        self.request = kwargs.pop('request')
        super(MemberEditForm, self).__init__(*args,**kwargs)
        self.fields['classes'].queryset = models.Class.objects.filter(school=self.request.user.school)
        self.fields['section'].queryset = models.Section.objects.filter(school=self.request.user.school)
        self.fields['school'].queryset = models.School.objects.filter(id=self.request.user.school.id)

    address = forms.CharField( required=False, max_length= 1000 ,widget=forms.Textarea(attrs={'class': 'validate materialize-textarea'}) )
    classes = forms.ModelChoiceField(queryset=models.Class.objects.all(), required=False, widget=forms.Select(attrs={'class':'input-field browser-default'}))
    section = forms.ModelChoiceField(queryset=models.Section.objects.all(), required=False,widget=forms.Select(attrs={'class':'input-field browser-default'}))
    school = forms.ModelChoiceField(queryset=models.School.objects.all(), required=False,widget=forms.Select(attrs={'class':'input-field browser-default'}))

    class Meta:
        model = models.UserProfile
        fields = ('username', 'name', 'email', 'phone', 'address', 'photo', 'school', 'classes', 'section')




#create routine form
day_list = (
        ('sunday', 'Sunday'),
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('saturday', 'Saturday'),)

class CreateRoutineForm(forms.Form):
    def __init__(self,*args,**kwargs):
        self.request = kwargs.pop('request')
        self.classes = kwargs.pop('classes')
        super(CreateRoutineForm, self).__init__(*args,**kwargs)

        self.fields['subject'].queryset = models.Subject.objects.filter(Q(school=self.request.user.school) & Q(classes=self.classes))


    subject = forms.ModelChoiceField(queryset=models.Subject.objects.all(), required=False,widget=forms.Select(attrs={'class':'input-field browser-default'}))
    day = forms.ChoiceField(choices=day_list, required=False, widget=forms.Select(attrs={'class': 'validate browser-default'}))
    period = forms.IntegerField(required=False, widget=forms.TextInput(attrs={'class': 'validate'}))
    start_hour = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate timepicker'}))
    end_hour = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate timepicker'}))

    def clean(self):
        subject = self.cleaned_data.get('subject')
        day = self.cleaned_data.get('day')
        period = self.cleaned_data.get('period')
        start_hour = self.cleaned_data.get('start_hour')
        end_hour = self.cleaned_data.get('end_hour')

        if subject == None:
            raise forms.ValidationError("Select Subject!")
        else:
            if len(start_hour) < 1:
                raise forms.ValidationError('Select Class Start Hour!')
            else:
                if len(end_hour) < 1:
                    raise forms.ValidationError("Select Class End Hour!")


    def deploy(self, section):
        subject = self.cleaned_data.get('subject')
        day = self.cleaned_data.get('day')
        period = self.cleaned_data.get('period')
        start_hour = self.cleaned_data.get('start_hour')
        end_hour = self.cleaned_data.get('end_hour')

        section_obj = models.Section.objects.get(Q(school=self.request.user.school) & Q(classes=self.classes) & Q(name=section))

        deploy = ClassRoutine(school=self.request.user.school, classes=self.classes, section=section_obj, subject=subject, day=day, period=period, start_hour=start_hour, end_hour=end_hour)
        deploy.save()


#routine edit form
class RoutineEditForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        self.request = kwargs.pop('request')
        self.classes = kwargs.pop('classes')
        super(RoutineEditForm, self).__init__(*args,**kwargs)

        self.fields['subject'].queryset = models.Subject.objects.filter(Q(school=self.request.user.school) & Q(classes=self.classes))

    subject = forms.ModelChoiceField(queryset=models.Subject.objects.all(), required=False,widget=forms.Select(attrs={'class':'input-field browser-default'}))
    day = forms.ChoiceField(choices=day_list, required=False, widget=forms.Select(attrs={'class': 'validate browser-default'}))
    period = forms.IntegerField(required=False, widget=forms.TextInput(attrs={'class': 'validate'}))
    start_hour = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate timepicker'}))
    end_hour = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate timepicker'}))

    class Meta:
        model = ClassRoutine
        fields = ('subject', 'day', 'period', 'start_hour', 'end_hour',)


#exam routine create
class CreateExamRoutineForm(forms.Form):
    def __init__(self,*args,**kwargs):
        self.request = kwargs.pop('request')
        self.classes = kwargs.pop('classes')
        super(CreateExamRoutineForm, self).__init__(*args,**kwargs)

        self.fields['subject'].queryset = models.Subject.objects.filter(Q(school=self.request.user.school) & Q(classes=self.classes))


    subject = forms.ModelChoiceField(queryset=models.Subject.objects.all(), required=False,widget=forms.Select(attrs={'class':'input-field browser-default'}))
    exam_name = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate'}))
    date = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate datepicker'}))
    start_hour = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate timepicker'}))
    end_hour = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate timepicker'}))

    def clean(self):
        subject = self.cleaned_data.get('subject')
        exam_name = self.cleaned_data.get('exam_name')
        date = self.cleaned_data.get('date')
        start_hour = self.cleaned_data.get('start_hour')
        end_hour = self.cleaned_data.get('end_hour')

        if subject == None:
            raise forms.ValidationError("Select Subject!")
        else:
            if exam_name == None:
                raise forms.ValidationError('Enter Exam Name!')
            else:
                if date == None:
                    raise forms.ValidationError('Select exam date!')
                else:
                    if len(start_hour) < 1:
                        raise forms.ValidationError('Select Exam Start Hour!')
                    else:
                        if len(end_hour) < 1:
                            raise forms.ValidationError("Select Exam End Hour!")


    def deploy(self):
        subject = self.cleaned_data.get('subject')
        exam_name = self.cleaned_data.get('exam_name')
        date = self.cleaned_data.get('date')
        start_hour = self.cleaned_data.get('start_hour')
        end_hour = self.cleaned_data.get('end_hour')

        deploy = ExamRoutine(school=self.request.user.school, classes=self.classes, subject=subject, exam_name=exam_name, date=date, start_hour=start_hour, end_hour=end_hour)
        deploy.save()


#exam routine edit form
class ExamRoutineEditForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        self.request = kwargs.pop('request')
        self.classes = kwargs.pop('classes')
        super(ExamRoutineEditForm, self).__init__(*args,**kwargs)

        self.fields['subject'].queryset = models.Subject.objects.filter(Q(school=self.request.user.school) & Q(classes=self.classes))

    subject = forms.ModelChoiceField(queryset=models.Subject.objects.all(), required=False,widget=forms.Select(attrs={'class':'input-field browser-default'}))
    exam_name = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate'}))
    date = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate datepicker'}))
    start_hour = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate timepicker'}))
    end_hour = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate timepicker'}))

    class Meta:
        model = ClassRoutine
        fields = ('subject', 'exam_name', 'date', 'start_hour', 'end_hour',)


#create notice
class NoticeForm(forms.Form):
    def __init__(self,*args,**kwargs):
        self.request = kwargs.pop('request')
        super(NoticeForm, self).__init__(*args,**kwargs)

        self.fields['classes'].queryset = models.Class.objects.filter(Q(school=self.request.user.school))


    classes = forms.ModelChoiceField(queryset=models.Class.objects.all(), required=False,widget=forms.Select(attrs={'class':'input-field browser-default'}))
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

        deploy = Notice(school=request.user.school, classes=classes, user=request.user, title=title, description=description)
        deploy.save()



#edit notice
class NoticeEditForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        self.request = kwargs.pop('request')
        super(NoticeEditForm, self).__init__(*args,**kwargs)

        self.fields['classes'].queryset = models.Class.objects.filter(Q(school=self.request.user.school))


    classes = forms.ModelChoiceField(queryset=models.Class.objects.all(), required=False,widget=forms.Select(attrs={'class':'input-field browser-default'}))
    title = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate'}))
    description = forms.CharField( required=False, max_length= 1000 ,widget=forms.Textarea(attrs={'class': 'validate materialize-textarea'}) )


    class Meta:
        model = Notice
        fields = ('classes', 'title', 'description')



# notice search form
class NoticeSearchForm(forms.Form):
    search_text = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate'}))

    def clean(self):
        search_text = self.cleaned_data.get('search_text')

    def search(self, request):
        search_text = self.cleaned_data.get('search_text')

        count = Notice.objects.filter(Q(id=search_text) & Q(school=request.user.school)).count()
        query = Notice.objects.filter(Q(id=search_text) & Q(school=request.user.school)).all()

        return query, count


#gallary image upload form
class GallaryImageForm(forms.Form):
    description = forms.CharField(required=False, max_length=1000, widget=forms.Textarea(attrs={'class': 'validate materialize-textarea'}))
    image = forms.ImageField(required=False)


    def clean(self):
        description = self.cleaned_data.get('description')
        image = self.cleaned_data.get('image')

        if len(description) == 0:
            raise forms.ValidationError('Write Description for this photo!')
        else:
            if image == None:
                raise forms.ValidationError('Choose Image!')


    def deploy(self, request):
        description = self.cleaned_data.get('description')
        image = self.cleaned_data.get('image')

        deploy = GallaryImage(school=request.user.school, user=request.user, description=description, image=image)

        deploy.save()



#gallary video upload form
class GallaryVideoForm(forms.Form):
    description = forms.CharField(required=False, max_length=1000, widget=forms.Textarea(attrs={'class': 'validate materialize-textarea'}))
    video = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate'}))



    def clean(self):
        description = self.cleaned_data.get('description')
        video = self.cleaned_data.get('video')

        if len(description) == 0:
            raise forms.ValidationError('Write Description for this video!')
        else:
            if len(video) == 0:
                raise forms.ValidationError('Enter video url!')


    def deploy(self, request):
        description = self.cleaned_data.get('description')
        video = self.cleaned_data.get('video')

        deploy = GallaryVideo(school=request.user.school, user=request.user, description=description, video=video)

        deploy.save()



#classroom  form
class ClassroomForm(forms.Form):
    description = forms.CharField(required=False, max_length=1000, widget=forms.Textarea(attrs={'class': 'validate materialize-textarea'}))
    room = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate'}))



    def clean(self):
        description = self.cleaned_data.get('description')
        room = self.cleaned_data.get('room')

        if len(description) == 0:
            raise forms.ValidationError('Write Description for this room!')
        else:
            if len(room) == 0:
                raise forms.ValidationError('Enter room number!')


    def deploy(self, request, classes, section):
        description = self.cleaned_data.get('description')
        room = self.cleaned_data.get('room')

        class_obj = models.Class.objects.get(Q(school=request.user.school) & Q(name=classes))
        section_obj = models.Section.objects.get(Q(school=request.user.school) & Q(classes=class_obj) & Q(name=section))

        deploy = office_model.Classroom(school=request.user.school, classes=class_obj, section=section_obj, room=room, description=description)

        deploy.save()


#class room edit form
class ClassroomEditForm(forms.ModelForm):
    description = forms.CharField(required=False, max_length=1000, widget=forms.Textarea(attrs={'class': 'validate materialize-textarea'}))
    room = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate'}))

    class Meta:
        model = office_model.Classroom
        fields = ('description', 'room', )


#event create form
class EventForm(forms.Form):
    title = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate'}))
    description = forms.CharField(required=False, max_length=1000, widget=forms.Textarea(attrs={'class': 'validate materialize-textarea'}))
    start_date = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate datepicker'}))
    end_date = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate datepicker'}))

    def clean(self):
        title = self.cleaned_data.get('title')
        description = self.cleaned_data.get('description')
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')


        if len(title) == 0:
            raise forms.ValidationError('Enter event title!')
        else:
            if len(description) == 0:
                raise forms.ValidationError('Enter description!')
            else:
                if len(start_date) == 0:
                    raise forms.ValidationError('Select event start date!')
                else:
                    if len(end_date) == 0:
                        raise forms.ValidationError('Select event end date!')


    def deploy(self, request):
        title = self.cleaned_data.get('title')
        description = self.cleaned_data.get('description')
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')

        deploy = office_model.Event(school=request.user.school, user=request.user, title=title, description=description, start_date=start_date, end_date=end_date)

        deploy.save()



#event edit form
class EventEditForm(forms.ModelForm):
    title = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate'}))
    description = forms.CharField(required=False, max_length=1000, widget=forms.Textarea(attrs={'class': 'validate materialize-textarea'}))
    start_date = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate datepicker'}))
    end_date = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate datepicker'}))

    class Meta:
        model = office_model.Event
        fields = ('title', 'description', 'start_date', 'end_date')


#expense catagory form
class ExpenseCatagoryForm(forms.Form):
    name = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate'}))
    description = forms.CharField(required=False, max_length=1000, widget=forms.Textarea(attrs={'class': 'validate materialize-textarea'}))


    def clean(self):
        name = self.cleaned_data.get('name')
        description = self.cleaned_data.get('description')

        if len(name) == 0:
            raise forms.ValidationError('Enter Catagory Name!')
        else:
            if len(description) == 0:
                raise forms.ValidationError('Enter catagory description!')


    def deploy(self, request):
        name = self.cleaned_data.get('name')
        description = self.cleaned_data.get('description')

        deploy = office_model.ExpenseCatagory(school=request.user.school, user=request.user, name=name, description=description)

        deploy.save()



#expense catagory Edit form
class ExpenseCatagoryEditForm(forms.ModelForm):
    name = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate'}))
    description = forms.CharField(required=False, max_length=1000, widget=forms.Textarea(attrs={'class': 'validate materialize-textarea'}))

    class Meta:
        model = office_model.ExpenseCatagory
        fields = ('name', 'description', )



#expense form
payment_method = (
        ('cash', 'Cash'),
        ('bank', 'Bank'),
        ('cheque', 'Cheque'),)

class ExpenseForm(forms.Form):
    def __init__(self,*args,**kwargs):
        self.request = kwargs.pop('request')
        super(ExpenseForm, self).__init__(*args,**kwargs)

        self.fields['catagory'].queryset = office_model.ExpenseCatagory.objects.filter(Q(school=self.request.user.school))


    catagory = forms.ModelChoiceField(queryset=office_model.ExpenseCatagory.objects.all(), required=False,widget=forms.Select(attrs={'class':'input-field browser-default'}))
    name = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate'}))
    description = forms.CharField(required=False, max_length=1000, widget=forms.Textarea(attrs={'class': 'validate materialize-textarea'}))
    amount = forms.FloatField(required=False, widget=forms.TextInput(attrs={'class': 'validate'}))
    method = forms.ChoiceField(choices=payment_method, required=False, widget=forms.Select(attrs={'class': 'validate browser-default'}))
    date = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate datepicker'}))

    def clean(self):
        catagory = self.cleaned_data.get('catagory')
        name = self.cleaned_data.get('name')
        description = self.cleaned_data.get('description')
        amount = self.cleaned_data.get('amount')
        method = self.cleaned_data.get('method')
        date = self.cleaned_data.get('date')

        if catagory == None:
            raise forms.ValidationError('Select Expense Catagory!')
        else:
            if len(name) == 0:
                raise forms.ValidationError('Write expense name!')
            else:
                if amount == None:
                    raise forms.ValidationError('Enter expense amount!')
                else:
                    if method == None:
                        raise forms.ValidationError('Select Payment Method!')


    def deploy(self):
        catagory = self.cleaned_data.get('catagory')
        name = self.cleaned_data.get('name')
        description = self.cleaned_data.get('description')
        amount = self.cleaned_data.get('amount')
        method = self.cleaned_data.get('method')
        date = self.cleaned_data.get('date')

        deploy = office_model.Expense(school=self.request.user.school, user=self.request.user, catagory=catagory, name=name, description=description, amount=amount, method=method, date=date)

        deploy.save()



#expense edit form
class ExpenseEditForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        self.request = kwargs.pop('request')
        super(ExpenseEditForm, self).__init__(*args,**kwargs)

        self.fields['catagory'].queryset = office_model.ExpenseCatagory.objects.filter(Q(school=self.request.user.school))


    catagory = forms.ModelChoiceField(queryset=office_model.ExpenseCatagory.objects.all(), required=False,widget=forms.Select(attrs={'class':'input-field browser-default'}))
    name = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate'}))
    description = forms.CharField(required=False, max_length=1000, widget=forms.Textarea(attrs={'class': 'validate materialize-textarea'}))
    amount = forms.FloatField(required=False, widget=forms.TextInput(attrs={'class': 'validate'}))
    method = forms.ChoiceField(choices=payment_method, required=False, widget=forms.Select(attrs={'class': 'validate browser-default'}))
    date = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate datepicker'}))


    class Meta:
        model = office_model.Expense
        fields = ('catagory', 'name', 'description', 'amount', 'method', 'date', )



#bus form
class BusForm(forms.Form):
    name = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate'}))
    bus_route = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate'}))
    driver_name = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate'}))
    driver_phone = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate'}))
    amount = forms.FloatField(required=False, widget=forms.TextInput(attrs={'class': 'validate'}))


    def clean(self):
        name = self.cleaned_data.get('name')
        bus_route = self.cleaned_data.get('bus_route')
        driver_name = self.cleaned_data.get('driver_name')
        driver_phone = self.cleaned_data.get('driver_phone')
        amount = self.cleaned_data.get('amount')


        if len(name) == 0:
            raise forms.ValidationError('Enter Bus Name!')
        else:
            if len(bus_route) == 0:
                raise forms.ValidationError('Enter Bus Route!')
            else:
                if amount == None:
                    raise forms.ValidationError('Enter Amount!')



    def deploy(self, request):
        name = self.cleaned_data.get('name')
        bus_route = self.cleaned_data.get('bus_route')
        driver_name = self.cleaned_data.get('driver_name')
        driver_phone = self.cleaned_data.get('driver_phone')
        amount = self.cleaned_data.get('amount')

        deploy = office_model.Bus(school=request.user.school, name=name, bus_route=bus_route, driver_name=driver_name, driver_phone=driver_phone, amount=amount)
        deploy.save()



#bus edit form
class BusEditForm(forms.ModelForm):
    name = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate'}))
    bus_route = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate'}))
    driver_name = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate'}))
    driver_phone = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate'}))
    amount = forms.FloatField(required=False, widget=forms.TextInput(attrs={'class': 'validate'}))


    class Meta:
        model = office_model.Bus
        fields = ('name', 'bus_route', 'driver_name', 'driver_phone', 'amount', )




#class form
class ClassForm(forms.Form):
    name = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate'}))

    def clean(self):
        name = self.cleaned_data.get('name')

        if len(name) == 0:
            raise forms.ValidationError('Enter class name!')


    def deploy(self, request):
        name = self.cleaned_data.get('name')

        deploy = models.Class(school=request.user.school, name=name)
        deploy.save()



#class edit form
class ClassEditForm(forms.ModelForm):
    name = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate'}))

    class Meta:
        model = models.Class
        fields = ('name', )



#section create
class SectionForm(forms.Form):
    name = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate'}))


    def clean(self):
        name = self.cleaned_data.get('name')

        if len(name) == 0:
            raise forms.ValidationError('Enter Section Name!')


    def deploy(self, request, classes):
        name = self.cleaned_data.get('name')

        classes_obj = models.Class.objects.get(Q(school=request.user.school) & Q(name=classes))

        deploy = models.Section(school=request.user.school, classes=classes_obj, name=name)
        deploy.save()



#section create
class SectionEditForm(forms.ModelForm):
    name = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate'}))


    class Meta:
        model = models.Section
        fields = ('name', )



