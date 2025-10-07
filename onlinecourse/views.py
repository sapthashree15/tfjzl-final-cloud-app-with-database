from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.views import generic
from django.contrib.auth.models import User
import logging

# Import your models
from .models import Course, Enrollment, Question, Choice, Submission

logger = logging.getLogger(__name__)


# Registration view
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'onlinecourse/user_registration_bootstrap.html', context)
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']

        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.info("New user")

        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name,
                                            last_name=last_name, password=password)
            login(request, user)
            return redirect("onlinecourse:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'onlinecourse/user_registration_bootstrap.html', context)


# Login view
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('onlinecourse:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'onlinecourse/user_login_bootstrap.html', context)
    else:
        return render(request, 'onlinecourse/user_login_bootstrap.html', context)


# Logout view
def logout_request(request):
    logout(request)
    return redirect('onlinecourse:index')


# Check if enrolled
def check_if_enrolled(user, course):
    if user.id:
        return Enrollment.objects.filter(user=user, course=course).exists()
    return False


# Course list view
class CourseListView(generic.ListView):
    template_name = 'onlinecourse/course_list_bootstrap.html'
    context_object_name = 'course_list'

    def get_queryset(self):
        user = self.request.user
        courses = Course.objects.order_by('-total_enrollment')[:10]
        for course in courses:
            if user.is_authenticated:
                course.is_enrolled = check_if_enrolled(user, course)
            else:
                course.is_enrolled = False
        return courses


# Course detail view
class CourseDetailView(generic.DetailView):
    model = Course
    template_name = 'onlinecourse/course_detail_bootstrap.html'


# Enroll view
def enroll(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user = request.user

    if user.is_authenticated and not check_if_enrolled(user, course):
        Enrollment.objects.create(user=user, course=course, mode='honor')
        course.total_enrollment += 1
        course.save()

    return HttpResponseRedirect(reverse('onlinecourse:course_details', args=(course.id,)))


# Extract answers helper
def extract_answers(request):
    submitted_answers = []
    for key in request.POST:
        if key.startswith('choice'):
            value = request.POST[key]
            choice_id = int(value)
            submitted_answers.append(choice_id)
    return submitted_answers


# Submit view
def submit(request, course_id):
    user = request.user
    course = get_object_or_404(Course, pk=course_id)

    enrollment = Enrollment.objects.get(user=user, course=course)
    submission = Submission.objects.create(enrollment=enrollment)

    selected_choices = extract_answers(request)
    for choice_id in selected_choices:
        choice = get_object_or_404(Choice, pk=choice_id)
        submission.choices.add(choice)

    submission.save()

    return HttpResponseRedirect(
        reverse('onlinecourse:show_exam_result', args=(course_id, submission.id))
    )


