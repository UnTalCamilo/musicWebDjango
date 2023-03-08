import requests

# Definir la clave de API y la consulta de búsqueda
api_key = 'https://api.deezer.com/version/service/id/method/?parameters'
query = 'Despacito'

# Realizar una búsqueda de la canción en la API de Deezer
search_url = f'https://api.deezer.com/search?q={query}&limit=1'
response = requests.get(search_url, headers={'Authorization': f'Bearer {api_key}'})
search_results = response.json()

# Obtener la información de la primera canción en los resultados de búsqueda
if 'data' in search_results and len(search_results['data']) > 0:
    song_info = search_results['data'][0]
    print(f"Nombre de la canción: {song_info['title']}")
    print(f"Artista: {song_info['artist']['name']}")
    print(f"URL de vista previa: {song_info['preview']}")
else:
    print("No se encontraron resultados para la búsqueda.")