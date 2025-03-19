from django.urls import path
from Quiztopia import views 

app_name = 'Quiztopia'

urlpatterns = [
    path('', views.index, name = "index"),
    path('login/', views.user_login, name='login'),
    path('add_quiz/', views.add_quiz, name='add_quiz'),
    path('categories/<str:category_slug>/<int:quiz_id>/take_quiz/', views.take_quiz, name = 'take_quiz'),
    path('categories/<str:category_slug>/<int:quiz_id>/take_quiz/quiz_results/', views.quiz_results, name = "quiz_results")
]