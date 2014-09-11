from django.http import HttpResponseRedirect, HttpResponse
#from django.http import Http404
from django.shortcuts import get_object_or_404, render
#from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

from polls.models import Choice, Question

# Create your views here.

class IndexView(generic.ListView):
	#latest_question_list = Question.objects.all().order_by('-pub_date')[:5]
	#context = {'latest_question_list' : latest_question_list}
	#return render(request, 'polls/index.html', context)
	template_name = 'polls/index.html'
	context_object_name='latest_question_list'

	def get_queryset(self):
        #    return Question.objects.order_by('-pub_date')[:5]
            return Question.objects.filter(
                   pub_date__lte=timezone.now() 
            ).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
	#try:
	#	question = Question.objects.get(pk=question_id)
	#except Question.DoesNotExist:
	#	raise Http404
	#return render(request, 'polls/detail.html', {'question': question})
	#question = get_object_or_404(Question, pk=question_id)
	#return render(request, 'polls/detail.html', {'question': question})
	model = Question
	template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
	#response ="You're looking at the results of question %s."
	#return HttpResponse(response % question_id)
	model = Question
	template_name = 'polls/results.html'

def vote(request, question_id):
#	return HttpResponse("You're voting on question %s" % question_id)
	p = get_object_or_404(Question, pk = question_id)
	try:
		selected_choice = p.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		# Redisplay the question voting form
		return render(request, 'polls/detail.html', {
			'question': p,
			'error_message': "You didn't select a choice.",
		})
	else:
		selected_choice.votes += 1
		selected_choice.save()
		# Always return an HttpResponseRedirect after successfully dealing
		# with POST data. This prevents data from being posted twice if a user
		# hits the back button.
		return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))

def results(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'polls/results', {'question': question})
