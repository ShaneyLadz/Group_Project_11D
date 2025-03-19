from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from Quiztopia.forms import QuizForm, QuestionForm, AnswerForm, AnswerFormSet, QuestionFormSet
from Quiztopia.models import UserProfile, Question, Quiz, Answer

CATEGORIES = [
    ("Movies And TV", "Movies And TV"),
    ("Animals", "Animals"),
    ("General Knowledge", "General Knowledge"),
    ("Sports", "Sports"),
    ("Other", "Other"),
]

def index(request):
    return render(request, 'Quiztopia/index.html', {'categories': CATEGORIES})

def category_view(request, category_name):
    quizzes = Quiz.objects.filter(category=category_name)
    return render(request, 'Quiztopia/category.html', {'quizzes': quizzes, 'category_name': category_name})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('Quiztopia:index'))
            else:
                return HttpResponse("Your Quiztopia account is disabled.")
            
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
        
    else:
        return render(request, 'Quiztopia/login.html')
    
@login_required
def add_quiz(request):

    if request.method == 'POST':
        form = QuizForm(request.POST)
        question_formset = QuestionFormSet(request.POST, prefix="questions")



        if form.is_valid() and question_formset.is_valid():
            creator = UserProfile.objects.get(user=request.user)
            quiz = form.save(commit=False)
            quiz.creator = creator
            form.save(commit=True)
        
            
            for i, question_form in enumerate(question_formset):
                    if question_form.cleaned_data:
                        question = question_form.save(commit=False)
                        question.quiz_ID = quiz
                        question.save()

                      


                        answer_formset = AnswerFormSet(request.POST, prefix=f'answers-{i}')
                        
                        if answer_formset.is_valid():
                            answers = answer_formset.save(commit=False)
                            correct_answer_index = request.POST.get(f'correct_answer_question_{i}')
                            for j, answer in enumerate(answers):
                                if int(correct_answer_index) == j:
                                    answer.is_correct = True
                                else:
                                    answer.is_correct = False
                                answer.question_ID = question
                                answer.save()

            return redirect('/Quiztopia/')
        
    else:
        form = QuizForm()
        question_formset = QuestionFormSet(prefix="questions")
        answer_formsets = [AnswerFormSet(prefix=f'answers-{i}') for i in range(10)]
        question_answer_pairs = zip(question_formset, answer_formsets)


    return render(request, 'Quiztopia/add_quiz.html', {'form' : form, 'questions' : question_formset, 'questions_and_answers' : question_answer_pairs})


def take_quiz(request, category_slug, quiz_id):
    
    if request.method == 'POST':
        user = UserProfile.objects.get(user = request.user)
        user.quizzes_taken += 1
        user.save()

        # Radio buttons which user selected for each question
        # Note, you'll want these for quiz_results
        selected_answers = {}
        questions = Question.objects.filter(quiz_ID = quiz_id)

        i = 1
        while i <= len(questions):
            selected_answers[f"question_{i}"] = request.POST.get(str(i))
            i += 1

        return redirect(reverse("Quiztopia:quiz_results",
                                kwargs = {"category_slug" : category_slug,
                                          "quiz_id" : quiz_id}))

    else:
        context_dict = {}
        try:
            quiz = Quiz.objects.get(quiz_ID = quiz_id, category_slug = category_slug)
            questions = Question.objects.filter(quiz_ID = quiz_id)
        except Quiz.DoesNotExist:   
            quiz = None

        if quiz is None:
            return HttpResponse("Quiz Does Not Exist.")

        context_dict["quiz"] = quiz
        context_dict["questions_answers"] = []

        for question in questions:
            answers = Answer.objects.filter(question_ID = question.question_ID)
            context_dict["questions_answers"].append((question, answers))

        return render(request, 'Quiztopia/take_quiz.html', context_dict)
    

def quiz_results(request, category_slug, quiz_id):
    return HttpResponse("This view is in progress")