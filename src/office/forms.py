from django import forms
from django.db.models import Q

import re

from account import models


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

