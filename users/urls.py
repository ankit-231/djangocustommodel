from django.urls import path
from django.contrib.auth.views import PasswordChangeView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

from . import views

urlpatterns = [
    path('register/', views.register_page, name='register'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('send_mail_view/', views.send_mail_try, name='send_mail_view'),
    path('myprofile/', views.myprofile, name='myprofile'),

    path('add_user/', views.add_user, name='add_user'),


    path('create_grade_level/', views.create_grade_level, name='create_grade_level'),
    path('create_section/', views.create_section, name='create_section'),

    path('viewalldata/', views.viewalldata, name='viewalldata'),
    path('viewalldata/addstdtosec/', views.addstdtosec, name='addstdtosec'),

    path('viewalldata/studentviewdata', views.studentviewdata, name='studentviewdata'),
    path('viewalldata/studentviewdata/<int:id>', views.updatestudentviewdata, name='updatestudentviewdata'),
    path('viewalldata/studentviewdata/studentdeletedata/<int:id>', views.studentdeletedata, name='studentdeletedata'),

    path('viewalldata/teacherviewdata', views.teacherviewdata, name='teacherviewdata'),
    path("viewalldata/teacherviewdata/<int:id>", views.updateteacherviewdata, name="updateteacherviewdata"),
    path('viewalldata/gradelevelviewdata', views.gradelevelviewdata, name='gradelevelviewdata'),
    path('viewalldata/sectionviewdata', views.sectionviewdata, name='sectionviewdata'),

    path('add_teacher_to_grade', views.add_teacher_to_grade, name='add_teacher_to_grade'),


    path('home/', views.home, name='home'),

    path('password_change/', views.password_change, name='password_change'),

    path("password_reset", views.password_reset_request, name="password_reset"),


]
