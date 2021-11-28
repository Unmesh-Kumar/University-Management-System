from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User

from .models import Profile
from courses.models import Enrollment, Course


def index(request):
    return render(request, 'pages/index.html')

def about(request):
    return render(request, 'pages/about.html')

def register(request):
  if request.method == 'POST':
    # Get form values
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    password2 = request.POST['password2']
    type = request.POST['type']

    # Check if passwords match
    if password == password2:
      # Check username
      if User.objects.filter(username=username).exists():
        messages.error(request, 'That username is taken')
        return redirect('register')
      else:
        if User.objects.filter(email=email).exists():
          messages.error(request, 'That email is being used')
          return redirect('register')
        else:
          # Looks good
          user = User.objects.create_user(username=username, password=password,email=email, first_name=first_name, last_name=last_name)
          # Login after register
          # auth.login(request, user)
          # messages.success(request, 'You are now logged in')
          # return redirect('index')
          user.save()
          profile= Profile(user=user, type=type)
          profile.save()
          messages.success(request, 'You are now registered and can log in')
          return redirect('login')
    else:
      messages.error(request, 'Passwords do not match')
      return redirect('register')
  else:
    return render(request, 'accounts/register.html')

def login(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']

    user = auth.authenticate(username=username, password=password)

    if user is not None:
      auth.login(request, user)
      messages.success(request, 'You are now logged in')
      return redirect('dashboard')
    else:
      messages.error(request, 'Invalid credentials')
      return redirect('login')
  else:
    return render(request, 'accounts/login.html')

def logout(request):
  if request.method == 'POST':
    auth.logout(request)
    messages.success(request, 'You are now logged out')
    return redirect('index')


def dashboard(request):
    if request.method == 'POST':
        course_name = request.POST['course']
        course = Course.objects.get(course_name=course_name)
        Enrollment(student=request.user, course=course).save()
        messages.success(request, f'You are now registered for {course_name}')
        redirect('dashboard')

    status=True
    if request.user.profile.type == 'professor':
        status=False
        context={'status': status}
        credits= list(range(1,5))
        context['credits']=credits
        taught_courses= Course.objects.filter(professor=request.user)
        context['taught_courses']=taught_courses
    else:
        context={'status': status}
        qs=Enrollment.objects.filter(student=request.user)

        grades =list(range(0,11))
        number={}
        for enr in qs:
          number[enr.grade]=number.get(enr.grade,0)+1

        elem=[]
        for i in grades:
          elem.append((i,number.get(i,0),))
        elem.append((11,0,))


        # print(qs)
        context['qs']=qs
        context['stats']=elem
        context['total_courses']=len(qs)
        total_credits_taken=0
        total_weighted_grade=0

        taken = set()
        for enr in qs:
            taken.add(enr.course.course_name)
            total_credits_taken+=enr.course.credits
            total_weighted_grade+=enr.course.credits*enr.grade

        courses=[]
        for course in Course.objects.all():
            if course.course_name not in taken:
                courses.append(course)

        context['courses']=courses

        overall_grade=0.00
        if total_credits_taken !=0:
          overall_grade=total_weighted_grade/total_credits_taken

        overall_grade="%.2f" % overall_grade

        context['total_credits_taken']=total_credits_taken
        context['total_weighted_grade']=total_weighted_grade
        context['overall_grade']=overall_grade

    return render(request, 'accounts/dashboard.html', context)


def course_addition(request):
    if request.method == 'POST':
        course_name = request.POST['course_name']
        credits = int(request.POST['credits'])
        Course(course_name=course_name, credits=credits, professor=request.user).save()
        messages.success(request, f'Course {course_name} has been successfully added')
        return redirect('dashboard')


def course_detail(request, course_id):
  course = Course.objects.get(id=course_id)
  students= Enrollment.objects.filter(course=course)
  modifiable=course.professor==request.user
  grades =list(range(0,11))
  number={}
  for student in students:
    number[student.grade]=number.get(student.grade,0)+1

  elem=[]
  for i in grades:
    elem.append((i,number.get(i,0),))
  elem.append((11,0,))

  context ={
    'students': students,
    'course': course,
    'modifiable': modifiable,
    'grades': grades,
    'stats': elem,
  }

  return render(request,'accounts/detail.html',context) 


def grade_change(request, enr_id):
  if request.method=='POST':
    new_grade=request.POST['new_grade']
    enr=Enrollment.objects.get(id=enr_id)
    enr.grade=new_grade
    enr.save()
    messages.success(request, f'Grade assigned to {enr.student.first_name} has been successfully changed')
  return redirect('course_detail',course_id=enr.course.id)

