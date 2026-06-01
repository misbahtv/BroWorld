from django.urls import path
from . import views

app_name='posts'

urlpatterns=[
    path('create/',views.create_post,name='create_post'),
    path('<int:post_id>/',views.detail_post,name='detail_post'),
    path('<int:post_id>/like/',views.toggle_like,name='toggle_like'),
    path('<int:user_id>/follow/',views.toggle_follow,name='toggle_follow'),
    path('remove-following/<int:user_id>/',views.remove_following,name='remove_following'),
    path('remove-follower/<int:user_id>/',views.remove_follower,name='remove_follower'),

]