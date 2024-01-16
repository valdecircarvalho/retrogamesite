import os
import hashlib
import zlib
import re

def calcular_hashes(caminho_arquivo):
    with open(caminho_arquivo, 'rb') as arquivo:
        conteudo = arquivo.read()
        md5 = hashlib.md5(conteudo).hexdigest()
        sha1 = hashlib.sha1(conteudo).hexdigest()
        crc = '%08X' % (zlib.crc32(conteudo) & 0xFFFFFFFF)
        return md5, sha1, crc

def limpar_nome_arquivo(nome_arquivo):
    nome_limpo = re.sub(r"\(.*\)|\[.*\]|\..*$", "", nome_arquivo).strip()
    return nome_limpo

def listar_arquivos(diretorio):
    arquivos_info = []
    if not os.path.exists(diretorio):
        print(f"Erro: Diretório '{diretorio}' não encontrado.")
        return arquivos_info

    for raiz, diretorios, arquivos in os.walk(diretorio):
        if not arquivos:
            print(f"Aviso: Nenhum arquivo encontrado em '{diretorio}'.")
            continue
        arquivos.sort()
        for nome_arquivo in arquivos:
            caminho_completo = os.path.join(raiz, nome_arquivo)
            tamanho = os.path.getsize(caminho_completo)
            md5, sha1, crc = calcular_hashes(caminho_completo)
            nome_jogo = limpar_nome_arquivo(nome_arquivo)
            arquivos_info.append((nome_arquivo, nome_jogo, tamanho, crc, md5, sha1))
    return arquivos_info

diretorio_roms = '/home/ubuntu/projects/retrogamesite/roms_raw/atari2600'
informacoes_arquivos = listar_arquivos(diretorio_roms)

cabecalho = "Nome Completo do Arquivo, Nome do Jogo, Tamanho, CRC, MD5, SHA1\n"

if informacoes_arquivos:
    with open('lista_jogos.txt', 'w') as arquivo_saida:
        arquivo_saida.write(cabecalho)
        for info in informacoes_arquivos:
            linha = f"{info[0]}, {info[1]}, {info[2]}, {info[3]}, {info[4]}, {info[5]}\n"
            arquivo_saida.write(linha)
    print('Dados salvos em lista_jogos.txt')
else:
    print('Nenhum dado foi salvo.')
