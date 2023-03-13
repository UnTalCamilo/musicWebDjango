from django.db import models
from django.contrib.auth.models import User


class Song(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    song_name = models.CharField(max_length=50)
    artist_name = models.CharField(max_length=50)
    uri = models.CharField(max_length=100)
    url_song = models.CharField(max_length=100)
    url_image = models.CharField(max_length=100)

class LikedSong(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)

class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    playlist_name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)

class PlaylistSong(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)

class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)