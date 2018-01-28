from django import forms
from . import models
from django.contrib.auth import authenticate


import re
from django.utils.timezone import now


#user registration form
class RegistrationForm(forms.Form):
    member_type = forms.ModelChoiceField(models.AvailableUser.objects.filter(name='office'))
    school = forms.ModelChoiceField(models.School.objects.all(), required=False)
    username = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate', 'id': 'icon_prefix'}))
    name = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate', 'id': 'icon_prefix'}))
    email = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate', 'id': 'email'}))
    phone = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate', 'id': 'icon_prefix'}))
    address = forms.CharField( required=False, max_length= 10000 ,widget=forms.Textarea )
    account_type = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate', 'id': 'icon_prefix'}))
    password1 = forms.CharField(max_length=20, required=False, widget=forms.PasswordInput(attrs={'class': 'validate', 'id': 'email'}))
    password2 = forms.CharField(max_length=20, required=False, widget=forms.PasswordInput(attrs={'class': 'validate', 'id': 'password'}))
    photo = forms.ImageField(required=False)


    def clean(self):
        member_type = self.cleaned_data.get('member_type')
        school = self.cleaned_data.get('school')
        username = self.cleaned_data.get('username')
        name = self.cleaned_data.get('name')
        email = self.cleaned_data.get('email')
        phone = self.cleaned_data.get('phone')
        address = self.cleaned_data.get('address')
        account_type = self.cleaned_data.get('account_type')
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        photo = self.cleaned_data.get('photo')

        if len(username) < 1:
            raise forms.ValidationError("Enter username!")
        else:
            user_exist = models.UserProfile.objects.filter(username__iexact=username).exists()
            if user_exist:
                raise forms.ValidationError("Username already taken!")
            else:
                if len(email) < 1:
                    raise forms.ValidationError("Enter email address!")
                else:
                    email_correction = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)
                    if email_correction == None:
                        raise forms.ValidationError("Email not correct!")
                    else:
                        email_exist = models.UserProfile.objects.filter(email__iexact=email).exists()
                        if email_exist:
                            raise forms.ValidationError("Email already exist!")
                        else:
                            if len(password1) < 8:
                                raise forms.ValidationError("Password is too short!")
                            else:
                                if password1 != password2:
                                    raise forms.ValidationError("Password not matched!")

    def registration(self):
        member_type = self.cleaned_data.get('member_type')
        school = self.cleaned_data.get('school')
        username = self.cleaned_data.get('username')
        name = self.cleaned_data.get('name')
        email = self.cleaned_data.get('email')
        phone = self.cleaned_data.get('phone')
        address = self.cleaned_data.get('address')
        account_type = self.cleaned_data.get('account_type')
        password1 = self.cleaned_data.get('password1')
        photo = self.cleaned_data.get('photo')

        user = models.UserProfile.objects.create_user(username=username, email=email, name=name, phone=phone, address=address, school=school, photo=photo)
        user.set_password(password1)

        #if official set account type 'admin' or 'superuser'
        if account_type == 'admin' or account_type == 'superuser':
            user.is_staff = True
            user.is_superuser = True
        else:
            pass

        user.member_type = member_type
        user.last_login = now()

        user.save()


#login form
class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'validate', 'id': 'icon_prefix',}))
    password = forms.CharField(max_length=20, required=False, widget=forms.PasswordInput(attrs={'class': 'validate', 'id': 'password'}))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if len(username) < 1:
            raise forms.ValidationError("Enter Username!")
        else:
            if len(password) < 8:
                raise forms.ValidationError("Password is too short!")
            else:
                user = authenticate(username=username, password=password)
                if not user or not user.is_active:
                    raise forms.ValidationError("Username or Password not matched!")
        return self.cleaned_data

    def login(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user
