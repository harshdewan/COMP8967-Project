import os
import pickle
import re
import requests
import nltk
from django.http import HttpResponse
from django.shortcuts import render, redirect
from rake_nltk import Rake
from six.moves.urllib.parse import quote
from users.models import UserDetails, Post
from django.urls import reverse


nltk.download('stopwords')
nltk.download('punkt')


def signup(request):
    if request.method == 'POST':
        req_email_id = request.POST['email']
        req_password = request.POST['password']
        req_confirm_password = request.POST['confirm_password']
        if req_confirm_password != req_password:
            print('password and confirmation do not match')
            return render(request, 'users/signup.html', context={'message':'Password and Confirm Password did not '
                                                                           'match, Please Try Again'})
        user = UserDetails.objects.create(
            email_id=req_email_id,
            password=req_password
        )
        user_id = user.id
        print('New user created with id: ', user_id)
        return render(request, 'users/login.html')
    return render(request, 'users/signup.html', {'message': ''})


def login(request):
    if request.method == 'POST':
        login_email = request.POST['login_email']
        login_password = request.POST['login_password']

        # Check if the email exists in the Student table
        user1 = UserDetails.objects.filter(email_id=login_email).first()
        if not user1:
            return render(request, 'users/login.html', {'message': 'Invalid email. Please try again.'})

        # Check if the password exists in the StudentPassword table for the corresponding student_id
        user1_password = user1.password
        if user1_password == login_password:
            # If login is successful, redirect to the course_selection page
            url = reverse('home', args=[user1.id])
            return redirect(url)
        else:
            return render(request, 'users/login.html', {'message': 'Invalid password. Please try again.'})

    return render(request, 'users/login.html', {'message': ''})


def home(request, user_id):
    print('user_id is:', user_id)
    user_details = UserDetails.objects.get(id=user_id) ##this will give us email id
    posts = Post.objects.filter(user_id=user_id)
    #fetch all posts with respect to user_id and pass it to home.html page context
    return render(request, 'users/home.html', {'user_id':user_id, 'posts':posts, 'user_email':user_details.email_id})


def logout(request):
    return render(request, 'users/login.html', {'message': ''})


def userpost(request, user_id):
    print('userpost page, user_id: ', user_id)
    fullName = UserDetails.objects.get(id=user_id).email_id
    if request.method == 'POST':
        user_postData = request.POST['userpost_content']
        print('user has entered: ', user_postData)
        if not user_postData:
            return render(request, 'users/user_post.html',{'user_name':fullName, 'user_id': user_id})
        print('checking for spam and fraud!')
        if detect_scam_words([user_postData]):
            print('text analyze userpost looks like scam!!')
            return render(request, 'users/user_post.html', {'display_message': 'Post is not valid due to spam content.', 'user_name': fullName, 'user_id': user_id})
        elif detect_spam(user_postData):
            print('urls check userpost looks like scam!!')
            return render(request, 'users/user_post.html', {'display_message': 'Post is not valid due to spam content.', 'user_name': fullName, 'user_id': user_id})
        else:
            print('userpost is fine to post!!')
        Post.objects.create(
            user_id=user_id,
            content=user_postData
        )
        return render(request, 'users/user_post.html', {'display_message': 'Post submitted successfully.', 'user_name': fullName, 'user_id': user_id})
    return render(request, 'users/user_post.html', {'user_name': fullName, 'user_id': user_id})
    #url = reverse('mypost', args=[user_id])
    #print('url reverse is: ', url)
    #return redirect(url)
    #return render(request, 'users/user_post.html', {'user_name': fullName, 'display_message': ''})


def check_if_post_valid(request):
    return render(request, 'users/user_post.html')


def load_models():
    # Load CountVectorizer
    with open(os.path.join(os.path.dirname(__file__), 'ml_model', 'count_vector.pkl'), 'rb') as f:
        count_vectorizer = pickle.load(f)

    # Load Naive Bayes classifier
    with open(os.path.join(os.path.dirname(__file__), 'ml_model', 'model.pkl'), 'rb') as f:
        naive_bayes1 = pickle.load(f)

    return count_vectorizer, naive_bayes1


def detect_scam_words(text):
    count_vectorizer, naive_bayes1 = load_models()
    # Ensure the input is a list of strings
    if not isinstance(text, list) or not all(isinstance(t, str) for t in text):
        raise ValueError("Input text should be a list of strings.")

    # Transform the text data
    try:
        predictors = count_vectorizer.transform(text)
    except Exception as e:
        raise ValueError("Error in transforming text data: {e}")

    # Predict using Naive Bayes
    try:
        result = naive_bayes1.predict(predictors)
    except Exception as e:
        raise ValueError("Error in prediction: {e}")

    # Calculate the average of predictions
    average = sum(result) / len(result)

    # Determine if the average prediction indicates a scam
    return average >= 0.4


# Function to extract keywords from text
def keyword(key):
    r = Rake()
    r.extract_keywords_from_text(key)
    a = r.get_ranked_phrases()
    return a


# Function to extract URLs from text
def url_extract(text):
    url_pattern = r"\b((?:https?://)?(?:(?:www\.)?(?:[\da-z\.-]+)\.(?:[a-z]{2,6})|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])))(?::[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])?(?:/[\w\.-]*)*/?)\b"
    check_urls = re.findall(url_pattern, text)
    return check_urls


# Function to check if a URL is a scam
def is_scam(url_query):
    for url in url_query:
        ii = url.replace("/", "%2F")
        req = "https://www.ipqualityscore.com/api/json/url/MdoNe2UZwelnq6u39GwgBYre2rqz3uNH/" + quote(ii)
        resp = requests.get(req)
        if resp.status_code == 200:
            result = resp.json()
            spam = result.get('spamming', False)
            malware = result.get('malware', False)
            suspicious = result.get('suspicious', False)
            phishing = result.get('phishing', False)
            unsafe = result.get('unsafe', False)
            risk_score = result.get('risk_score', 0)

            if spam or malware or suspicious or phishing or unsafe or risk_score > 75:
                return True

    return False


def detect_spam(text):
    keywords = keyword(text)
    print('keywords: ', keywords)
    urls = url_extract(text)
    scam_result = is_scam(urls)
    if scam_result:
        return True
    return False
