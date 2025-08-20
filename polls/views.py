from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.db.models import F
from django.views import generic
from django.utils import timezone
from .models import Question, Choice



class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_questions_list"
    
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    template_name = "polls/detail.html" 
    model = Question
    
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultView(generic.DetailView):
    template_name = "polls/results.html"
    model = Question
    
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())
       

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id, pub_date__lte=timezone.now())
    try:
        # if question.pub_date > timezone.now():    # if user tries to access the future poll votes using url it 
        # # will raise error
        #     raise KeyError
        
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(request, "polls/detail.html", {
            "question": question,
            "error_message": "You didn't selected any choice.",
        })
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        
        return redirect("polls:results", question_id)
    

