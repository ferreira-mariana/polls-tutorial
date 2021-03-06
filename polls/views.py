from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import Question
# Create your views here.

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list' #to specify that we want to use this variable instead of the default question_list

    def get_queryset(self):
        # return the last five published questions
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question #this automatically provide the context variable question
    template_name = 'polls/detail.html' #tells Django to use a specific template name instead of the autogenerated default <app name>/<model name>_detail.html

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', { 'question': question, 'error_message': "You didn't select a choice."})
    else:
        selected_choice.votes += 1
        selected_choice.save()

    return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))