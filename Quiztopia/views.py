from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from Quiztopia.forms import QuizForm, AnswerFormSet, QuestionFormSet, UserForm, UserProfileForm, EditQuestionFormSet
from Quiztopia.models import UserProfile, Question, Quiz, Answer
import json
import os

CATEGORIES = [
    "movies-and-tv", "animals", "general-knowledge", "sports", "other"
]

def index(request):
    top_users = UserProfile.objects.order_by("-points")[:10]
    return render(request, 'Quiztopia/index.html', {'categories': CATEGORIES, 'top_users' : top_users})

def categories_view(request):
    return render(request, 'Quiztopia/categories.html', {'categories' : CATEGORIES})

def category_view(request, category_slug):
    quizzes = Quiz.objects.filter(category_slug=category_slug)
    return render(request, 'Quiztopia/category.html', {'quizzes': quizzes, 'category_name': category_slug})

def about(request):
    return render(request, 'Quiztopia/about.html')

def faq(request):
    return render(request, 'Quiztopia/faq.html')

def register(request):
    registered = False
    
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.username = user.username

            if 'profile_picture' in request.FILES:
                profile.profile_picture = request.FILES['profile_picture']
            else:
                profile.profile_picture = 'profile_pictures/default_profile.jpg'
            
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'Quiztopia/register.html', context={'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

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
def user_logout(request):
    logout(request)
    return redirect(reverse('Quiztopia:index'))
    
@login_required
def add_quiz(request):

    if request.method == 'POST':
        form = QuizForm(request.POST)
        question_formset = QuestionFormSet(request.POST, prefix="questions", queryset=Question.objects.none())



        if form.is_valid() and question_formset.is_valid():
            creator = UserProfile.objects.get(user=request.user)
            quiz = form.save(commit=False)
            quiz.creator = creator
            form.save(commit=True)
        
            creator.quizzes_created += 1
            creator.save()
            
            for i, question_form in enumerate(question_formset):
                    if question_form.cleaned_data:
                        question = question_form.save(commit=False)
                        question.quiz_ID = quiz
                        question.save()

                      


                        answer_formset = AnswerFormSet(request.POST, instance=question, prefix=f'answers-{i}')
                        
                        if answer_formset.is_valid():
                            answers = answer_formset.save(commit=False)
                            correct_answer_index = request.POST.get(f'correct_answer_question_{i}')
                            if correct_answer_index == "3" and len(answers) == 3:
                                correct_answer_index = 2
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
        question_formset = QuestionFormSet(prefix="questions", queryset=Question.objects.none())
        answer_formsets = [AnswerFormSet(prefix=f'answers-{i}') for i in range(10)]
        question_answer_pairs = zip(question_formset, answer_formsets)

    return render(request, 'Quiztopia/add_quiz.html', {'form' : form, 'questions' : question_formset, 'questions_and_answers' : question_answer_pairs})


@login_required
def edit_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, quiz_ID=quiz_id)  
    questions = Question.objects.filter(quiz_ID=quiz_id)  
    
    if request.method == 'POST':
        quiz_form = QuizForm(request.POST, instance=quiz)
        question_formset = EditQuestionFormSet(request.POST, prefix="questions", queryset=questions)

        if quiz_form.is_valid() and question_formset.is_valid():
            quiz_form.save() 


            for i, question_form in enumerate(question_formset):
                question = question_form.save(commit=False)
                question.quiz_ID = quiz 
                question.save()

                answer_formset = AnswerFormSet(request.POST, instance=question, prefix=f'answers-{i}')
                if answer_formset.is_valid():
                    number_of_answers = len(Answer.objects.filter(question_ID = question.question_ID))
                    correct_answer_index = request.POST.get(f'correct_answer_question_{i}')
                    for j in range(number_of_answers):
                        answer = answer_formset[j].save(commit=False)
                        if answer != "":
                            if int(correct_answer_index) == j:
                                answer.is_correct = True
                            else:
                                answer.is_correct = False
                            answer.question_ID = question
                            answer.save()

            return redirect('/Quiztopia/') 

    else:
        quiz_form = QuizForm(instance=quiz)
        question_formset = EditQuestionFormSet(prefix="questions", queryset=questions)
        answer_formsets = [AnswerFormSet(instance=questions[i], prefix=f'answers-{i}') for i in range(len(questions))]
        question_answer_pairs = zip(question_formset, answer_formsets)

    return render(request, 'Quiztopia/edit_quiz.html', {'form': quiz_form, 'questions' : question_formset, 'questions_and_answers': question_answer_pairs, "quiz_id" : quiz_id})

def take_quiz(request, category_slug, quiz_id):
    
    if request.method == 'POST':

        if request.user.is_authenticated:
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

        request.session["selected_answers"] = selected_answers

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
    if request.method == 'POST':
        # This code will run when the thumbs-up or thumbs-down is clicked
        # on the quiz results page.
        try:
            data = json.loads(request.body)

            quiz = Quiz.objects.get(quiz_ID = quiz_id, category_slug = category_slug)
            if data["vote"] == "upvote":
                quiz.upvotes += 1
            elif data["vote"] == "downvote":
                quiz.upvotes -= 1
            quiz.save()

            return JsonResponse({})
        
        except json.JSONDecodeError:
            # When the return-to-homepage button is clicked, this code will run since a
            # json request is not being processed (from clicking thumbs-up or thumbs-down).
            return redirect(reverse("Quiztopia:index"))
        
    else:
        selected_answers = request.session.get("selected_answers")

        context_dict = {}
        quiz = Quiz.objects.get(quiz_ID = quiz_id, category_slug = category_slug)
        questions = Question.objects.filter(quiz_ID = quiz_id)

        context_dict["quiz"] = quiz
        context_dict["questions_answers_selections"] = []
        context_dict["no_questions"] = len(questions)

        for index, question in enumerate(questions):
            answers = Answer.objects.filter(question_ID = question.question_ID)
            selected_answer = selected_answers[f"question_{index+1}"]

            context_dict["questions_answers_selections"].append((question, answers, int(selected_answer)))

        score, no_correct = compute_results(context_dict)

        # If score is -1, then template will not display score
        context_dict["score"] = -1
        context_dict["no_correct"] = no_correct
        
        if request.user.is_authenticated:
            user = UserProfile.objects.get(user = request.user)
            user.points += score
            user.save()

            # User is logged in, so we want to display the score they earned
            context_dict["score"] = score

        return render(request, 'Quiztopia/quiz_results.html', context_dict)


def compute_results(context_dict):

    EASY_MULTIPLIER = 1
    MEDIUM_MULTIPLIER = 2
    HARD_MULTIPLIER = 3

    no_correct = 0
    for question, answers, selected in context_dict["questions_answers_selections"]:
        # Since answers start at index 0, selected is decremented
        selected_answer = answers[selected-1]

        if selected_answer.is_correct:
            no_correct += 1

    quiz = context_dict["quiz"]
    multiplier = 0

    if quiz.difficulty == "Easy":
        multiplier = EASY_MULTIPLIER
    elif quiz.difficulty == "Medium":
        multiplier = MEDIUM_MULTIPLIER
    elif quiz.difficulty == "Hard":
        multiplier = HARD_MULTIPLIER

    return no_correct * multiplier, no_correct

@login_required
def profile(request):
    if request.method == "POST":
        if request.POST.get("add_quiz"):
            return redirect(reverse("Quiztopia:add_quiz"))
        
        elif request.POST.get("edit_quiz"):
            quiz_id = request.POST.get("edit_quiz")
            return redirect(reverse("Quiztopia:edit_quiz",
                                     kwargs={"quiz_id" : quiz_id}))
        
        # Request to delete a quiz
        if request.content_type == "application/json":
            data = json.loads(request.body)
            quiz_id = data["selected"]
            quiz = Quiz.objects.get(quiz_ID = quiz_id)

            quiz.delete()

            quiz.creator.quizzes_created -= 1
            quiz.creator.save()

            return JsonResponse({})

        # Request to change profile picture
        elif request.content_type == "multipart/form-data":
            form = UserProfileForm(request.POST, request.FILES)
            if form.is_valid():
                user = UserProfile.objects.get(user = request.user)

                DEFAULT_PROFILE_PICTURES = [
                    "profile_pictures/default_profile.jpg",
                    "profile_pictures/profile_1.png",
                    "profile_pictures/profile_2.png",
                    "profile_pictures/profile_3.png",
                    "profile_pictures/profile_4.png"
                    "profile_pictures/profile_5.png"
                ]

                # Deleting a user's old profile picture from the media folder,
                # unless it's in the DEFAULT_PROFILE_PICTURES list
                if user.profile_picture not in DEFAULT_PROFILE_PICTURES:
                    old_profile_picture = user.profile_picture

                    #path = os.path.join(settings.MEDIA_ROOT, old_profile_picture.name)
                    path = old_profile_picture.path
                    os.remove(path)

                user.profile_picture = request.FILES["profile_picture"]
                user.save()
                
                return JsonResponse({"url" : user.profile_picture.url,})

    else:
        user = UserProfile.objects.get(user = request.user)
        quizzes = Quiz.objects.filter(creator = user.username)
        
        return render(request, 'Quiztopia/profile.html', {"user" : user, "quizzes" : quizzes})