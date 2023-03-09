from django.shortcuts import redirect, render
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.db.models import Q

from configparser import ConfigParser
from django.conf import settings


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
    print(type(top_artists))  # imprime el tipo de dato de top_artists
    # imprime el nombre de los artistas
    for artist in top_artists['artists']['items']:
        print(artist, end="\n\n")
    
    return render(request, 'musicApp/index.html', {'top_artists': top_artists})


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