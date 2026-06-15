from django.db import models
from accounts.models import User
from datetime import date, datetime
from django.utils import timezone


# Create your models here.

class GameManager(models.Manager):

    def game_validator(self, postData):
        errors = {}
        
        # Name Validation
        name = postData.get('name', '').strip()
        if len(name) < 2:
            errors['name'] = "Game name must be at least 2 characters long."
        
        # Genre Validation
        genre = postData.get('genre', '').strip()
        if len(genre) < 3:
            errors['genre'] = "Genre must be at least 3 characters long."
        
        # Release Date Validation
        release_date_str = postData.get('release_date', '')
        try:
            release_date = datetime.strptime(release_date_str, '%Y-%m-%d').date()
            if release_date > date.today():
                errors['release_date'] = "Release date cannot be in the future."
        except ValueError:
            errors['release_date'] = "Invalid release date format. Please use YYYY-MM-DD."
        
        # Description Validation
        description = postData.get('description', '').strip()
        if len(description) < 1:
            errors['description'] = "Description cannot be blank."
        
        return errors

class Game (models.Model):
    name = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)
    release_date = models.DateField()
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='games')
    created_at = models.DateTimeField(auto_now_add=True)
    updates_at = models.DateTimeField(auto_now=True)

    objects = GameManager()


    def __str__(self):
        return self.name
    

class UserFavoriteGame (models.Model):
    users = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "player_favorites")
    games = models.ForeignKey(Game, on_delete=models.CASCADE, related_name = "game_ratings")
    rate = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('users', 'games')
        
    
