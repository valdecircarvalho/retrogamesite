import requests
import os
import mysql.connector

# Dados de conexão ao banco de dados
host = "localhost"
user = "root"
password = "root_mysql_retrogamesite"
dbname = "teste_db"

# Conectar ao banco de dados
db = mysql.connector.connect(host=host, user=user, password=password, database=dbname)
cursor = db.cursor()

# Ler a chave da API do arquivo
with open('api_rawg.txt', 'r') as arquivo:
    api_key = arquivo.read().strip()

platform_id = '23'  # Substitua pelo ID real da Atari 2600

# Assegurar que o diretório de imagens existe
os.makedirs('imgs', exist_ok=True)

# Ler os nomes dos jogos do arquivo
with open('lista_jogos.txt', 'r') as arquivo:
    linhas = arquivo.readlines()
    nomes_jogos = [linha.split(',')[1].strip() for linha in linhas[1:]]

# Fazer as requisições à API e salvar os dados
for nome_jogo in nomes_jogos:
    url_busca = f'https://api.rawg.io/api/games?key={api_key}&search={nome_jogo}&platforms={platform_id}'
    response_busca = requests.get(url_busca)
    if response_busca.status_code == 200 and response_busca.json()['results']:
        jogo_id = response_busca.json()['results'][0]['id']
        url_detalhes = f'https://api.rawg.io/api/games/{jogo_id}?key={api_key}'
        response_detalhes = requests.get(url_detalhes)
        if response_detalhes.status_code == 200:
            detalhes_jogo = response_detalhes.json()
            gameNome = detalhes_jogo.get('name', 'N/A')
            gameDescricao = detalhes_jogo.get('description_raw', 'N/A')
            gameLancamento = detalhes_jogo.get('released', 'N/A')
            gameGenero = ', '.join([g['name'] for g in detalhes_jogo.get('genres', [])])
            gameDesenvolvedores = ', '.join([d['name'] for d in detalhes_jogo.get('developers', [])])
            
            # Fazer requisição para obter screenshots
            url_screenshots = f'https://api.rawg.io/api/games/{jogo_id}/screenshots?key={api_key}'
            response_screenshots = requests.get(url_screenshots)
            if response_screenshots.status_code == 200:
                screenshots = response_screenshots.json()['results']
                if screenshots:
                    gameScreenshot1 = screenshots[0]['image']
                else:
                    gameScreenshot1 = 'N/A'
            
            # Inserir dados no banco de dados
            query = """INSERT INTO games (gameNome, gameDescricao, gameLancamento, gameGenero, gameDesenvolvedores, gameScreenshot1)
                       VALUES (%s, %s, %s, %s, %s, %s)"""
            valores = (gameNome, gameDescricao, gameLancamento, gameGenero, gameDesenvolvedores, gameScreenshot1)
            cursor.execute(query, valores)
            db.commit()

# Fechar conexão com o banco de dados
cursor.close()
db.close()
