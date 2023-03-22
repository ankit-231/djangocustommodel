from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from .forms import *
from .models import *
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail, EmailMessage, get_connection
from mycustomuser.settings import EMAIL_HOST_USER


# Create your views here.

def home_page(request):
    return HttpResponse("<h1>This is homepage</h1>")

def register_page(request):
    if request.method == "POST":
        if request.POST['role'] == "student":
            print(request.POST)
            form = StudentForm(request.POST)
            print("before valid")
            # is_valid is a function so is_valid()
            if form.is_valid():
                print("stu form valid")
                print(form)
                # form.username=request.POST.get('username')
                print(form.cleaned_data['email'])
                form.save()
                print("saved")

                user = CustomUser.objects.create_user(username=form.cleaned_data['username'], email=form.cleaned_data['email'], password=form.cleaned_data['password'], role="student")
                user.save()

                # saving user foreign key in s_u_id
                t = StudentsNew.objects.get(username=form.cleaned_data['username'])
                t.s_u_id = user
                t.save()

                print("user saved")
            # print("this stu")
        else:
            print(request.POST)
            form = TeacherForm(request.POST)
            print("before valid")
            # is_valid is a function so is_valid()
            if form.is_valid():
                print("tea form valid")
                print(form)
                # form.username=request.POST.get('username')
                print(form.cleaned_data['email'])
                form.save()
                print("saved")

                user = CustomUser.objects.create_user(username=form.cleaned_data['username'], email=form.cleaned_data['email'], password=form.cleaned_data['password'], role="teacher")
                user.save()
                print(user.role)

                # saving user foreign key in s_u_id
                t = TeachersNew.objects.get(username=form.cleaned_data['username'])
                t.t_u_id = user
                t.save()

                print("user saved")
    
        return render(request, "studentform.html", {"form": form})
    else:
        form = StudentForm()
        return render(request, "studentform.html", {"form": form})


    

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            print(user)
            if user is not None:
                login(request=request, user=user)
                print("loggedin")

                return redirect('/users/home/')
            else:
                print("not loggedin")

                messages.error(request, "Invalid username or password.")
        else:
            print("form invalid")
            messages.error(request, "Invalid username or password.")
    
    else:
        form = AuthenticationForm()

    return render(request, "loginform.html", {"form": form})

def home(request):
    return render(request, "home.html")

def logout_view(request):
    logout(request)
    return redirect('/users/login/')

def myprofile(request):
    return render(request, "profile.html")
     

def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        print(form)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/users/home/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'passwordchangeform.html', {
        'form': form
    })

from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
# from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            user = CustomUser.objects.filter(Q(email=data))
            if user.exists():
                subject = "Password Reset Requested"
                email_template_name = "password/password_reset_email.txt"
                c = {
                "email":user.email,
                'domain':'127.0.0.1:8000',
                'site_name': 'Website',
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "user": user,
                'token': default_token_generator.make_token(user),
                'protocol': 'http',
                }
                email = render_to_string(email_template_name, c)
                try:
                    send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                return redirect ("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="password/password_reset.html", context={"password_reset_form":password_reset_form})

def send_mail_try(request):
    # message = f'Hi testing, thank you for registering in geeksforgeeks.'
    # email = 'try231things@gmail.com'
    # subject = 'welcome to GFG world'
    # body= "testuing"
    # recipient_list = ["twarinxteslt@gmail.com", "sslicedbreadd@gmail.com", ]
    # try:
    #     send_mail(subject, message, from_email=email, recipient_list=recipient_list, connection=get_connection(username='try231things@gmail.com',
    #     password="qljxdoiikixhprfr") , connection=get_connection(username="try231things@gmail.com", password="qljxdoiikixhprfr"), fail_silently=False )
    #     print("Sent")
    # except Exception as e:
    #      print(e, "not sent")
    
    return HttpResponse("this page is not made, go back")

def add_user(request):
    if request.method == "POST":
        try:
            print("aa")
            user = CustomUser.objects.create_user(username=request.POST['username'], email=request.POST['email'], password=request.POST['password'], role="admin")
            
            print("aaa")
            print(user.id)
            messages.success(request, "user saved." )
        except Exception as e:
            print(e)
            print("bbb")
            messages.error(request, "user not saved. make sure you've entered all fields and username is unique" )
    
    return render(request, "adduser.html", {})

def create_grade_level(request):
    if request.method == 'POST':
        form = CreateGradeLevelForm(request.POST)
        gradelevel = GradeLevel.objects.filter(gradelevel_name=request.POST["gradelevel_name"])
        if  gradelevel.exists():
            print("grade exists")
            return HttpResponse("grade not saved, it already exists")
        else:
            if form.is_valid():
                print("cr grade valid")
                gradelevel = GradeLevel.objects.filter(gradelevel_name=form.cleaned_data["gradelevel_name"])
                print(gradelevel)
                form.save()
                print("grade saved")
                return HttpResponse("grade saved")
        return render(request, "gradelevel.html", {'form': form})
    else:
        form = CreateGradeLevelForm()
        return render(request, "gradelevel.html", {'form': form})
    
def create_section(request):
    if request.method == 'POST':
        form = CreateSectionForm(request.POST)
        print(form)
        sectionname_ = Section.objects.filter(sectionname=request.POST["sectionname"])
        if sectionname_.exists():
            print("section exists")
            return HttpResponse("section not saved, it already exists")
        else:
            if form.is_valid():
                print("section valid")
                print(sectionname_)
                form.save()
                print("section saved")
                return HttpResponse("section saved")
        return render(request, "section.html", {'form': form, 'gradelevels': GradeLevel.objects.all()})
    else:
        form = CreateSectionForm()
        return render(request, "section.html", {'form': form, 'gradelevels': GradeLevel.objects.all()})




def addstdtosec(request):
    students = StudentsNew.objects.all()
    sections = Section.objects.all()
    if request.method == "POST":
        print("lol")
        print(request.POST)
        st = StudentsNew.objects.get(username=request.POST["sel_student"])
        print(Section.objects.get(id=request.POST["sel_section"]))
        st.section = Section.objects.get(id=request.POST["sel_section"])
        st.save()
    return render(request, "addstdtosec.html", context={"students":students, "sections":sections, })

def add_teacher_to_grade(request):
    teachers = TeachersNew.objects.all()
    gradelevels = GradeLevel.objects.all()
    if request.method == "POST":
        form = CreateGradeLevelTeacherForm(request.POST)
        print(form)
        if form.is_valid():
            print("valid")
            form.save()
    return render(request, "add_teacher_to_grade.html", context={"teachers": teachers, "gradelevels": gradelevels})

def viewalldata(request):
    users = CustomUser.objects.values('id', 'username', 'email', 'role')
    teachers = TeachersNew.objects.all()
    students = StudentsNew.objects.all()
    gradelevels = GradeLevel.objects.all()
    sections = Section.objects.all()
    return render(request, "viewalldata.html", context={"users":users, "teachers": teachers, "students":students, "gradelevels":gradelevels, "sections":sections, })

def studentviewdata(request):
    students = StudentsNew.objects.all()
    return render(request, "studentviewdata.html", context={"students":students, })

def updatestudentviewdata(request, id):
    student = StudentsNew.objects.get(id=id)
    context = {'students': student,}
    if request.method == "POST":
        fullName = request.POST["fullName"]
        email = request.POST["email"]
        rollno = request.POST["rollno"]
        print(student.fullName)
        print(request.POST["fullName"])
        if not fullName == "":
            student.fullName = request.POST["fullName"]
        if not email == "":
            student.email = request.POST["email"]
        if not rollno == "":
            student.rollno = request.POST["rollno"]
        print(student.fullName)
        student.save()

    return render(request, "updatestudentviewdata.html", context)

def studentdeletedata(request, id):
    student = StudentsNew.objects.get(id=id)
    student.is_deleted = 1
    student.save()
    return redirect("/users/viewalldata/studentviewdata")

def teacherviewdata(request):
    teachers = TeachersNew.objects.all()
    return render(request, "teacherviewdata.html", context={"teachers": teachers, })

def updateteacherviewdata(request, id):
    teacher = TeachersNew.objects.get(id=id)
    context = {'teachers': teacher,}
    
    if request.method == "POST":
        fullName = request.POST["fullName"]
        email = request.POST["email"]
        subject = request.POST["subject"]
        print(teacher.fullName)
        print(request.POST["fullName"])
        if not fullName == "":
            teacher.fullName = request.POST["fullName"]
        if not email == "":
            teacher.email = request.POST["email"]
        if not subject == "":
            teacher.subject = request.POST["subject"]
        print(teacher.fullName)
        teacher.save()

    return render(request, "updateteacherviewdata.html", context)


def gradelevelviewdata(request):
    gradelevels = GradeLevel.objects.all()
    return render(request, "gradelevelviewdata.html", context={"gradelevels":gradelevels, })

def sectionviewdata(request):
    sections = Section.objects.all()
    return render(request, "sectionviewdata.html", context={"sections":sections, })
