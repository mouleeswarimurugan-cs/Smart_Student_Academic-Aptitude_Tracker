
from django.urls import path

from myapp.views import *

from . import views


urlpatterns = [

    # Home
    path("", home, name="home"),

    # Authentication
    path("register/", register, name="register"),
    path("login/", login, name="login"),
    path("logout/", logout_view, name="logout"),

    # Dashboard
    path("dashboard/", dashboard, name="dashboard"),

    # Assignments
    path("assignments/", assignment_list, name="assignment_list"),
    path("assignments/add/", add_assignment, name="add_assignment"),
    path("assignments/edit/<int:id>/", edit_assignment, name="edit_assignment"),
    path("assignments/delete/<int:id>/",delete_assignment, name="delete_assignment"),

    # Subjects
    path("subjects/", subject_list, name="subject_list"),
    path("subjects/add/", add_subject, name="add_subject"),
    path("subjects/edit/<int:id>/", edit_subject, name="edit_subject"),
    path("subjects/delete/<int:id>/", delete_subject, name="delete_subject"),


    #api
    path("subject/",SubjectAPIView.as_view()),
    path("subject/<int:id>/",SubjectviewById.as_view()),
    path("assignment/",AssignmentAPIView.as_view()),
    path("assignment/<int:id>/",AssignmentViewById.as_view()),
    path("assignment-details/<int:id>/",AssignmentViewById.as_view()),
#aptitude api
    path("aptitude/category/",AptitudeCategoryAPIView.as_view()),
    path("aptitude/question/",QusetionAPIView.as_view()),

    path("aptitude/questions/<int:category_id>/",aptitude_questions,name="aptitude_questions"),
    path("aptitude/",views.aptitude_dashboard,name="aptitude_dashboard"),
]

