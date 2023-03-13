from django import forms
from .models import *

class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['id', 'song_name', 'artist_name', 'uri', 'url_song', 'url_image']

class LikedSongForm(forms.ModelForm):
    class Meta:
        model = LikedSong
        fields = ['user', 'song']

class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ['user', 'playlist_name', 'description']

class PlaylistSongForm(forms.ModelForm):
    class Meta:
        model = PlaylistSong
        fields = ['playlist', 'song']

class HistoryForm(forms.ModelForm):
    class Meta:
        model = History
        fields = ['user', 'song', 'date']

