from django.urls import path
from . import views

urlpatterns = [
    path('', views.BoardListView.as_view(), name='home'),
    path('board/<int:id>/', views.board_topics, name='board'),
    path('board/<int:id>/new/', views.new_topic, name='new-topic'),
    path('board/<int:id>/topic/<int:topic_id>/', views.topic_posts, name = 'topic_posts'),
    path('board/<int:id>/topic/<int:topic_id>/reply/', views.reply_topic, name = 'reply_topic'),
    path('board/<int:id>/topic/<int:topic_id>/posts/<int:post_id>/edit/', views.PostUpdateView.as_view(), name = 'edit_post'),

]