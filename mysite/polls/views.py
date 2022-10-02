from audioop import reverse
from re import template
from select import select
from django.shortcuts import get_object_or_404, render
from .models import Question, Choice
from django.http import Http404, HttpResponse, HttpResponseRedirect

# Create your views here.
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        "latest_question_list" : latest_question_list,
    }
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        seleced_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplays the question voting form.
        return render(request, 'polls/detail.html',{'question': question, 'error_message': "You didn't select a choice.",
        })
    else:
        seleced_choice.votes += 1
        seleced_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits back button

    return HttpResponseRedirect(reverse('polls/results', args=(question.id)))

