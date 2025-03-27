from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from Quiztopia.models import UserProfile, Quiz, Question

# Create your tests here.
class QuizCreationTests(TestCase):
    
    def setUp(self):
        #Set up a test user and user profile
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user_profile = UserProfile.objects.create(user=self.user, username='testuser')
 

    def test_add_quiz_create_quiz(self):
        #Test that a logged-in user can create a quiz - EDIT
        self.client.login(username='testuser', password='testpassword')
        self.simulate_add_quiz()

        self.assertEqual(Quiz.objects.count(), 1)
        print("test_add_quiz_create_quiz PASSED")


    def test_add_quiz_correct_fields(self):
        self.client.login(username='testuser', password='testpassword')
        self.simulate_add_quiz()
        quiz = Quiz.objects.first()
        
        self.assertEqual(quiz.quiz_title, "Sample Quiz")
        self.assertEqual(quiz.category, "General Knowledge")
        self.assertEqual(quiz.difficulty, "Easy")
        self.assertEqual(quiz.upvotes, 0)
        print("test_add_quiz_correct_fields PASSED")
    

    def test_add_quiz_creator_is_user(self):
        self.client.login(username='testuser', password='testpassword')
        self.simulate_add_quiz()
        quiz = Quiz.objects.first()

        self.assertEquals(quiz.creator, self.user_profile)
        print("test_add_quiz_creator_is_user PASSED")


    def test_add_quiz_increments_user_created_quizzes(self):
        self.client.login(username='testuser', password='testpassword')
        self.simulate_add_quiz()
        self.user_profile.refresh_from_db()
        
        self.assertEqual(self.user_profile.quizzes_created, 1)
        print("test_add_quiz_increments_user_created_quizzes PASSED")


    def test_add_quiz_no_of_questions(self):
        self.client.login(username='testuser', password='testpassword')
        self.simulate_add_quiz()

        self.assertEqual(Question.objects.count(), 2)
        print("test_add_quiz_no_of_questions PASSED")


    def test_add_quiz_correct_questions(self):
        self.client.login(username='testuser', password='testpassword')
        self.simulate_add_quiz()
        
        question_1 = Question.objects.all()[0]
        question_2 = Question.objects.all()[1]
        self.assertEqual(question_1.question_text, "Sample Question 1")
        self.assertEqual(question_2.question_text, "Sample Question 2")
        print("test_add_quiz_correct_questions PASSED")



    # Helper Method
    def simulate_add_quiz(self):
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


    def test_profile_delete_quiz(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse("Quiztopia:profile"), {"selected" : self.quiz.quiz_ID}, content_type="application/json")

        self.assertEqual(Quiz.objects.count(), 0)
        print("test_profile_delete_quiz PASSED")


    def test_profile_delete_quiz_decrements_user_created_quizzes(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse("Quiztopia:profile"), {"selected" : self.quiz.quiz_ID}, content_type="application/json")
        self.user_profile.refresh_from_db()

        self.assertEqual(self.user_profile.quizzes_created, 0)
        print("test_profile_delete_quiz_decrements_user_created_quizzes PASSED")


    def test_profile_delete_quiz_no_of_questions(self):
        question = Question.objects.create(
            question_text="Question to Delete",
            quiz_ID=self.quiz
        )
        questionCount = Question.objects.count()

        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse("Quiztopia:profile"), {"selected" : self.quiz.quiz_ID}, content_type="application/json")
        
        self.assertEqual(Question.objects.count(), questionCount-1)
        print("test_profile_delete_quiz_no_of_questions PASSED")


class QuizEditTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user_profile = UserProfile.objects.create(user=self.user, username='testuser')

        self.client.login(username='testuser', password='testpassword')
        self.simulate_add_quiz()
        self.quiz = Quiz.objects.first()

        self.user_profile.quizzes_created += 1
        self.user_profile.save()


    def test_edit_quiz_fields_change(self):
        self.simulate_edit_quiz()
        self.quiz.refresh_from_db()

        self.assertNotEqual(self.quiz.quiz_title, "Quiz to Edit")
        self.assertNotEqual(self.quiz.category, "General Knowledge")
        self.assertNotEqual(self.quiz.difficulty, "Easy")
        print("test_edit_quiz_fields_change PASSED")

    
    def test_edit_quiz_user_created_quizzes_remains_same(self):
        self.simulate_edit_quiz()
        self.quiz.refresh_from_db()

        self.assertEqual(self.user_profile.quizzes_created, 1)
        print("test_edit_quiz_user_created_quizzes_remains_same PASSED")

    # Helper Method
    def simulate_edit_quiz(self):
        response = self.client.post(reverse("Quiztopia:edit_quiz", 
                                            kwargs = {"quiz_id" : self.quiz.quiz_ID}), {
            'quiz_title': 'Quiz Editted', 
            'category': 'Animals', 
            'difficulty': 'Hard', 
            'upvotes': '0',
            'questions-TOTAL_FORMS': '1', 
            'questions-INITIAL_FORMS': '0',
            'questions-0-question_text': ['', 'Editted Question'],
            'answers-0-TOTAL_FORMS': '4', 
            'answers-0-INITIAL_FORMS': '0',
        })

    # Helper Method
    def simulate_add_quiz(self):
        response = self.client.post(reverse("Quiztopia:add_quiz"), {
            'quiz_title': 'Quiz to Edit', 
            'category': 'General Knowledge', 
            'difficulty': 'Easy', 
            'upvotes': '0', 
            'questions-TOTAL_FORMS': '1', 
            'questions-INITIAL_FORMS': '0',
            'questions-0-question_text': ['', 'Question to Edit'],
            'answers-0-TOTAL_FORMS': '4', 
            'answers-0-INITIAL_FORMS': '0', 
        })


class TakeQuizTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user_profile = UserProfile.objects.create(user=self.user, username='testuser')

        self.client.login(username='testuser', password='testpassword')
        self.simulate_add_quiz()
        self.quiz = Quiz.objects.first()

        self.user_profile.quizzes_created += 1
        self.user_profile.save()

    def test_take_quiz_increments_user_taken_quizzes(self):
        self.client.post(reverse("Quiztopia:take_quiz", kwargs = {
            "category_slug" : self.quiz.category_slug,
            "quiz_id" : self.quiz.quiz_ID
            }))
        self.user_profile.refresh_from_db()

        self.assertEqual(self.user_profile.quizzes_taken, 1)
        print("test_take_quiz_increments_user_taken_quizzes PASSED")

    # Helper Method
    def simulate_add_quiz(self):
        response = self.client.post(reverse("Quiztopia:add_quiz"), {
            'quiz_title': 'Quiz to Edit', 
            'category': 'General Knowledge', 
            'difficulty': 'Easy', 
            'upvotes': '0', 
            'questions-TOTAL_FORMS': '1', 
            'questions-INITIAL_FORMS': '0',
            'questions-0-question_text': ['', 'Question to Edit'],
            'answers-0-TOTAL_FORMS': '4', 
            'answers-0-INITIAL_FORMS': '0', 
        })

class QuizResultsTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user_profile = UserProfile.objects.create(user=self.user, username='testuser')


    def test_quiz_results_updates_user_points_easy_quiz(self):
        self.client.login(username='testuser', password='testpassword')
        self.simulate_add_quiz_easy()
        self.quiz = Quiz.objects.first()

        self.user_profile.quizzes_created += 1
        self.user_profile.save()

        session = self.client.session
        session["selected_answers"] = {'question_1' : 1}
        session.save()

        self.client.get(reverse("Quiztopia:quiz_results", kwargs = {
            "category_slug" : self.quiz.category_slug,
            "quiz_id" : self.quiz.quiz_ID
            }))
        self.user_profile.refresh_from_db()

        self.assertEqual(self.user_profile.points, 1)
        print("test_quiz_results_updates_user_points_easy_quiz PASSED")


    def test_quiz_results_updates_user_points_medium_quiz(self):
        self.client.login(username='testuser', password='testpassword')
        self.simulate_add_quiz_medium()
        self.quiz = Quiz.objects.first()

        self.user_profile.quizzes_created += 1
        self.user_profile.save()

        session = self.client.session
        session["selected_answers"] = {'question_1' : 1}
        session.save()

        self.client.get(reverse("Quiztopia:quiz_results", kwargs = {
            "category_slug" : self.quiz.category_slug,
            "quiz_id" : self.quiz.quiz_ID
            }))
        self.user_profile.refresh_from_db()

        self.assertEqual(self.user_profile.points, 2)
        print("test_quiz_results_updates_user_points_medium_quiz PASSED")


    def test_quiz_results_updates_user_points_hard_quiz(self):
        self.client.login(username='testuser', password='testpassword')
        self.simulate_add_quiz_hard()
        self.quiz = Quiz.objects.first()

        self.user_profile.quizzes_created += 1
        self.user_profile.save()

        session = self.client.session
        session["selected_answers"] = {'question_1' : 1}
        session.save()

        self.client.get(reverse("Quiztopia:quiz_results", kwargs = {
            "category_slug" : self.quiz.category_slug,
            "quiz_id" : self.quiz.quiz_ID
            }))
        self.user_profile.refresh_from_db()

        self.assertEqual(self.user_profile.points, 3)
        print("test_quiz_results_updates_user_points_hard_quiz PASSED")


    # Helper Method
    def simulate_add_quiz_easy(self):
        response = self.client.post(reverse("Quiztopia:add_quiz"), {
            'quiz_title': 'Sample Quiz', 
            'category': 'General Knowledge', 
            'difficulty': 'Easy', 
            'upvotes': '0', 
            'questions-TOTAL_FORMS': '1', 
            'questions-INITIAL_FORMS': '0',
            'questions-0-question_text': ['', 'Sample Question'],
            'answers-0-TOTAL_FORMS': '4', 
            'answers-0-INITIAL_FORMS': '0',
            'answers-0-0-answer_text': ['Sample Answer'], 
            'correct_answer_question_0': ['0'], 
            'answers-0-1-answer_text': ['Sample Answer'], 
            'answers-0-2-answer_text': [''], 
            'answers-0-3-answer_text': ['']
        })

    # Helper Method
    def simulate_add_quiz_medium(self):
        response = self.client.post(reverse("Quiztopia:add_quiz"), {
            'quiz_title': 'Sample Quiz', 
            'category': 'General Knowledge', 
            'difficulty': 'Medium', 
            'upvotes': '0', 
            'questions-TOTAL_FORMS': '1', 
            'questions-INITIAL_FORMS': '0',
            'questions-0-question_text': ['', 'Sample Question'],
            'answers-0-TOTAL_FORMS': '4', 
            'answers-0-INITIAL_FORMS': '0',
            'answers-0-0-answer_text': ['Sample Answer'], 
            'correct_answer_question_0': ['0'], 
            'answers-0-1-answer_text': ['Sample Answer'], 
            'answers-0-2-answer_text': [''], 
            'answers-0-3-answer_text': ['']
        })

    # Helper Method
    def simulate_add_quiz_hard(self):
        response = self.client.post(reverse("Quiztopia:add_quiz"), {
            'quiz_title': 'Sample Quiz', 
            'category': 'General Knowledge', 
            'difficulty': 'Hard', 
            'upvotes': '0', 
            'questions-TOTAL_FORMS': '1', 
            'questions-INITIAL_FORMS': '0',
            'questions-0-question_text': ['', 'Sample Question'],
            'answers-0-TOTAL_FORMS': '4', 
            'answers-0-INITIAL_FORMS': '0',
            'answers-0-0-answer_text': ['Sample Answer'], 
            'correct_answer_question_0': ['0'], 
            'answers-0-1-answer_text': ['Sample Answer'], 
            'answers-0-2-answer_text': [''], 
            'answers-0-3-answer_text': ['']
        })


class RegisterTests(TestCase):

    def test_register_user_created(self):
        self.client.post(reverse("Quiztopia:register"), {"username" : "testuser", "password" : "testpassword"})

        self.user = UserProfile.objects.first()
        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.user.username, "testuser")
        print("test_register_user_created PASSED")
        