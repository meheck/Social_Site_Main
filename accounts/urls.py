

from django.urls import path,re_path
from accounts.views import SignUp,CreateProfile,DetailProfile,VerifyProfile,FollowToggle,search
from django.contrib.auth import views as auth_views
from django.conf.urls import url

app_name='accounts'

urlpatterns=[
    path('signup/',SignUp.as_view(),name='signup'),
    path('login/',auth_views.LoginView.as_view(template_name='accounts/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('<slug:username>/profile/create', CreateProfile.as_view(), name='createprofile'),
    path('<slug:username>/profile/<int:pk>/', DetailProfile.as_view(), name='profile'),
    path('<slug:username>/profile/',VerifyProfile , name='verifyprofile'),
    url(r'^(?P<slug>[\w-]+)/follow/$', FollowToggle.as_view(), name="follow_toggle"),
    #url(r'^search/', search, name="search"),
    path('search/', search,name='search')

]