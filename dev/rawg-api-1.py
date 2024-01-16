import requests
import os

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
            with open(f"{nome_jogo.replace(' ', '_')}.txt", 'w') as arquivo_txt:
                arquivo_txt.write(f"Nome: {detalhes_jogo.get('name', 'N/A')}\n")
                arquivo_txt.write(f"Descrição: {detalhes_jogo.get('description_raw', 'N/A')}\n")
                arquivo_txt.write(f"Lançamento: {detalhes_jogo.get('released', 'N/A')}\n")
                arquivo_txt.write("Gêneros: " + ', '.join([g['name'] for g in detalhes_jogo.get('genres', [])]) + "\n")
                arquivo_txt.write("Desenvolvedores: " + ', '.join([d['name'] for d in detalhes_jogo.get('developers', [])]) + "\n")
                
                # Fazer requisição para obter screenshots
                url_screenshots = f'https://api.rawg.io/api/games/{jogo_id}/screenshots?key={api_key}'
                response_screenshots = requests.get(url_screenshots)
                if response_screenshots.status_code == 200:
                    screenshots = response_screenshots.json()['results']
                    for screenshot in screenshots:
                        img_url = screenshot['image']
                        img_nome = f"imgs/{nome_jogo.replace(' ', '_')}_{screenshot['id']}.jpg"
                        img_data = requests.get(img_url).content
                        with open(img_nome, 'wb') as img_file:
                            img_file.write(img_data)
                        # Salvar nome da imagem e caminho no arquivo .txt
                        arquivo_txt.write(f"Screenshot: {img_nome}\n")
