from django.urls import path
from . import views

app_name='accounts'

urlpatterns=[
    path('',views.feed,name='feed'),
    path('register/',views.register,name='register'),
    path('login/',views.user_login,name='login'),
    path('logout/',views.user_logout,name='logout'),
    path('profile/<int:user_id>/',views.profile_user,name='profile'),
    path('profile/edit/',views.edit_profile,name='edit_profile'),
    path('profile/<int:user_id>/followers/',views.followers_list,name='followers_list'),
    path('profile/<int:user_id>/following/',views.following_list,name='following_list'),
    path('search/',views.user_search,name='user_search'),

]
