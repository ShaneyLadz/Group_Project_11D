from django.contrib import admin
from Quiztopia.models import UserProfile, Quiz, Question, Answer

class UserProfileAdmin(admin.ModelAdmin):

    list_display = ('user', 'username', 'points', 'quizzes_taken', 'quizzes_created','profile_picture')

class QuizAdmin(admin.ModelAdmin):

    list_display = ('quiz_ID', 'quiz_title', 'category', 'difficulty','upvotes','creator', 'category_slug')

class QuestionAdmin(admin.ModelAdmin):

    list_display = ('question_ID','question_text','quiz_ID')

class AnswerAdmin(admin.ModelAdmin):

    list_display = ('answer_ID','answer_text','is_correct','question_ID')

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)

