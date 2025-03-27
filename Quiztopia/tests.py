from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from Quiztopia.models import UserProfile, Quiz, Question

# Create your tests here.
class QuizCreationTests(TestCase):
    #def simulateAddQuizPost(self):
    #    return {
    #    'csrfmiddlewaretoken': ['vu0JIKH8BN2xZJXigzGOBDQX7QMpRzFEfSL8cEfr7YTQX9U5jEQj1ipVSMjmQ4dC'], 
    #    'quiz_title': ['TestQuiz'], 
    #    'category': ['Movies And TV'], 
    #    'difficulty': ['Easy'], 
    #    'upvotes': ['0'], 
    #    'questions-TOTAL_FORMS': ['1'], 
    #    'questions-INITIAL_FORMS': ['0'], 
    #    'questions-MIN_NUM_FORMS': ['0'], 
    #    'questions-MAX_NUM_FORMS': ['10'], 
    #    'questions-0-question_text': ['', 'TestQ'], 
    #    'answers-0-TOTAL_FORMS': ['4'], 
    #    'answers-0-INITIAL_FORMS': ['0'], 
    #    'answers-0-MIN_NUM_FORMS': ['0'], 
    #    'answers-0-MAX_NUM_FORMS': ['4'], 
    #    'answers-0-0-answer_text': ['TestAns1'], 
    #    'correct_answer_question_0': ['0'], 
    #    'answers-0-1-answer_text': ['TestAns2'], 
    #    'answers-0-2-answer_text': [''], 
    #    'answers-0-3-answer_text': [''], 
    #    'submit': ['Create Quiz']
    #    }

    def setUp(self):
        #Set up a test user and user profile
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user_profile = UserProfile.objects.create(user=self.user, username='testuser')
 

    def test_add_quiz_create_quiz(self):
        #Test that a logged-in user can create a quiz - EDIT
        self.client.login(username='testuser', password='testpassword')
        self.simulateAddQuiz()

        self.assertEqual(Quiz.objects.count(), 1)
        print("test_add_quiz_create_quiz PASSED")


    def test_add_quiz_correct_fields(self):
        self.client.login(username='testuser', password='testpassword')
        self.simulateAddQuiz()
        quiz = Quiz.objects.first()
        
        self.assertEqual(quiz.quiz_title, "Sample Quiz")
        self.assertEqual(quiz.category, "General Knowledge")
        self.assertEqual(quiz.difficulty, "Easy")
        self.assertEqual(quiz.upvotes, 0)
        print("test_add_quiz_correct_fields PASSED")
    

    def test_add_quiz_creator_is_user(self):
        self.client.login(username='testuser', password='testpassword')
        self.simulateAddQuiz()
        quiz = Quiz.objects.first()

        self.assertEquals(quiz.creator, self.user_profile)
        print("test_add_quiz_creator_is_user PASSED")


    def test_add_quiz_increments_user_created_quizzes(self):
        self.client.login(username='testuser', password='testpassword')
        self.simulateAddQuiz()
        self.user_profile.refresh_from_db()
        
        self.assertEqual(self.user_profile.quizzes_created, 1)
        print("test_add_quiz_increments_user_created_quizzes PASSED")


    def test_add_quiz_no_of_questions(self):
        self.client.login(username='testuser', password='testpassword')
        self.simulateAddQuiz()

        self.assertEqual(Question.objects.count(), 2)
        print("test_add_quiz_no_of_questions PASSED")

    # Test no of answers?

    # Helper Method
    def simulateAddQuiz(self):
        response = self.client.post(reverse("Quiztopia:add_quiz"), {
            'quiz_title': 'Sample Quiz', 
            'category': 'General Knowledge', 
            'difficulty': 'Easy', 
            'upvotes': '0', 
            'questions-TOTAL_FORMS': '2', 
            'questions-INITIAL_FORMS': '0',
            'questions-0-question_text': ['', 'Sample Question 1'],
            'questions-1-question_text': ['', 'Sample Question 2'],
            'answers-0-TOTAL_FORMS': '4', 
            'answers-0-INITIAL_FORMS': '0',
            'answers-1-TOTAL_FORMS': '4', 
            'answers-1-INITIAL_FORMS': '0', 
        })

#class QuizEditTests(TestCase):


class QuizDeletionTests(TestCase):
    
    def setUp(self):
        #Set up a test user and user profile
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user_profile = UserProfile.objects.create(user=self.user, username='testuser')
        self.quiz = Quiz.objects.create(
            quiz_title='Quiz to Delete',
            category='Movies And TV',
            difficulty='Medium',
            creator=self.user_profile
        )
        self.user_profile.quizzes_created += 1
        self.user_profile.save()


    def test_delete_quiz(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse("Quiztopia:profile"), {"selected" : self.quiz.quiz_ID}, content_type="application/json")

        self.assertEqual(Quiz.objects.count(), 0)
        print("test_profile_delete_quiz PASSED")


    def test_delete_quiz_decrements_user_created_quizzes(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse("Quiztopia:profile"), {"selected" : self.quiz.quiz_ID}, content_type="application/json")
        self.user_profile.refresh_from_db()

        self.assertEqual(self.user_profile.quizzes_created, 0)
        print("test_delete_quiz_decrements_user_created_quizzes PASSED")


    def test_delete_quiz_no_of_questions(self):
        question = Question.objects.create(
            question_text="Question to Delete",
            quiz_ID=self.quiz
        )
        questionCount = Question.objects.count()

        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse("Quiztopia:profile"), {"selected" : self.quiz.quiz_ID}, content_type="application/json")
        
        self.assertEqual(Question.objects.count(), questionCount-1)
        print("test_delete_quiz_no_of_questions PASSED")


    