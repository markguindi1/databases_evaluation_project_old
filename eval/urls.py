from django.urls import path
from . import views


app_name = 'eval'

urlpatterns = [

    #/index/
    path('', views.index, name='index'),

    path('login/', views.login, name='login'),

    path('homepage/', views.homepage, name="homepage"),

    path('stud-homepage/', views.student_homepage, name="stud-homepage"),

    path('stud-eval/', views.stud_eval, name="stud-eval"),

    path('eval-page/', views.eval_page, name="eval-page"),

    path('eval-submit/', views.eval_submit, name="eval-submit"),

    path('prof-homepage/', views.professor_homepage, name="prof-homepage"),

    path('prof-new-session/', views.prof_new_session, name="prof-new-session"),

    path('evals-report/', views.evals_report, name="evals-report"),

]
