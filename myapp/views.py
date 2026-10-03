
from datetime import date

import requests

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect,get_list_or_404
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import *
from .serializers import *
    



class SubjectAPIView(APIView):

    def get(self, request):
        subjects = Subject.objects.all()
        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SubjectSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class SubjectviewById(APIView):

    def get(self, request, id):
        try:
            subject = Subject.objects.get(id=id)
        except Subject.DoesNotExist:
            return Response(
                {"error": "Subject not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = SubjectSerializer(subject)
        return Response(serializer.data)

    def put(self, request, id):
        try:
            subject = Subject.objects.get(id=id)
        except Subject.DoesNotExist:
            return Response(
                {"error": "Subject not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = SubjectSerializer(
            subject,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, id):
        try:
            subject = Subject.objects.get(id=id)
        except Subject.DoesNotExist:
            return Response(
                {"error": "Subject not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        subject.delete()

        return Response(
            {"message": "Subject deleted successfully"},
            status=status.HTTP_200_OK
        )


class AssignmentAPIView(APIView):

    def get(self, request):
        assignments = Assignment.objects.all()

        search = request.GET.get("search")
        priority = request.GET.get("priority")
        status_value = request.GET.get("status")
        subject = request.GET.get("subject")

        if search:
            assignments = assignments.filter(
                Q(title__icontains=search)
                | Q(description__icontains=search)
            )

        if priority:
            assignments = assignments.filter(priority=priority)

        if status_value:
            assignments = assignments.filter(status=status_value)

        if subject:
            assignments = assignments.filter(subject_id=subject)

        serializer = AssignmentSerializer(
            assignments,
            many=True,
            context={"request": request}
        )

        return Response(serializer.data)

    def post(self, request):
        serializer = AssignmentSerializer(
            data=request.data,
            context={"request": request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Assignment saved successfully",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {"error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )


class AssignmentViewById(APIView):

    def get(self, request, id):
        try:
            assignment = Assignment.objects.get(id=id)
        except Assignment.DoesNotExist:
            return Response(
                {"error": "Assignment not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = AssignmentSerializer(
            assignment,
            context={"request": request}
        )

        return Response(serializer.data)

    def put(self, request, id):
        try:
            assignment = Assignment.objects.get(id=id)
        except Assignment.DoesNotExist:
            return Response(
                {"error": "Assignment not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = AssignmentSerializer(
            assignment,
            data=request.data,
            context={"request": request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            {"error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    def patch(self, request, id):
        try:
            assignment = Assignment.objects.get(id=id)
        except Assignment.DoesNotExist:
            return Response(
                {"error": "Assignment not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = AssignmentSerializer(
            assignment,
            data=request.data,
            partial=True,
            context={"request": request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            {"error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, id):
        try:
            assignment = Assignment.objects.get(id=id)
        except Assignment.DoesNotExist:
            return Response(
                {"error": "Assignment not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        assignment.delete()

        return Response(
            {"message": "Assignment deleted successfully"},
            status=status.HTTP_200_OK
        )


def home(request):
    return render(request, "home.html")



def register(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        if not username or not password:
            return render(
                request,
                "register.html",
                {"error": "Username and password are required"}
            )

        if password != confirm_password:
            return render(
                request,
                "register.html",
                {"error": "Passwords do not match"}
            )

        if User.objects.filter(username=username).exists():
            return render(
                request,
                "register.html",
                {"error": "Username already exists"}
            )

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(request, "Registration successful. Please login.")
        return redirect("login")

    return render(request, "register.html")


def login(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            auth_login(request, user)
            return redirect("dashboard")

        return render(
            request,
            "login.html",
            {"error": "Invalid username or password"}
        )

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("login")



@login_required(login_url="login")
def dashboard(request):

    assignments = Assignment.objects.all()

    today = date.today()

    total_assignments = assignments.count()

    pending_assignments = assignments.filter(
        status="Pending"
    ).count()

    completed_assignments = assignments.filter(
        status="Completed"
    ).count()

    high_priority_assignments = assignments.filter(
        priority="High"
    ).count()

    overdue_assignments = assignments.filter(
        due_date__lt=today
    ).exclude(
        status="Completed"
    ).count()

    context = {
        "total_assignments": total_assignments,
        "pending_assignments": pending_assignments,
        "completed_assignments": completed_assignments,
        "overdue_assignments": overdue_assignments,
        "high_priority_assignments": high_priority_assignments,
        "assignments": assignments,
    }

    return render(
        request,
        "dashboard.html",
        context
    )


from django.shortcuts import render

def assignment_list(request):

    search = request.GET.get("search", "")
    priority = request.GET.get("priority", "")
    status_value = request.GET.get("status", "")
    subject = request.GET.get("subject", "")

    assignments = Assignment.objects.all()
    subjects = Subject.objects.all()

    # Search
    if search:
        assignments = assignments.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search) |
            Q(name__icontains=search)
        )

    # Priority filter
    if priority:
        assignments = assignments.filter(
            priority=priority
        )

    # Status filter
    if status_value:
        assignments = assignments.filter(
            status=status_value
        )

    # Subject filter
    if subject:
        assignments = assignments.filter(
            subject_id=subject
        )

    return render(
        request,
        "assignment_list.html",
        {
            "assignments": assignments,
            "subjects": subjects,
            "search": search,
            "selected_priority": priority,
            "selected_status": status_value,
            "selected_subject": subject,
            "error": None,
        }
    )

def add_assignment(request):

    subjects = Subject.objects.all()

    if request.method == "GET":

        return render(
            request,
            "assignment_form.html",
            {
                "subjects": subjects
            }
        )

    if request.method == "POST":

        title = request.POST.get("title", "").strip()
        subject_id = request.POST.get("subject")
        description = request.POST.get("description", "").strip()
        due_date = request.POST.get("due_date")
        priority = request.POST.get("priority")
        status = request.POST.get("status")
        name = request.POST.get("name", "").strip()

        attachment = request.FILES.get("attachment")

        try:
            subject = Subject.objects.get(id=subject_id)

        except Subject.DoesNotExist:

            return render(
                request,
                "assignment_form.html",
                {
                    "subjects": subjects,
                    "error": "Please select a valid subject."
                }
            )

        Assignment.objects.create(
            title=title,
            subject=subject,
            description=description,
            due_date=due_date,
            priority=priority,
            status=status,
            name=name,
            attachment=attachment
        )

        messages.success(
            request,
            "Assignment added successfully!"
        )

        return redirect("assignment_list")

    
def edit_assignment(request, id):

    try:
        assignment = Assignment.objects.get(id=id)
    except Assignment.DoesNotExist:
        return HttpResponse("Assignment not found", status=404)

    subjects = Subject.objects.all()

    if request.method == "GET":

        return render(
            request,
            "edit_assignment.html",
            {
                "assignment": assignment,
                "subjects": subjects,
            }
        )

    if request.method == "POST":

        title = request.POST.get("title", "").strip()
        subject_id = request.POST.get("subject")
        description = request.POST.get("description", "").strip()
        due_date = request.POST.get("due_date")
        priority = request.POST.get("priority")
        status = request.POST.get("status")
        name = request.POST.get("name", "").strip()

        attachment = request.FILES.get("attachment")

        # Check subject
        if not subject_id:
            return render(
                request,
                "edit_assignment.html",
                {
                    "assignment": assignment,
                    "subjects": subjects,
                    "error": "Please select a subject."
                }
            )

        try:
            subject = Subject.objects.get(id=int(subject_id))

        except (Subject.DoesNotExist, ValueError):
            return render(
                request,
                "edit_assignment.html",
                {
                    "assignment": assignment,
                    "subjects": subjects,
                    "error": "Please select a valid subject."
                }
            )

        # Update assignment
        assignment.title = title
        assignment.subject = subject
        assignment.description = description
        assignment.due_date = due_date
        assignment.priority = priority
        assignment.status = status
        assignment.name = name

        if attachment:
            assignment.attachment = attachment

        assignment.save()

        messages.success(
            request,
            "Assignment updated successfully!"
        )

        return redirect("assignment_list")


def delete_assignment(request, id):

    try:
        assignment = Assignment.objects.get(id=id)
    except Assignment.DoesNotExist:
        return HttpResponse("Assignment not found", status=404)

    if request.method == "GET":

        return render(
            request,
            "assignment_delete.html",
            {
                "assignment": assignment
            }
        )

    if request.method == "POST":

        assignment.delete()

        messages.success(
            request,
            "Assignment deleted successfully!"
        )

        return redirect("assignment_list")


from django.shortcuts import render
from django.views.decorators.cache import never_cache

@never_cache
def subject_list(request):

    subjects = Subject.objects.all()

    response = render(
        request,
        "subject_list.html",
        {
            "subjects": subjects,
            "error": None,
        }
    )

    return response


def add_subject(request):

    if request.method == "GET":
        return render(
            request,
            "subject_form.html"
        )

    subject_name = request.POST.get(
        "subject_name",
        ""
    ).strip()

    if not subject_name:
        return render(
            request,
            "subject_form.html",
            {
                "error": "Please enter a subject name."
            }
        )

    if len(subject_name) > 30:
        return render(
            request,
            "subject_form.html",
            {
                "error": "Subject name must be within 30 characters."
            }
        )

    # Save directly to database
    Subject.objects.create(
        subject_name=subject_name
    )

    messages.success(
        request,
        "Subject added successfully!"
    )

    return redirect("subject_list")
    
def edit_subject(request, id):

    try:
        subject = Subject.objects.get(id=id)
    except Subject.DoesNotExist:
        return HttpResponse("Subject not found", status=404)

    if request.method == "GET":
        return render(
            request,
            "edit_subject.html",
            {
                "subject": subject
            }
        )

    if request.method == "POST":

        subject_name = request.POST.get(
            "subject_name",
            ""
        ).strip()

        if not subject_name:
            return render(
                request,
                "edit_subject.html",
                {
                    "subject": subject,
                    "error": "Subject name is required."
                }
            )

        if len(subject_name) > 30:
            return render(
                request,
                "edit_subject.html",
                {
                    "subject": subject,
                    "error": "Subject name must be within 30 characters."
                }
            )

        subject.subject_name = subject_name
        subject.save()

        messages.success(
            request,
            "Subject updated successfully!"
        )

        return redirect("subject_list")


def delete_subject(request, id):

    try:
        subject = Subject.objects.get(id=id)
    except Subject.DoesNotExist:
        return HttpResponse("Subject not found", status=404)

    if request.method == "GET":
        return render(
            request,
            "delete_subject.html",
            {
                "subject": subject
            }
        )

    if request.method == "POST":

        subject.delete()

        # Check whether deletion really happened
        if Subject.objects.filter(id=id).exists():
            return HttpResponse(
                "Subject was not deleted from database.",
                status=500
            )

        messages.success(
            request,
            "Subject deleted successfully!"
        )

        return redirect("subject_list")


class AptitudeCategoryAPIView(APIView):

    def get(self, request):
        categories = AptitudeCategory.objects.all()

        serializer = AptitudeCategorySerializer(
            categories,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):
        serializer = AptitudeCategorySerializer(
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Category created successfully",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {"error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )






class QusetionAPIView(APIView):

    def get(self, request):
        questions = Question.objects.all()

        category_id = request.GET.get("category")

        if category_id:
            questions = questions.filter(category_id=category_id)

        serializer = QuestionSerializer(
            questions,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):
        serializer = QuestionSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Question created successfully",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {"error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )




from .models import AptitudeCategory

def aptitude_dashboard(request):
    categories = AptitudeCategory.objects.all()

    print("Aptitude categories:", categories.count())

    return render(
        request,
        "aptitude_dashboard.html",
        {
            "categories": categories
        }
    )



from django.shortcuts import get_object_or_404
# APTITUDE QUESTIONS AND RESULT
def aptitude_questions(request, category_id):

    category = get_object_or_404(
        AptitudeCategory,
        id=category_id
    )

    questions = Question.objects.filter(
        category=category
    )

    if request.method == "POST":

        score = 0
        total = questions.count()

        for question in questions:

            selected_answer = request.POST.get(
                f"answer_{question.id}",
                ""
            ).strip().upper()

            correct_answer = str(
                question.correct_answer
            ).strip().upper()

            if selected_answer == correct_answer:
                score += 1

        return render(
            request,
            "aptitude_result.html",
            {
                "category": category,
                "score": score,
                "total": total
            }
        )

    return render(
        request,
        "aptitude_questions.html",
        {
            "category": category,
            "questions": questions
        }
    )