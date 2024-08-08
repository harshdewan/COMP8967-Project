import json
import os
import pickle
import re
from datetime import datetime

import requests
import nltk
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from rake_nltk import Rake
from six.moves.urllib.parse import quote
from users.models import UserDetails, Post, Friends, LikedPosts, SavedPosts
from django.urls import reverse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

nltk.download('stopwords')
nltk.download('punkt')


def signup(request):
    if request.method == 'POST':
        req_email_id = request.POST['email']
        req_password = request.POST['password']
        req_confirm_password = request.POST['confirm_password']
        if req_confirm_password != req_password:
            return render(request, 'users/signup.html', context={'message': 'Password and Confirm Password did not '
                                                                            'match, Please Try Again'})
        user = UserDetails.objects.create(
            email_id=req_email_id,
            password=req_password
        )
        user_id = user.id
        return redirect('editprofile', user_id=user_id)
    return render(request, 'users/signup.html', {'message': ''})


def login(request):
    if request.method == 'POST':
        login_email = request.POST['login_email']
        login_password = request.POST['login_password']
        user1 = UserDetails.objects.filter(email_id=login_email).first()
        if not user1:
            return render(request, 'users/login.html', {'message': 'Invalid email. Please try again.'})
        user1_password = user1.password
        if user1_password == login_password:
            url = reverse('home', args=[user1.id])
            return redirect(url)
        else:
            return render(request, 'users/login.html', {'message': 'Invalid password. Please try again.'})
    return render(request, 'users/login.html', {'message': ''})


def home(request, user_id):
    print('user_id is:', user_id)
    user_details = UserDetails.objects.get(id=user_id)
    posts = list(Post.objects.filter(user_id=user_id))
    print("posts details: ", posts.__str__())
    followingUsersIds = Friends.objects.filter(userFollower=user_details)
    myPosts = Post.objects.filter(user_id=user_details)
    postContext = []
    for post in myPosts:
        if post.spamReported < 2:
            checkIfSaved = SavedPosts.objects.filter(user=user_details, post=post)
            if checkIfSaved:
                postContext.append({'post': post, 'isSaved': True})
            else:
                postContext.append({'post': post, 'isSaved': False})
    for user in followingUsersIds:
        tempPostObjecst = (Post.objects.filter(user_id=user.userFollowed.id))
        for post in tempPostObjecst:
            if post.spamReported < 2:
                checkIfSaved = SavedPosts.objects.filter(user=user_details, post=post)
                if checkIfSaved:
                    postContext.append({'post':post, 'isSaved':True})
                else:
                    postContext.append({'post': post, 'isSaved': False})
    return render(request, 'users/home.html', {'user_id': user_id, 'postContext': postContext, 'user_email': user_details.email_id})


def logout(request):
    return render(request, 'users/login.html', {'message': ''})


def userpost(request, user_id):
    print('userpost page, user_id: ', user_id)
    fullName = UserDetails.objects.get(id=user_id)
    # usr = UserDetails.objects.get(id=user_id)
    if request.method == 'POST':
        user_postData = request.POST['userpost_content']
        if not user_postData:
            return render(request, 'users/user_post.html',
                          {'user_name': fullName, 'user_id': user_id, 'userpost_content': user_postData})
        print('checking for spam and fraud!')
        if detect_scam_words([user_postData]):
            print('text analyze userpost looks like scam!!')
            Post.objects.create(
                user_id=user_id,
                content=user_postData,
                isScam=True
            )
            return render(request, 'users/user_post.html',
                          {'display_message': 'Post is not valid due to spam content.', 'user_name': fullName,
                           'user_id': user_id, 'userpost_content': user_postData, 'isScam': True})
        elif detect_spam(user_postData):
            Post.objects.create(
                user_id=user_id,
                content=user_postData,
                isScam=True
            )
            print('urls check userpost looks like scam!!')
            return render(request, 'users/user_post.html',
                          {'display_message': 'Post is not valid due to spam content.', 'user_name': fullName,
                           'user_id': user_id, 'userpost_content': user_postData, 'isScam': True})
        else:
            print('userpost is fine to post!!')
            Post.objects.create(
                user_id=user_id,
                content=user_postData,
                isScam=False
            )
        return render(request, 'users/user_post.html',
                      {'display_message': 'Post submitted successfully.', 'user_name': fullName, 'user_id': user_id,
                       'userpost_content': ""})
    return render(request, 'users/user_post.html', {'user_name': fullName, 'user_id': user_id, 'userpost_content': ""})
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


def explore(request):
    return HttpResponse('Explore Page')


def following(request, user_id):
    following = False
    followingList = []
    user_details = UserDetails.objects.get(id=user_id)
    followingUsersIds = Friends.objects.filter(userFollower=user_details)
    for user in followingUsersIds:
        following = True
        followingList.append(UserDetails.objects.get(id=user.userFollowed.id))
    print("following: ", following)
    print("followingList: ", followingList)
    print("followingList_length: ", len(followingList))
    print("followinguserIds: ", followingUsersIds)
    return render(request, 'users/followings.html', {'user_id': user_id, 'user_details': user_details, 'following': following, 'followingList':followingList})


def notificationView(request):
    return HttpResponse('Notification Page')


def notificationView(request, user_id):
    user_details = UserDetails.objects.get(id=user_id)
    return render(request, 'users/notification.html', {'user_id': user_id, 'user_details': user_details})


def messagesView(request):
    return HttpResponse('Messages Page')


def savedpostsView(request, user_id):
    user_details = UserDetails.objects.get(id=user_id)
    savedPostsSet = SavedPosts.objects.filter(user=user_details)
    savedPostsPresent = False
    savedPosts = []
    if savedPostsSet:
        savedPostsPresent = True
        for post in savedPostsSet:
            print("post_id: ", post.post_id)
            savedPosts.append(Post.objects.get(id=post.post_id))
        print("savedPosts: ", len(savedPosts))
    return render(request, 'users/savedpost.html', {'user_id': user_id, 'user_details': user_details, 'savedPosts': savedPosts, 'savedPostsPresent':savedPostsPresent})


def searchView(request, user_id):
    user_details = UserDetails.objects.get(id=user_id)
    allUsers = UserDetails.objects.all()
    allUsersFollowing = []
    tempList = Friends.objects.filter(userFollower=user_details)
    for user in tempList:
        allUsersFollowing.append(UserDetails.objects.get(id=user.userFollowed.id))
    suggestedFriends = []
    for user in allUsers:
        if user not in allUsersFollowing:
            suggestedFriends.append(user)
    return render(request, 'users/search.html', {'user_id': user_id, 'user_details': user_details, 'userList': suggestedFriends,
                                                 'suggestedPeoplePresent': True})


def profileView(request, user_id):
    user_details = UserDetails.objects.get(id=user_id)
    return render(request, 'users/profile.html', {'user_id': user_id, 'user_details': user_details})


def myFollowersView(request, user_id):
    user_details = UserDetails.objects.get(id=user_id)
    allUsers = UserDetails.objects.all()
    allUsersFollowers = []
    tempList = Friends.objects.filter(userFollowed=user_details)
    followers=False
    if tempList:
        followers=True
    for user in tempList:
        allUsersFollowers.append(UserDetails.objects.get(id=user.userFollower.id))
    return render(request, 'users/followers.html',
                  {'user_id': user_id, 'user_details': user_details, 'followerList': allUsersFollowers,
                   'followers': followers})


def myPostsViews(request, user_id):
    user_details = UserDetails.objects.get(id=user_id)
    myPostsPresent = False
    posts = Post.objects.filter(user_id=user_details)
    if posts:
        myPostsPresent = True
    return render(request, 'users/myposts.html',
                  {'user_id': user_id, 'user_details': user_details, 'posts': posts,'myPostsPresent': myPostsPresent})


def changePasswordView(request, user_id):
    user_details = UserDetails.objects.get(id=user_id)
    return render(request, 'users/changepassword.html', {'user_id': user_id, 'user_details': user_details})


def communitiesView(request, user_id):
    return render(request, 'users/communities.html', {'user_id': user_id})


def editProfileView(request, user_id):
    user = get_object_or_404(UserDetails, id=user_id)
    if request.method == "POST":
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email_id = request.POST['email']
        user.username = request.POST['username']
        user.city = request.POST['city']
        user.country = request.POST['country']
        user.password = request.POST['password']
        user.save()
        return redirect('profile', user_id=user.id)

    return render(request, 'users/editprofile.html', {'user': user, 'user_id': user.id})


def updateFollowing(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print("data received: ", data)
        user_to_follow_id = data.get('user_id2')
        current_user_id = data.get('user_id1')
        print("following request received: tofollow: ", user_to_follow_id, " follower: ", current_user_id)
        user_to_follow = get_object_or_404(UserDetails, id=user_to_follow_id)
        current_user = get_object_or_404(UserDetails, id=current_user_id)
        print("current_user: ", current_user.__str__())
        print("user_to_follow: ", user_to_follow.__str__())
        relationPresent = False
        if current_user != user_to_follow:
            try:
                friendObject = Friends.objects.filter(userFollowed=user_to_follow, userFollower=current_user)
                if friendObject:
                    relationPresent = True
                if not relationPresent:
                    Friends.objects.create(followingSince=datetime.today(), userFollowed=user_to_follow,
                                           userFollower=current_user)
                    action = 'followed'
                else:
                    friendObject.delete()
                    action = 'unfollowed'
            except Exception:
                return JsonResponse({'status': 'error', 'message': 'Unable to proceeed'})
            return JsonResponse({'status': 'success', 'action': action})
        else:
            return JsonResponse({'status': 'error', 'message': 'You cannot follow yourself'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def updatePostLikes(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print("data received: ", data)
        userId = data.get('userId')
        postId = data.get('postId')
        print("update like request, postId: ", postId, " userId: ", userId)
        user = get_object_or_404(UserDetails, id=userId)
        post_to_like = get_object_or_404(Post, id=postId)
        print("current_user: ", user.__str__())
        print("post to like: ", post_to_like.__str__())
        alreadyLike = False
        try:
            checkExistingObject = LikedPosts.objects.filter(user=user, post=post_to_like)
            if checkExistingObject:
                alreadyLike = True
            if not alreadyLike:
                LikedPosts.objects.create(user=user, post=post_to_like)
                post_to_like.totalLikes = post_to_like.totalLikes + 1
                post_to_like.save()
                action = 'liked-success'
                currentLikes = post_to_like.totalLikes
            else:
                print("unliking the post")
                checkExistingObject.delete()
                print("prev likes: ", post_to_like.totalLikes)
                post_to_like.totalLikes = post_to_like.totalLikes - 1
                print("new likes: ", post_to_like.totalLikes)
                currentLikes = post_to_like.totalLikes
                post_to_like.save()
                action = 'unliked-success'
                print("delete: currentLikes: ", currentLikes)
        except Exception:
            return JsonResponse({'status': 'error', 'message': 'Unable to proceeed'})
        print("currentLikes: ", currentLikes)
        return JsonResponse({'status': 'success', 'action': action, 'currentLikes': currentLikes})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def savethepost(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print("data received: ", data)
        userId = data.get('userId')
        postId = data.get('postId')
        print("update like request, postId: ", postId, " userId: ", userId)
        user = get_object_or_404(UserDetails, id=userId)
        post_to_like = get_object_or_404(Post, id=postId)
        print("current_user: ", user.__str__())
        print("post to like: ", post_to_like.__str__())
        alreadySaved = False
        try:
            checkExistingObject = SavedPosts.objects.filter(user=user, post=post_to_like)
            if checkExistingObject:
                alreadySaved = True
            if not alreadySaved:
                SavedPosts.objects.create(user=user, post=post_to_like)
                action = 'saved-success'
            else:
                checkExistingObject.delete()
                action = 'unsaved-success'
        except Exception:
            return JsonResponse({'status': 'error', 'message': 'Unable to proceeed'})
        return JsonResponse({'status': 'success', 'action': action})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def report_post_spam(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print("data received: ", data)
        userId = data.get('userId')
        postId = data.get('postId')
        print("update like request, postId: ", postId, " userId: ", userId)
        user = get_object_or_404(UserDetails, id=userId)
        post_to_spam = get_object_or_404(Post, id=postId)
        print("current_user: ", user.__str__())
        print("post to spam: ", post_to_spam.__str__())
        message=''
        try:
            post_to_spam.isScam = 1
            post_to_spam.spamReported = post_to_spam.spamReported+1
            post_to_spam.save()
            action = 'spam-report-success'
            if post_to_spam.spamReported >= 2:
                message='disable-post'
                action=''
            else:
                message='enable-post'
        except Exception:
            action = 'spam-report-unsuccess'
            return JsonResponse({'status': 'error', 'message': 'Unable to proceeed'})
        return JsonResponse({'status': 'success', 'action': action, 'message': message})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})