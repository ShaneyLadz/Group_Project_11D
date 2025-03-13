from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from Quiztopia.forms import QuizForm, QuestionForm, AnswerForm

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
        return render(request, 'Quiztopia/login.html')#
    
@login_required
def add_quiz(request):
    form = QuizForm()

    if request.method == 'POST':
        form = QuizForm(request.POST)

        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.creator = request.user
            form.save(commit=True)
            return redirect('/Quiztopia/')
        else:
            print(form.errors)
    
    return render(request, 'Quiztopia/add_quiz.html', {'form': form})