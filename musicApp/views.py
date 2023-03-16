from django.shortcuts import redirect, render
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.db.models import Q

from configparser import ConfigParser
from django.conf import settings

from django.http import JsonResponse

# Models
from .models import Song, LikedSong, History

# spotify api
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

config = ConfigParser()
config.read(settings.CONFIG_FILE)

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=config.get('SPOTIFY', 'CLIENT_ID'),
                                                                             client_secret=config.get('SPOTIFY', 'CLIENT_SECRET')))

# Create your views here.
def index(request):
    top_artists = spotify.search(q='year:2023', type='artist', limit=20)
    top_music = spotify.search(q='year:2023', type='track', limit=20)
       
    return render(request, 'musicApp/index.html', {'top_artists': top_artists,
                                                   'top_music': top_music})


def search(request):
    if request.method == 'POST':
        search = request.POST['data']
        if search == '':
            return redirect('/')
        
        info_artist = spotify.search(q='artist:' + search, type='artist', limit=20)
        info_music = spotify.search(q='track:' + search, type='track', limit=20)

        return render(request, 'musicApp/options/search.html', {'info_artist': info_artist['artists']['items'],
                                                                'info_music': info_music['tracks']['items']})

def history(request):
    try:
        user = request.user
        history = Song.objects.filter(history__user=user).order_by('-history__date')
        return render(request, 'musicApp/options/history.html', {'history': history})
    except Exception as e:
        print("Exception: ", e)
        return redirect('/')

def login(request):
    if request.method == 'POST':
        username = request.POST['uname']
        password = request.POST['pwd']
        user = auth.authenticate(username=username, password=password)
        print("user: ", user)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('/')
    else:
        return redirect('/')

def signup(request):
    try:
        fname = request.POST.get("fname","default")
        lname = request.POST.get("lname","default")
        username = request.POST.get("username","default")
        email = request.POST.get("email","default")
        password = request.POST.get("pwd","default")
        cpassword = request.POST.get("cpwd","default")
        if password == cpassword:
            users = User.objects.filter(Q(username=username) | Q(email=email))
            if len(users) > 0:
                print("Username or Email already exists")
                messages.info(request, 'Username or Email already exists')
                return redirect('/')
            else:
                user = User.objects.create_user(username=username, password=password, email=email, first_name=fname, last_name=lname)
                user.save()
                user = auth.authenticate(username=username, password=password)
                auth.login(request, user)
                return redirect('/')
        else:
            messages.info(request, 'Password not matching')
            return redirect('/')
    except Exception as e:
        print("Exception: ", e)
        return redirect('/')
    
def logout(request):
    try:
        auth.logout(request)
        return redirect('/')
    except Exception as e:
        print("Exception: ", e)
        return redirect('/')
    

def artist(request, name):
    info_artist = spotify.search(q='artist:' + name, type='artist', limit=1)
    artist_id = info_artist['artists']['items'][0]['id']
    music_artist = spotify.artist_top_tracks(artist_id)

    return render(request, 'musicApp/options/artist.html', {'info_artist': info_artist['artists']['items'][0],
                                                            'music_artist': music_artist['tracks']})

def liked(request):
    try:
        id_song = request.POST.get('id')
        name_song = request.POST.get('name')
        artist_song = request.POST.get('artist')
        uri = request.POST.get('uri')
        url_song = request.POST.get('song')
        url_image = request.POST.get('image')

        tmp_song = Song.objects.filter(id=id_song)
        if len(tmp_song) == 0:
            song = Song(id=id_song, song_name=name_song, artist_name=artist_song, uri=uri, url_song=url_song, url_image=url_image)
            song.save()
        else:
            song = tmp_song[0]
        
        tmp_liked_song = LikedSong.objects.filter(user=request.user, song=song)
        if len(tmp_liked_song) > 0:
            return JsonResponse({'status': 'ok'})
        
        liked_song = LikedSong(user=request.user, song=song)
        liked_song.save()
        return JsonResponse({'status': 'ok'})

    except Exception as e:
        print("Exception: ", e)
        return JsonResponse({'status': 'error'})


def disliked(request):
    try:
        id_song = request.POST.get('id')

        song = Song.objects.filter(id=id_song)
        if len(song) == 0:
            return JsonResponse({'status': 'ok'})
        
        liked_song = LikedSong.objects.filter(user=request.user, song=song[0])
        if len(liked_song) == 0:
            return JsonResponse({'status': 'ok'})
        
        liked_song.delete()
        return JsonResponse({'status': 'ok'})
    except Exception as e:
        print("Exception: ", e)
        return JsonResponse({'status': 'error'})
    
def liked_songs(request):
    try:
        songs = Song.objects.filter(likedsong__user=request.user)
        return render(request, 'musicApp/options/likedSongs.html', {'liked_songs': songs})
    except Exception as e:
        print("Exception: ", e)
        return redirect('/')
    

def addHistory(request):
    try:
        id_song = request.POST.get('id')
        tmp_song = Song.objects.filter(id=id_song)
        if len(tmp_song) == 0:
            track = spotify.track(id_song)
            name_song = track['name']
            artist_song = track['artists'][0]['name']
            uri = track['uri']
            url_song = track['href']
            url_image = track['album']['images'][0]['url']

            song = Song(id=id_song, song_name=name_song, artist_name=artist_song, uri=uri, url_song=url_song, url_image=url_image)
            song.save()
        else:
            song = tmp_song[0]
        
        tmp_history = History.objects.filter(user=request.user, song=song)
        if len(tmp_history) > 0:
            return JsonResponse({'status': 'ok'})
        
        history = History(user=request.user, song=song)
        history.save()
        return JsonResponse({'status': 'ok'})

    except Exception as e:
        print("Exception: ", e)
        return JsonResponse({'status': 'error'})