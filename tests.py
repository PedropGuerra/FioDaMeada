import requests


# REQUESTS TO API CONFIG
# REQ_HOST = "https://intense-elysium-398121.rj.r.appspot.com"
REQ_TEST = ["status_code"]
REQ_HOST = "http://127.0.0.1:5000"
# REQ_TEST = ["status_code", "response"]


# TOOLS FUNCTIONS CONFIG


# SERVICES FUNCTIONS CONFIG
SERV_CHATGPT = False


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

    r = requests.get(REQ_HOST + endpoint, params=param_AFN)

    if "status_code" in REQ_TEST:
        assert r.status_code == 200

    if r.status_code == 200:
        response: dict = r.json()

    if "response" in REQ_TEST:
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

    r = requests.get(REQ_HOST + endpoint, params=param_NS)
    response: dict = r.json()

    if "status_code" in REQ_TEST:
        assert r.status_code == 200

    if "response" in REQ_TEST:
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

    r = requests.get(REQ_HOST + endpoint, params=param_OEF)
    response: dict = r.json()

    if "status_code" in REQ_TEST:
        assert r.status_code == 200

    if "response" in REQ_TEST:
        assert len(response["Noticias"]) == param_OEF["qtd_noticias"]
        assert len(response["Gabarito"]) == param_OEF["qtd_rodadas"]


def test_script():
    endpoint = "/api/script"
    param_script = {"API_KEY": "JOiurVpPh2UNeCGFWaPe"}

    r = requests.get(REQ_HOST + endpoint, params=param_script)

    if "status_code" in REQ_TEST:
        assert r.status_code == 200


def test_mensagens_enviar():
    endpoint = "/api/mensagens/enviar"
    param_enviar_msg = {"API_KEY": "JOiurVpPh2UNeCGFWaPe"}

    r = requests.get(REQ_HOST + endpoint, params=param_enviar_msg)

    if "status_code" in REQ_TEST:
        assert r.status_code == 200


from services.chatgpt import escolherFakeNews, criar_fakenews


def test_chatgpt_EscolherFakeNews():
    escolhas = [0, 0]
    tentativas = 100
    for _ in range(tentativas):
        escolha = escolherFakeNews(headline="teste", text="teste", test=True)
        if escolha[3] == 1:
            escolhas[1] += 1
        if escolha[3] == 0:
            escolhas[0] += 1

    assert escolhas[1] / tentativas >= 0.25 and escolhas[1] / tentativas <= 0.45


def test_chatgpt_CriarFakeNews():
    if SERV_CHATGPT:
        headline = "Essa mensagem é um teste"
        texto = "Essa mensagem é um teste"
        local = "Introducao"

        f_headline, f_texto = criar_fakenews(headline, texto, local)

        assert headline != f_headline
        assert texto != f_texto
