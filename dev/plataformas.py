import requests
import json

api_key = '3d6045c2cab54b58836ccd6ec57d9a37'

# URL da API para buscar plataformas
url = f'https://api.rawg.io/api/platforms?key={api_key}'

response = requests.get(url)
if response.status_code == 200:
    plataformas = response.json()
    with open('plataformas.txt', 'w') as arquivo_txt:
        for plataforma in plataformas['results']:
            nome = plataforma['name']
            plataforma_id = plataforma['id']
            arquivo_txt.write(f"{nome}: {plataforma_id}\n")
    print('Plataformas salvas em plataformas.txt')
else:
    print('Erro ao buscar plataformas')
