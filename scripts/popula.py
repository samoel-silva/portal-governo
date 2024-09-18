from pathlib import Path
import logging
import requests
from random import choice

# Define como faremos o log das ações
logging.basicConfig()
logger = logging.getLogger("portal.goveno.popula")
logger.setLevel(logging.INFO)


# Constantes utilizadas no script
PASTA_ATUAL = Path(__file__).parent.resolve()
PASTA_DADOS = PASTA_ATUAL / "data"
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




CONTEUDOS = {
    "/cultura": {
        "id": "cultura",
        "@type": "Secretaria",
        "title": "Secretaria de Cultura",
        "description": "Secretaria de Cultura do Estado do Rio Grande do Sul",
        "telefone": "5132885400",
        "email": "gabinete@sedac.rs.gov.br",
    },
    "/cultura/beatriz-araujo": {
        "id": "beatriz-araujo",
        "@type": "Pessoa",
        "title": "Beatriz Araújo",
        "description": "Assumiu a Secretaria Estadual da Cultura em 2019. À frente da Sedac, alterou a legislação de incentivo à cultura, desenvolveu projetos de recuperação patrimonial e fortaleceu a relação com os municípios.",
        "cargo": "secretario",
        "telefone": "5132885400",
        "email": "gabinete@sedac.rs.gov.br",
    },
}

# Criar Conteúdos

for path in CONTEUDOS:
    data = CONTEUDOS[path]
    parent_path = "/".join(path.split("/")[:-1])[1:]
    response = session.get(f"{BASE_URL}/{path}")
    if response.status_code != 404:
        logger.info(f"Ignorando {BASE_URL}{path}: Conteúdo já existe")
        continue
    response = session.post(f"{BASE_URL}/{parent_path}", json=data)
    if response.status_code > 300:
        logger.error(f"Erro ao criar '{path}': {response.status_code}")
    else:
        logger.info(f"Conteúdo criado: '{path}'")
