from django.contrib import messages
from django.shortcuts import render, redirect

from accounts.models import User
from main.models import Game, UserFavoriteGame

# Create your views here.

def home(request):
    if 'user_id' not in request.session:
        return redirect('accounts:index')
    sort_by = request.GET.get('sort', '-created_at')
    games = Game.objects.all().order_by(sort_by)

    if request.method == 'POST':
        errors = Game.objects.game_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return render(request, 'main/home.html', {'games': games})
        
        current_user = User.objects.get(id=request.session['user_id'])
        Game.objects.create(
            name = request.POST['name'],
            genre = request.POST['genre'],
            release_date = request.POST['release_date'],
            description = request.POST['description'],
            created_by = current_user
        )
        return redirect('main:home')
    return render(request, 'main/home.html', {'games': games})



def game_detail(request, game_id):
    if 'user_id' not in request.session:
        return redirect('accounts:index')
    
    game = Game.objects.get(id=game_id)
    ratings = game.game_ratings.all()
    is_favorite = UserFavoriteGame.objects.filter(users_id=request.session['user_id'], games_id=game_id).exists()

    if request.method == 'POST':
        current_user = User.objects.get(id=request.session['user_id'])
        rate = int(request.POST.get('rate', 5))

        UserFavoriteGame.objects.update_or_create(
            users=current_user,
            games=game,
            defaults={'rate': rate}
        )

        return redirect('main:game_detail', game_id=game_id)
    
    context = {
        'game': game,
        'ratings': ratings,
        'is_favorite': is_favorite
    }
    return render(request, 'main/game_detail.html', context)

    

def edit_game(request, game_id):
    if 'user_id' not in request.session:
        return redirect('accounts:index')
    
    game = Game.objects.get(id=game_id)

    if game.created_by.id != request.session['user_id']:
        messages.error(request, "You are not authorized to edit this game.")
        return redirect('main:game_detail', game_id=game.id)

    if request.method == 'POST':
        errors = Game.objects.game_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return render(request, 'main/edit_game.html', {'game': game})
        
        game.name = request.POST['name']
        game.genre = request.POST['genre']
        game.release_date = request.POST['release_date']
        game.description = request.POST['description']
        game.save()
        return redirect('main:game_detail', game_id=game.id)
    
    return render(request, 'main/edit_game.html', {'game': game})

def delete_game(request, game_id):
    if 'user_id' not in request.session:
        return redirect('accounts:index')
    
    game = Game.objects.get(id=game_id)

    if game.created_by.id == request.session['user_id']:
        game.delete()
        return redirect('main:home')
    
    return render(request, 'main/game_detail.html', {'game': game})


def profile_page(request, user_id):
    if 'user_id' not in request.session:
        return redirect('accounts:index')
    
    user = User.objects.get(id=user_id)
    favorite_games = user.player_favorites.all()
    games = user.games.all()

    context = {
        'user': user,
        'favorite_games': favorite_games,
        'games': games
    }
    return render(request, 'main/profile_page.html', context)