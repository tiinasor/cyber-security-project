from django.db.models import F
from django.db import connection
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)

from .models import Choice, Question


class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]


class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(LoginRequiredMixin, generic.DetailView):
    model = Question
    template_name = "polls/results.html"


@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(request, "polls/detail.html", {
            "question": question,
            "error_message": "You didn't select a choice.",
        })
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username and password:
            if User.objects.filter(username=username).exists():
                return render(request, "polls/register.html", {"error": "Username already taken."})
            # FLAW 3:
            password_is_valid = True
            # FIX 3: Uncomment the following and replace the line above
            # from django.contrib.auth.password_validation import validate_password
            # from django.core.exceptions import ValidationError
            # try:
            #     validate_password(password)
            #     password_is_valid = True
            # except ValidationError as e:
            #     password_is_valid = False
            #     return render(request, "polls/register.html", {"error": " ".join(e.messages)})
            User.objects.create_user(username=username, password=password)
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect("polls:index")
    return render(request, "polls/register.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("polls:index")
        # FLAW 5: Failed login attempts are not logged
        # FIX 5: Uncomment the following line
        # logger.warning(f"Failed login attempt for user: {username}")
    return render(request, "polls/login.html")


def logout_view(request):
    logout(request)
    return redirect("polls:index")


# FLAW 1:
@login_required
def search(request):
    query = request.GET.get("q", "")
    questions = []
    if query:
        cursor = connection.cursor()
        cursor.execute(
            f"SELECT * FROM polls_question WHERE question_text LIKE '%%{query}%%'"
        )
        questions = cursor.fetchall()
    # FIX 1: Uncomment the following and replace the block above
    # if query:
    #     questions = Question.objects.filter(question_text__icontains=query)
    return render(request, "polls/search.html", {"questions": questions, "query": query})


# FLAW 2:
@login_required
def delete_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    question.delete()
    return render(request, "polls/delete_success.html", {"question_text": question.question_text})
# FIX 2: Uncomment the following and replace the block above
# from django.contrib.admin.views.decorators import staff_member_required
# @staff_member_required
# def delete_question(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     question.delete()
#     return render(request, "polls/delete_success.html", {"question_text": question.question_text})
