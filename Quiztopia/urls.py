from django.urls import path
from Quiztopia import views

app_name = 'Quiztopia'

urlpatterns = [
    path('', views.index, name = "index"),
    path('login/', views.user_login, name='login'),
    path('add_quiz/', views.add_quiz, name='add_quiz'),
    path('register/', views.register, name='register'),
    path('categories/', views.categories_view, name="categories"),
    path('categories/<str:category_slug>/', views.category_view, name="category"),
    path('categories/<str:category_slug>/<int:quiz_id>/take_quiz/', views.take_quiz, name = 'take_quiz'),
    path('categories/<str:category_slug>/<int:quiz_id>/take_quiz/quiz_results/', views.quiz_results, name = "quiz_results"),
    path('logout/', views.user_logout, name='logout'),
    path('login/profile', views.profile, name='profile'),
    path('edit_quiz/<int:quiz_id>/', views.edit_quiz, name='edit_quiz'),
    path('about', views.about, name='about'),
    path('faq', views.faq, name="faq"),
]