from django.shortcuts import redirect, render
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.db.models import Q

from configparser import ConfigParser
from django.conf import settings

from django.http import JsonResponse

# Models
from .models import Song, LikedSong, Playlist, PlaylistSong, History

# spotify api
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

config = ConfigParser()
config.read(settings.CONFIG_FILE)

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=config.get('SPOTIFY', 'CLIENT_ID'),
                                                                             client_secret=config.get('SPOTIFY', 'CLIENT_SECRET')))

# Create your views here.
def index(request):
    top_artists = spotify.search(q='year:2023', type='artist', limit=10)
    top_music = spotify.search(q='year:2023', type='track', limit=10)
       
    return render(request, 'musicApp/index.html', {'top_artists': top_artists,
                                                   'top_music': top_music})


def search(request):
    pass

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
            messages.info(request, 'Invalid credentials')
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
                return render(request, 'musicApp/index.html')
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
    print("name: ", name)
    info_artist = spotify.search(q='artist:' + name, type='artist', limit=1)
    artist_id = info_artist['artists']['items'][0]['id']
    music_artist = spotify.artist_top_tracks(artist_id)
    for music in music_artist['tracks']:
        print(type(music))
        print(music['name'], end="\n\n")
        break
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
        
        liked_song = LikedSong(user=request.user, song=song)
        liked_song.save()
        return JsonResponse({'status': 'ok'})

    except Exception as e:
        print("Exception: ", e)
        return JsonResponse({'status': 'error'})
