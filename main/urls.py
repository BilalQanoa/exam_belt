from django.urls import path
from . import views

app_name = 'main' 

urlpatterns = [
    path('', views.home, name='home'),
    path('game/<int:game_id>/', views.game_detail, name='game_detail'),
    path('game/<int:game_id>/edit/', views.edit_game, name='edit_game'),
    path('game/<int:game_id>/delete/', views.delete_game, name='delete_game'),
    path('profile/<int:user_id>/', views.profile_page, name='profile_page'),
]