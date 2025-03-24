# Please see the 'Population Script' section in the README.md for this codes overall explanation

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'Group_Project_11D.settings')

import django
django.setup()
from Quiztopia.models import Quiz, Question, Answer, UserProfile
from django.contrib.auth.models import User

# Imports to handle API requests
import requests # Needs to be installed using pip
import time
import html

# Import to show the progress of the script
from tqdm import tqdm # Needs to be installed using pip

def populate():
    # CREATING THE USERS
    print('Creating users...')
    example_users = ['Tshimollo', 'Shane', 'Jack', 'Uuri', 'Shay']

    for user in example_users:
        add_user(user)
        u = User.objects.get(username=user)
        u.set_password(f'{user}123')
        u.save()

    # Print the users we have added
    for u in UserProfile.objects.all():
        print(f'- User {u.username} was successfully created.')
    
    print('Completed creating users.')

    # CREATING THE QUIZZES
    print('Creating quizzes...')
    
    # Using the Open Trivia DB (https://opentdb.com) to import quiz questions. No changes were made.
    quiz_api_urls = ['https://opentdb.com/api.php?amount=5&category=9&difficulty=easy&type=multiple',           # General Knowledge - Easy - 5 questions 
                     'https://opentdb.com/api.php?amount=7&category=9&difficulty=medium&type=multiple',         # General Knowledge - Medium - 7 questions
                     'https://opentdb.com/api.php?amount=10&category=9&difficulty=hard&type=multiple',          # General Knowledge - Hard - 10 questions
                     'https://opentdb.com/api.php?amount=5&category=21&difficulty=easy&type=multiple',          # Sports - Easy - 5 questions
                     'https://opentdb.com/api.php?amount=7&category=21&difficulty=medium&type=multiple',        # Sports - Medium - 7 questions
                     'https://opentdb.com/api.php?amount=10&category=21&difficulty=hard&type=multiple',         # Sports - Hard - 10 questions
                     'https://opentdb.com/api.php?amount=5&difficulty=easy&type=multiple',                      # Other - Easy - 5 questions
                     'https://opentdb.com/api.php?amount=7&difficulty=medium&type=multiple',                    # Other - Medium - 7 questions
                     'https://opentdb.com/api.php?amount=10&difficulty=hard&type=multiple',                     # Other - Hard - 10 questions
                     'https://opentdb.com/api.php?amount=5&category=27&difficulty=easy&type=multiple',          # Animals - Easy - 5 questions
                     'https://opentdb.com/api.php?amount=7&category=27&difficulty=medium&type=multiple',        # Animals - Medium - 7 questions
                     'https://opentdb.com/api.php?amount=10&category=27&difficulty=hard&type=multiple',         # Animals - Hard - 10 questions
                     'https://opentdb.com/api.php?amount=5&category=14&difficulty=easy&type=multiple',          # Movies and TV - Easy - 5 questions
                     'https://opentdb.com/api.php?amount=7&category=14&difficulty=medium&type=multiple',        # Movies and TV - Medium - 7 questions
                     'https://opentdb.com/api.php?amount=10&category=14&difficulty=hard&type=multiple']         # Movies and TV - Hard - 10 questions

    category_options = ['General Knowledge', 'Sports', 'Other', 'Animals', 'Movies And TV']
    difficulty_options = ['Easy', 'Medium', 'Hard']

    for i in tqdm(range(len(quiz_api_urls))):
        response = requests.get(quiz_api_urls[i])
        quizData = response.json()
        results = quizData.get('results')

        # Check if results is valid
        if not results:
            print(f"Error: No results found for URL {quiz_api_urls[i]}")
            continue

        # Determine quiz title, category, and difficulty
        category_index = (i // 3) % len(category_options) # Changes iteration every 3 quizzes
        difficulty_index = i % len(difficulty_options) # Changes iteration every quiz
        quiz_title = f"{category_options[category_index]} - {difficulty_options[difficulty_index]}"
        category = category_options[category_index]
        difficulty = difficulty_options[difficulty_index]
        upvotes = 0
        creator = UserProfile.objects.get(username=example_users[i % len(example_users)])

        # Create or get the quiz
        quiz = add_quiz(quiz_title, category, difficulty, upvotes, creator)

        # Add questions and answers to the quiz
        for j in range(len(results)):
            question_text = html.unescape(results[j].get('question'))
            question = add_question(question_text, quiz)
            correct_answer = html.unescape(results[j].get('correct_answer'))
            incorrect_answers = results[j].get('incorrect_answers') 

            # Add incorrect answers
            for answer in incorrect_answers:
                add_answer(html.unescape(answer), question[0], False)

            # Add correct answer
            add_answer(correct_answer, question[0], True)

        # The script needs to wait 5 seconds for the API to respond
        time.sleep(5)
    
    print('Completed creating quizzes.')

    # Print the quizzes we have added
    for q in Quiz.objects.all():
        print(f'- Quiz {q.quiz_title} was successfully created.')

def add_quiz(name, cat, diff, upvotes, creator):
    q, created = Quiz.objects.get_or_create(
        quiz_title=name,
        category=cat,
        difficulty=diff,
        creator=creator,
        defaults={'upvotes': upvotes}
    )
    if not created:
        q.upvotes = upvotes
        q.save()

    # Update the creator's quizzes_created field
    u = UserProfile.objects.get(username=creator.username)
    u.quizzes_created += 1
    u.save()
    return q

def add_question(text, quiz):
    q = Question.objects.get_or_create(
        question_text=text,
        quiz_ID=quiz
    )
    return q

def add_answer(text, question, answer):
    a = Answer.objects.get_or_create(
        answer_text=text,
        question_ID=question,
        defaults={'is_correct': answer}
    )
    return a
    
def add_user(name, image=None, points=0, quizzes_taken=0, quizzes_created=0):
    # Create or get the User object
    user, created = User.objects.get_or_create(username=name)
    
    # Create or get the UserProfile object
    try:
        u, created = UserProfile.objects.get_or_create(
            user=user,
            defaults={
                'username': name,  # Use the username field in UserProfile
                'profile_picture': image,
                'points': points,
                'quizzes_taken': quizzes_taken,
                'quizzes_created': quizzes_created
            }
        )
    except UserProfile.DoesNotExist:
        # If the UserProfile does not exist, create it manually
        u = UserProfile(
            user=user,
            username=name,
            profile_picture=image,
            points=points,
            quizzes_taken=quizzes_taken,
            quizzes_created=quizzes_created
        )

    # Update fields if the UserProfile already exists
    if not created:
        u.profile_picture = image
        u.points = points
        u.quizzes_taken = quizzes_taken
        u.quizzes_created = quizzes_created
        u.save()
    return u

# The script starts running here
if __name__ == '__main__':
    print('Starting Quiztopia population script...')
    populate()
    print('Quiztopia population script completed.')