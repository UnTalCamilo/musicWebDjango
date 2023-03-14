from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('artist/<str:name>/', views.artist, name='artist'),
    path('liked/', views.liked, name='liked'),
    path('disliked/', views.disliked, name='disliked'),
    path('liked_songs/', views.liked_songs, name='liked_songs'),
    path('addhistory/', views.addHistory, name='addhistory'),
    path('history/', views.history, name='history'),

]