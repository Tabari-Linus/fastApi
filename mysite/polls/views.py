from re import template
from django.shortcuts import render
from .models import Question


# Create your views here.
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        "latest_question_list" : latest_question_list,
    }
    return render(request, 'polls/index.html', context)


def detail(request):
    return HttpResponse("Hello, World. You're at the polls index")


def results(request):
    return HttpResponse("Hello, World. You're at the polls index")


def vote(request):
    return HttpResponse("Hello, World. You're at the polls index")