import requests

HOST = "https://intense-elysium-398121.rj.r.appspot.com"
# HOST = "http://127.0.0.1:5000"

# TEST = ["status_code", "response"]
TEST = ["status_code"]


def test_noticias_AFN():
    endpoint = "/api/noticias"
    param_AFN = {
        "contact_id": "6500e99d564ffa8cf10d994f",
        "API_KEY": "JOiurVpPh2UNeCGFWaPe",
        "qtd_fakenews": "3",
        "qtd_noticias": "6",
        "qtd_rodadas": "3",
        "producao": "0",
    }

    r = requests.get(HOST + endpoint, params=param_AFN)

    response: dict = r.json()

    if "status_code" in TEST:
        assert r.status_code == 200

    if "response" in TEST:
        assert len(response["Noticias"]) == param_AFN["qtd_noticias"]
        assert len(response["Gabarito"]) == param_AFN["qtd_rodadas"]


def test_noticias_NS():
    endpoint = "/api/noticias"
    param_NS = {
        "contact_id": "6500e99d564ffa8cf10d994f",
        "API_KEY": "JOiurVpPh2UNeCGFWaPe",
        "qtd_noticias": "10",
        "qtd_rodadas": "0",
        "producao": "0",
    }

    r = requests.get(HOST + endpoint, params=param_NS)
    response: dict = r.json()

    if "status_code" in TEST:
        assert r.status_code == 200

    if "response" in TEST:
        assert len(response["Noticias"]) == param_NS["qtd_noticias"]
        assert len(response["Gabarito"]) == param_NS["qtd_rodadas"]


def test_noticias_OEF():
    endpoint = "/api/noticias"
    param_OEF = {
        "contact_id": "6500e99d564ffa8cf10d994f",
        "API_KEY": "JOiurVpPh2UNeCGFWaPe",
        "qtd_fakenews": "3",
        "qtd_rodadas": "3",
        "producao": "0",
    }

    r = requests.get(HOST + endpoint, params=param_OEF)
    response: dict = r.json()

    if "status_code" in TEST:
        assert r.status_code == 200

    if "response" in TEST:
        assert len(response["Noticias"]) == param_OEF["qtd_noticias"]
        assert len(response["Gabarito"]) == param_OEF["qtd_rodadas"]


def test_script():
    endpoint = "/api/script"
    param_script = {"API_KEY": "JOiurVpPh2UNeCGFWaPe"}

    r = requests.get(HOST + endpoint, params=param_script)

    if "status_code" in TEST:
        assert r.status_code == 200


def test_mensagens_enviar():
    endpoint = "/api/mensagens/enviar"
    param_enviar_msg = {"API_KEY": "JOiurVpPh2UNeCGFWaPe"}

    r = requests.get(HOST + endpoint, params=param_enviar_msg)

    if "status_code" in TEST:
        assert r.status_code == 200
