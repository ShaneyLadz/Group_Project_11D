from django import forms 
from Quiztopia.models import Quiz, Question, Answer

class QuizForm(forms.ModelForm):

    quiz_title = forms.CharField(max_length=200, help_text="Quiz Name:")
    category = forms.ChoiceField(choices=Quiz.categories, help_text="Category:")
    difficulty = forms.ChoiceField(choices=Quiz.difficulties, help_text="Difficulty:")
    upvotes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Quiz
        fields = ('quiz_title','category','difficulty')

class QuestionForm(forms.ModelForm):

    question_text = forms.CharField(max_length=500, help_text="Enter your question")

    class Meta:
        model = Question
        fields = ('question_text',)

class AnswerForm(forms.ModelForm):

    answer_text = forms.CharField(max_length=200, help_text="Enter an answer")
    is_correct = forms.BooleanField()

    class Meta:
        model = Answer
        fields = ('answer_text',)
