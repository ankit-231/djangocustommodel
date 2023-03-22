from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _

from .managers import CustomUserManager

class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'))
    role = models.CharField(_('role'), max_length=250)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ('email',)

    objects = CustomUserManager()

    def __str__(self):
        return self.username



class TeachersNew(models.Model):
    username = models.CharField(max_length=250, unique=True)
    email = models.EmailField(("email address"))
    fullName = models.CharField(max_length=250)
    subject = models.CharField(max_length=250)
    password = models.CharField(max_length=100)
    t_u_id = models.ForeignKey(CustomUser(), on_delete=models.SET_NULL, null=True, blank=True)



class GradeLevel(models.Model):
    gradelevel_name = models.CharField(max_length=250, unique=True)
    fee = models.CharField(max_length=250)
    subjects = models.CharField(max_length=250)


class Section(models.Model):
    sectionname = models.CharField(max_length=250, unique=True)
    total_students_section = models.IntegerField()
    gradelevel_id = models.ForeignKey(GradeLevel(),  on_delete=models.SET_NULL, null=True, blank=True, )

class GradeLevelTeacher(models.Model):
    gradelevel_id = models.ForeignKey( GradeLevel(),  on_delete=models.SET_NULL, null=True, blank=True, )
    teacher_id = models.ForeignKey(TeachersNew(),  on_delete=models.SET_NULL, null=True, blank=True, )

class StudentsNew(models.Model):
    username = models.CharField(max_length=250, unique=True)
    email = models.EmailField(("email address"))
    fullName = models.CharField(max_length=250)
    rollno = models.CharField(max_length=250)
    password = models.CharField(max_length=100)
    is_deleted = models.IntegerField(max_length=1, default=0)
    s_u_id = models.ForeignKey(CustomUser(), on_delete=models.SET_NULL, null=True, blank=True)
    section = models.ForeignKey(Section(), on_delete=models.SET_NULL, null=True, blank=True, )
