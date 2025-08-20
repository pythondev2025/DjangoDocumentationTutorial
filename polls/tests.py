import datetime
from django.urls import reverse
from django.test import TestCase
from django.utils import timezone
from .models import Question


class QuestionModelTest(TestCase):
    def test_future_pub_date(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)
    
    def test_past_pub_date(self):
        past_time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        past_q = Question(pub_date=past_time)
        self.assertIs(past_q.was_published_recently(), False)
        
    def test_recent_pub_date(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_q = Question(pub_date=time)
        self.assertIs(recent_q.was_published_recently(), True)


class QuestionIndexViewTests(TestCase):
    def test_no_question(self):
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no questions yet:)")
        self.assertQuerySetEqual(response.context["latest_questions_list"], [])
        
    def test_past_question(self):
        past_question = create_question("Past Question", -30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_questions_list"], [past_question])

    def test_future_question(self):
        create_question("Future Question", 30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "There are no questions yet:)")
        self.assertQuerySetEqual(response.context["latest_questions_list"], [])
        
    def test_future_and_past_question(self):
        question_1 = create_question("PAST QUESTION", -12)
        question_2 = create_question("PAST QUESTION 2", -25)
        create_question("Future Question", 50)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_questions_list"], [question_1, question_2])


class QuestionDetailViewTest(TestCase):
    def test_future_question(self):
        question = create_question("future question", 25)
        url = reverse("polls:detail", args=(question.id,))
        res = self.client.get(url)
        self.assertEqual(res.status_code, 404)
    
    def test_past_question(self):
        question = create_question("past question", -29)
        url = reverse("polls:detail", args=(question.id,))
        res = self.client.get(url)
        self.assertContains(res, question.question_text)


# creating the function of creating the question and avoid the repitition in the view classes
def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


    
    