from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")
    emp_num = forms.CharField(max_length=6, label="직번")
    department = forms.CharField(max_length=20, label="부서")
    section = forms.CharField(max_length=20, label="섹션")


    class Meta:
        model = User
        fields = ("username", "email", "emp_num", "department", "section")