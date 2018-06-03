from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import *
from datetime import datetime

# Create your views here.

#CHANGE ALL/NECESSARY TO REDIRECT

def index(request):
    request.session.flush()
    return redirect('/login')

# Login page
def login(request):
    return render(request, 'eval/login.html', {})

# Authenticates user, and redirects to correct homepage, or redirects to login page w/ appropriate error message
def homepage(request):
    username = request.POST.get('username', 'blank-username') # If no username, default='blank-username'
    password = request.POST.get('password', 'blank-pswd') # If no password, default='blank-pswd'

    # If user is a student, check password, and if it's correct, redirect to student homepage.
    try:
        student = Student.objects.get(stud_id=username)
        if password == student.stud_pswd:
            # This returns entire rendering of student homepage
            request.session['stud-id'] = username
            #return student_homepage(request)
            return redirect('/stud-homepage') #URL


    # If user is not a student, check if they are a professor, and if they are
    # check if their passowrd is correct, and if it is, redir. to prof. homepage.
    except (KeyError, Student.DoesNotExist):
        try:
            professor = Professor.objects.get(prof_id=username)
            if password == professor.prof_pswd:
                request.session['prof-id'] = professor.prof_id

                return redirect('/prof-homepage')

        # If user is not a professor either, reload login page with message, "Invalid username"
        except (KeyError, Professor.DoesNotExist):
            error_message = "Invalid username"
            return render(request, 'eval/login.html', {
                'error_message' : error_message,
            })


    # If we've reached here, it means user is either a student or professor (i.e. username is valid),
    # but their password is incorrect
    error_message = "Password incorrect"
    return render(request, 'eval/login.html', {
        'error_message' : error_message,
        'valid_username' : username,
    })

# Complete Rendering of student homepage
def student_homepage(request):
    student = Student.objects.get(stud_id = request.session['stud-id'])
    comments = Comment.objects.all().filter(stud_id=student.stud_id)
    return render(request, 'eval/stud-homepage.html', {
        'student' : student,
        'comments' : comments,
    })


# Rendering of page where student can fill out evaluation
def stud_eval(request):
    comment_id = request.POST.get('comment-id', '')
    #"Evaluate" button was pressed without selecting an evaluation, redirects to same exact page
    if not comment_id:
        return redirect('/stud-homepage')
    request.session['comment-id'] = comment_id
    return redirect('/eval-page')


def eval_page(request):
    comment = Comment.objects.get(pk=request.session['comment-id'])
    return render(request, 'eval/eval-page.html', {
        'comment' : comment,
    })


# When submit button is clicked, save submission if possible, and redirect to student homepage
def eval_submit(request):
    comment = Comment.objects.get(pk=request.session['comment-id'])
    # If comment is NOW able to be edited
    if comment.can_edit():
        # Default values in case of absence of request POST values are the previous comment field values,
        # in case the eval session was closed when the eval page was loaded (in which case the input fields
        # would be disabled) but opened before the 'Submit' button was clicked (in which case the below
        # code would execute, attempting to save the input)
        class_rating = request.POST.get('class-rating', comment.class_rating)
        class_comment = request.POST.get('class-comment', comment.class_comment)
        comment.class_rating = class_rating
        comment.class_comment = class_comment
        comment.save()

    return redirect('/stud-homepage')


# To do - prof homepage
def professor_homepage(request):
    professor = Professor.objects.get(pk=request.session['prof-id'])
    courses = professor.course_set.all()
    sessions = [session for course in courses for session in course.session_set.all()]
    try:
        message = request.session['prof-message']
    except:
        message = ''

    return render(request, 'eval/prof-homepage.html', {
        'professor' : professor,
        'sessions' : sessions,
        'message' : message,
    })


def prof_new_session(request):
    course_id = request.POST.get('course-id', '')
    new_session_start = request.POST.get('new-session-start', '')
    new_session_end = request.POST.get('new-session-end', '')

    # If input info is not complete
    if not (course_id and new_session_start and new_session_end):
        request.session['prof-message'] = "The session has not been added"
        return redirect('/prof-homepage')

    # If input info is complete, proceed to add session
    session_course = Course.objects.get(pk=course_id)
    new_session = Session(course_id=session_course, session_start=new_session_start, session_end=new_session_end)
    new_session.save()

    for student in session_course.students.all():
        new_stud_comment = Comment(stud_id=student, session_id=new_session)
        new_stud_comment.save()

    request.session['prof-message'] = "YESS"


    return redirect('/prof-homepage')


def evals_report(request):
    session_id = request.POST.get('session-id', '')
    if not session_id:
        return redirect('/prof-homepage')

    session = Session.objects.get(pk=session_id)
    return render(request, 'eval/evals-report.html', {
        'session' : session, 
    })
