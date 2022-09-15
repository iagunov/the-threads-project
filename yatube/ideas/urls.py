from django.urls import path

from . import views


app_name = 'ideas'

urlpatterns = [
    path('idea/<int:idea_id>/edit/', views.idea_edit, name='idea_edit'),
    path(
            'idea/<int:idea_id>/opinion/',
            views.add_opinion,
            name='add_opinion'
        ),
    path('idea/<int:idea_id>/team/<int:user_id>/<int:team_id>/accept/', views.accept_member, name='accept'),
    path('idea/<int:idea_id>/team/<int:user_id>/<int:team_id>/decline/', views.decline_member, name='decline'),
    path('idea/<int:idea_id>/team/<int:user_id>/<int:team_id>/delete/', views.delete_member, name='delete'),
    path('idea/<int:idea_id>/team/participate/', views.participate, name='participate'),
    path('idea/<int:idea_id>/team/leave/', views.leave, name='leave'),
    path('idea/<int:idea_id>/team/', views.team_profile, name='team_profile'),
    path('idea/<int:idea_id>/', views.idea_detail, name='idea_detail'),
    path('create/', views.idea_create, name='idea_create'),
    path('', views.index, name='index'),
]


# urlpatterns = [
#     path('create/', views.post_create, name='post_create'),
#     path('group/<slug:slug>/', views.group_posts, name='group_list'),
#     path('posts/<int:post_id>/edit/', views.post_edit, name='post_edit'),
#     path(
#         'posts/<int:post_id>/comment/',
#         views.add_comment,
#         name='add_comment'
#     ),
#     path('profile/<str:username>/', views.profile, name='profile'),
#     path('follow/', views.follow_index, name='follow_index'),
#     path(
#         'profile/<str:username>/follow/',
#         views.profile_follow,
#         name='profile_follow'
#     ),
#     path(
#         'profile/<str:username>/unfollow/',
#         views.profile_unfollow,
#         name='profile_unfollow'
#     ),
#     path(
#         'profile/<str:username>/follow/',
#         views.profile_follow,
#         name='profile_follow'
#     ),
#     path('', views.index, name='index'),
# ]
