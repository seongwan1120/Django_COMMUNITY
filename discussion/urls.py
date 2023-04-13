from django.urls import path
from . import views

app_name = 'discussion'

urlpatterns = [
    path('create/', views.posting_create, name='posting_create'),
    path('', views.posting_index, name='posting_index'),
    path('feed/', views.posting_feed, name='posting_feed'),
    path('<int:posting_pk>/', views.posting_detail, name='posting_detail'),
    path('<int:posting_pk>/update/', views.posting_update, name='posting_update'),
    path('<int:posting_pk>/delete/', views.posting_delete, name='posting_delete'),
    path('<int:posting_pk>/posting_best/', views.posting_best, name='posting_best'),
    path('<int:posting_pk>/posting_worst/', views.posting_worst, name='posting_worst'),
    path('<int:posting_pk>/comment/create/', views.comment_create, name='comment_create'),
    path('<int:posting_pk>/comment/<int:comment_pk>/update/', views.comment_update, name='comment_update'),
    path('<int:posting_pk>/comment/<int:comment_pk>/delete/', views.comment_delete, name='comment_delete'),
    path('<int:posting_pk>/comment/<int:comment_pk>/comment_agree', views.comment_agree, name='comment_agree'),
    path('<int:posting_pk>/comment/<int:comment_pk>/comment_disagree', views.comment_disagree, name='comment_disagree'),
    path('<int:posting_pk>/comment/<int:comment_pk>/reply/create/', views.reply_create, name='reply_create'),
    path('<int:posting_pk>/comment/<int:comment_pk>/reply/<int:reply_pk>/update/', views.reply_update, name='reply_update'),
    path('<int:posting_pk>/comment/<int:comment_pk>/reply/<int:reply_pk>/delete/', views.reply_delete, name='reply_delete'),

]
