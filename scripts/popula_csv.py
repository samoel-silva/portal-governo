from copy import deepcopy
from pathlib import Path

import json
import logging
import requests

import csv

# Define como faremos o log das ações
logging.basicConfig()
logger = logging.getLogger("portal.goveno.popula")
logger.setLevel(logging.INFO)


# Constantes utilizadas no script
PASTA_ATUAL = Path(__file__).parent.resolve()
PASTA_DADOS = PASTA_ATUAL / "data"
PASTA_TEMPLATES = PASTA_ATUAL / "templates"
BASE_URL="http://localhost:8080/Plone/++api++"
USUARIO="admin"
SENHA="admin"

# Cabeçalhos HTTP
headers = {
    "Accept": "application/json"
}

session = requests.Session()
session.headers.update(headers)

# Autenticar o usuário admin utilizando um Token JWT
login_url = f"{BASE_URL}/@login"
response = session.post(login_url, json={"login": USUARIO, "password": SENHA})
data = response.json()
token = data["token"]
session.headers.update(
    {"Authorization": f"Bearer {token}"}
)

def popula_templates() -> dict:
    suffix = ".json"
    templates = {}
    arquivos = PASTA_TEMPLATES.glob("*.json")
    for arquivo in arquivos:
        tipo = arquivo.name[:-len(suffix)]
        dados = json.loads(arquivo.read_text())
        templates[tipo] = dados
    return templates


# Popula os templates por tipo de conteúdo
templates = popula_templates()

conteudos = {}

# Criar Conteúdos
with open('secretarias_rio_grande_do_sul_completo.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        path = f"/secretarias/{row['Id']}"
        conteudos[path] = {
            'id': row['Id'],
            '@type': 'Secretaria',
            'title': row['Secretaria'],
            'description': row['Secretaria'],
            'email': row['E-mail']
        }
        path = f"{path}/{row['Responsável Id']}"
        conteudos[path] = {
            'id': row['Responsável Id'],
            '@type': 'Pessoa',
            'title': row['Responsável'],
            'email': row['E-mail']
        }

# Popula os templates por tipo de conteúdo
templates = popula_templates()


# Criar Conteúdos
for path in conteudos:
    data = conteudos[path]
    parent_path = "/".join(path.split("/")[:-1])[1:]
    response = session.get(f"{BASE_URL}/{path}")
    if response.status_code != 404:
        logger.info(f"Ignorando {BASE_URL}{path}: Conteúdo já existe")
        continue
    # Identificamos qual o tipo de conteúdo será criado
    tipo = data["@type"]
    # Criamos uma nova varíavel com a cópia dos dados originais
    payload = deepcopy(templates.get(tipo, {}))
    # Aplicamos os dados recebidos de CONTEUDOS
    payload.update(data)
    response = session.post(f"{BASE_URL}/{parent_path}", json=payload)
    if response.status_code > 300:
        logger.error(f"Erro ao criar '{path}': {response.status_code}")
    else:
        logger.info(f"Conteúdo criado: '{path}'")



