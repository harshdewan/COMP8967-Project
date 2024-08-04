from django.urls import path
from .views import *

urlpatterns = [
    path('home/<int:user_id>/', home,name='home'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('signup/', signup, name='signup'),
    path('explore/', explore, name='explore'),
    path('following/<int:user_id>/', following, name='following'),
    path('search/<int:user_id>/', searchView, name='search'),
    path('notifications/<int:user_id>/', notificationView, name='mynotifications'),
    path('savedposts/<int:user_id>/', savedpostsView, name='mysavedposts'),
    path('messages/', messagesView, name='mymessages'),
    path('profile/<int:user_id>/', profileView, name='profile'),
    path('myposts/<int:user_id>/', myPostsViews,name='myposts'),
    path('myfollowers/<int:user_id>/', myFollowersView, name='followers'),
    path('changepassword/<int:user_id>', changePasswordView, name='changePassword'),
    path('communities/<int:user_id>/', communitiesView, name='communities'),
    path('editprofile<int:user_id>/', editProfileView, name='editprofile'),
    path('userpost/<int:user_id>/', userpost, name='userpost'),
    path('follow/', updateFollowing, name='follow_user'),
    path('updatepostlikes', updatePostLikes, name="update-post-like"),
    path('savepost/', savethepost,name="savepost"),
    path('reportpostspam/', report_post_spam, name='report-post-spam'),
]