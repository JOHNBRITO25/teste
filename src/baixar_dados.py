import requests
import re
import os
import zipfile

# URL base onde a ANS publica as Demonstrações Contábeis
BASE_URL = "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/"

# Diretórios locais para armazenar os arquivos baixados e extraídos
RAW_DIR = "data_raw"
EXTRACT_DIR = "data_extracted"

# Garantir que as pastas existam antes de salvar os arquivos baixados e extraídos
os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(EXTRACT_DIR, exist_ok=True)

def listar_anos():
    """
    Acessa a página raiz do repositório da ANS e extrai
    todos os anos disponíveis (ex: 2023, 2024, 2025)
    usando expressão regular.
    """
    html = requests.get(BASE_URL).text
    return re.findall(r'href="(20\d{2})/"', html)

def listar_zips_do_ano(ano):
    """
    Para um ano específico, acessa a pasta correspondente
    e retorna os arquivos ZIP de trimestre (ex: 1T2025.zip).
    """
    html = requests.get(BASE_URL + ano + "/").text
    return re.findall(r'href="(\dT' + ano + r'\.zip)"', html)

# Lista para armazenar os arquivos a serem baixados
# no formato (ano, trimestre, nome_arquivo)
todos = []

# Percorre todos os anos e seus respectivos ZIPs
for ano in listar_anos():
    for zipname in listar_zips_do_ano(ano):

        # O trimestre está no primeiro caractere do nome (ex: 1T2025.zip)
        trimestre = int(zipname[0])
        todos.append((ano, trimestre, zipname))

# Ordena os arquivos do mais recente para o mais antigo
# Primeiro por ano, depois por trimestre
todos.sort(reverse=True)

# Ira baixar apenas os 3 arquivos mais recentes
ultimos = todos[:3]

print("Baixando:")
for ano, trimestre, zipname in ultimos:
    print(zipname)

    # Monta a URL completa
    url = BASE_URL + ano + "/" + zipname

    # Caminho local para salvar o arquivo ZIP
    caminho_zip = os.path.join(RAW_DIR, zipname)

    # Baixa o arquivo ZIP
    r = requests.get(url)
    with open(caminho_zip, "wb") as f:
        f.write(r.content)

    # Extrai o conteúdo do ZIP para a pasta data_extracted
    with zipfile.ZipFile(caminho_zip, "r") as zip_ref:
        zip_ref.extractall(EXTRACT_DIR)

print("Download e extração concluídos.")
