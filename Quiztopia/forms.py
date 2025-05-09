from django import forms 
from Quiztopia.models import Quiz, Question, Answer, User, UserProfile
from django.forms import inlineformset_factory, modelformset_factory

class QuizForm(forms.ModelForm):

    quiz_title = forms.CharField(max_length=200)
    category = forms.ChoiceField(choices=Quiz.categories)
    difficulty = forms.ChoiceField(choices=Quiz.difficulties)
    upvotes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Quiz
        fields = ('quiz_title','category','difficulty')

class QuestionForm(forms.ModelForm):

    question_text = forms.CharField(widget=forms.HiddenInput(),max_length=500,required=True)

    class Meta:
        model = Question
        fields = ('question_text',)

class AnswerForm(forms.ModelForm):

    answer_ID = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    answer_text = forms.CharField(max_length=200, help_text="Enter an answer")
    is_correct = forms.BooleanField(required=False,widget=forms.RadioSelect())

    class Meta:
        model = Answer
        fields = ('answer_text','is_correct','answer_ID')

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('profile_picture',)

class EditQuestionForm(forms.ModelForm):

    question_text = forms.CharField(max_length=500,required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Question
        fields = ('question_text',)

        


QuestionFormSet = modelformset_factory(Question, form=QuestionForm, extra=10,min_num=0,max_num=10)
AnswerFormSet = inlineformset_factory(Question, Answer, form=AnswerForm, extra=4, max_num=4, can_delete=False)
EditQuestionFormSet = modelformset_factory(Question, form=EditQuestionForm, extra=0,min_num=0,max_num=10)
