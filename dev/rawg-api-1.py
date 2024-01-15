import requests
import json

api_key = '3d6045c2cab54b58836ccd6ec57d9a37'
url = f'https://api.rawg.io/api/platforms?key={api_key}'

response = requests.get(url)
if response.status_code != 200:
    print('Erro na requisição da API')
    exit()

data = response.json()

# Salvar os dados em um arquivo
with open('lista_plataformas.json', 'w') as file:
    json.dump(data, file, indent=4)

print('Dados salvos em games_data.txt')
