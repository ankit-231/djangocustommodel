from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm

from .models import *

from django import forms


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username',)

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username',)

class StudentForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = StudentsNew
        fields = ['username', 'fullName', 'email', 'rollno']

class TeacherForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = TeachersNew
        fields = ['username', 'fullName', 'email', 'subject', ]

class CreateGradeLevelForm(ModelForm):
    class Meta:
        model = GradeLevel
        fields = ['gradelevel_name', 'fee', 'subjects', ]

class CreateSectionForm(ModelForm):
    class Meta:
        model = Section
        fields = ["sectionname", "total_students_section", "gradelevel_id", ]
class CreateGradeLevelTeacherForm(ModelForm):
    class Meta:
        model = GradeLevelTeacher
        fields = ["gradelevel_id", "teacher_id", ]


# class ChangePasswordOwn(ModelForm):
#     old_password = forms.CharField(
#         label=("Old password"),
#         strip=False,
#         widget=forms.PasswordInput(
#             attrs={"autocomplete": "current-password", "autofocus": True}
#         ),
#     )

#     class Meta:
#         model = CustomUser
#         fields = []

#     new_password1 = 