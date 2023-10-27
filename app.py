from datetime import date, timedelta
import feedparser
from flask import (
    Flask,
    Response,
    request,
    make_response,
    redirect,
    render_template,
    url_for,
)
from dateutil.relativedelta import relativedelta
import services.sql_fiodameada as SQL
from services.integracao import Auth_SendPulse
import services.Script_Crawl as Script_Crawl
from threading import Thread
import random
import services.secrets as os
from time import strftime
import logging
import threading
from tools.timeManipulate import FORMAT_DATA
import json

logging.basicConfig(level=logging.DEBUG)


app = Flask(__name__)


error = None


def html_tags(link: str) -> str:
    tags_string = """"""
    options_pref_string = """"""

    parse = feedparser.parse(link)
    tags = SQL.Parceiros().confirm_tags(parse=parse)

    for tag in tags:
        tags_string += f"""
        <h1>{tag}</h1>
        <p>: {getattr(parse.entries[0], tag)}</p>"""

        options_pref_string += f"""
        <option value="{tag}">{tag}</option>"""

    html_string = f"""
    {tags_string}
    <br>
    <form method="POST">
        Titulo Noticia <select name="Headline">
            {options_pref_string}
        </select>
        <br>
        Texto_Publicacao <select name="Text">
           {options_pref_string}
        </select>
        <br>
        Resumo_Publicacao <select name="Resumo">
           {options_pref_string}
        </select>
        <input type="submit" value="Enviar">
    </form>
    """

    return html_string


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()

    return len(defaults) >= len(arguments)


def site_map_route():
    routes = []

    for rule in app.url_map.iter_rules():
        # Exclude rules that require parameters and rules you can't open in a browser
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            routes.append((url, rule.endpoint))

    return routes


@app.route("/admin")
def red_login():
    return redirect(url_for("login"))


@app.route("/admin/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        SQL.connect_db(user=request.form["user"], password=request.form["password"])

        resp = make_response(redirect(url_for("hub")))
        resp.set_cookie("login", request.form["user"])
        resp.set_cookie("password", request.form["password"])
        resp.set_cookie("db_login", "1")

        return resp

    else:
        return render_template("login.html", error=error)


def login_database():
    if request.cookies.get("db_login"):
        pass

    else:
        try:
            cookies_user = request.cookies.get("user")
            cookies_pswd = request.cookies.get("password")
            SQL.connect_db(user=cookies_user, password=cookies_pswd)

        except:
            return redirect(url_for("login"))


@app.route("/admin/hub")
def hub():
    routes = site_map_route()
    hub_string = f""""""

    for route in routes:
        if "login" in route[0] or "hub" in route[0]:
            continue
        route = route[1]
        hub_string += f"""
        <a href="{url_for(f"{route}")}">{route}</a> <br>
        """
    return hub_string


@app.route("/admin/cadastro_parceiro", methods=["POST", "GET"])
def cadastro():
    login_database()
    parceiros = SQL.Parceiros()
    if request.method == "POST":
        if "Headline" in request.form:
            dict_tags = {
                "Headline": request.form["Headline"],
                "Text": request.form["Text"],
                "Resumo": request.form["Resumo"],
            }

            parceiro_nome = request.cookies.get("Nome_Parceiro")

            parceiro_id = parceiros.confirm(Nome_Parceiro=parceiro_nome)[0][0]

            parceiros.update(
                ID_Parceiro=parceiro_id, Tags_HTML_Raspagem=json.dumps(dict_tags)
            )

            redirect(url_for("cadastro"))

        else:
            parceiro_nome = request.form["Nome_Parceiro"]
            parceiro_link = request.form["Link_Parceiro"]

            parceiros.insert(
                Nome_Parceiro=parceiro_nome,
                Link_Parceiro=parceiro_link,
                ID_Metodo_Coleta=request.form["ID_Metodo_Coleta"],
                Nome_Responsavel=request.form["Nome_Responsavel"],
                Contato_Responsavel=request.form["Contato_Responsavel"],
                Licenca_Distrib=request.form["Licenca_Distrib"],
            )

            resp = make_response(html_tags(parceiro_link))
            resp.set_cookie("Nome_Parceiro", parceiro_nome)
            return resp

    return render_template("cadastro.html", error=error)


def coletarNoticiasDisponiveis():
    dictNoticias = {}
    today = date.today()
    desde = today + relativedelta(day=1)
    ate = today + relativedelta(day=31)

    noticias = SQL.Noticias().select(
        formato="associacao", data_desde=str(desde), data_ate=str(ate)
    )

    while noticias:
        if len(noticias) == 0:
            continue
        """
        {1: {ID : ID, Link:Link, Headline:Headline, Resumo:Resumo, data_desde:desde, data_ate:ate},
        2: {ID : ID, Link:Link, Headline:Headline, Resumo:Resumo, data_desde:desde, data_ate:ate}}
        """
        if isinstance(noticias, list) and len(noticias[0]) == 4:
            noticias = list(
                map(
                    lambda noticia: {
                        "ID": noticia[0],
                        "Link": noticia[1],
                        "Headline": noticia[2][:150],
                        "Resumo": noticia[3][:400],
                        "data_desde": str(desde),
                        "data_ate": str(ate),
                    },
                    noticias,
                )
            )

            for noticia in noticias:
                proxIndex = len(dictNoticias) + 1
                dictNoticias[proxIndex] = noticia

        else:
            logging.info(noticias)

        today -= timedelta(days=30)
        desde = today + relativedelta(day=1)
        ate = today + relativedelta(day=31)

        noticias = SQL.Noticias().select(
            formato="associacao", data_desde=str(desde), data_ate=str(ate)
        )

    return dictNoticias


@app.route("/admin/associacao_noticias/render", methods=["POST"])
def associacao_noticias_render():
    data = request.form.to_dict(flat=False)
    for idNoticia in data:
        if "Inutilizar" in data[idNoticia]:
            SQL.Noticias().update(ID_Noticia=idNoticia, Status="1")
            continue

        for idPref in data[idNoticia]:
            if idPref == "":
                continue

            else:
                SQL.Noticias().insert_preferencia(
                    ID_Pref_Usuario=idPref, ID_Noticia=idNoticia
                )

    return redirect(url_for("associacao_noticias"))


@app.route("/admin/associacao_noticias")
def associacao_noticias():
    login_database()

    preferencias = SQL.Preferencia_Usuarios().select()
    noticias = coletarNoticiasDisponiveis()
    logging.info(preferencias)
    logging.info(noticias)

    return render_template(
        "associacaoNoticias.html", noticias=noticias, preferencias=preferencias
    )


@app.route("/api/script")
def script():
    if request.args.get("API_KEY") != os.getenv("SP_CONNECT_KEY"):
        return Response("Não Autorizado", status=400)

    SQL.connect_db(os.getenv("DB_SP_LOGIN"), os.getenv("SP_CONNECT_KEY"))
    Script_Crawl.FioDaMeada_Script_Crawling()
    return Response(status=200)


@app.route("/api/mensagens/enviar")
def enviar_mensagens():
    from tools.timeManipulate import weekday_sun_first

    if request.args.get("API_KEY") != os.getenv("SP_CONNECT_KEY"):
        return Response("Não Autorizado", status=400)

    SQL.connect_db(os.getenv("DB_SP_LOGIN"), os.getenv("SP_CONNECT_KEY"))

    API_SendPulse = Auth_SendPulse()
    contatos = API_SendPulse.get_contatos()
    logging.info(contatos)

    dia_semana = weekday_sun_first(date.today())

    flow = SQL.SendPulse_Flows().select(categorizacao="dia", Dia_Semana=dia_semana)

    if len(flow) == 0:
        logging.info("SemEnviosHoje")
        logging.info(flow)
        return Response("SemEnviosHoje", status=200)

    tamanho_thread = len(contatos) // 3
    grupos = {
        1: contatos[0:tamanho_thread],
        2: contatos[tamanho_thread : tamanho_thread * 2],
        3: contatos[tamanho_thread * 2 : tamanho_thread * 3],
    }
    logging.info(grupos)

    if len(contatos) - tamanho_thread * 3 != 0:
        de = tamanho_thread * 3
        ate = de + len(contatos) - tamanho_thread * 3
        grupos[4] = contatos[de:ate]

    for grupo in grupos.values():
        Thread(target=API_SendPulse.run_flows, args=(flow, grupo)).start()
        logging.info(f"Iniciando thread grupo {grupo} para self.run_flows")

    SQL.Envios().insert(
        Dia_Semana=dia_semana,
        Data_Envio=strftime(FORMAT_DATA),
        ID_Flow_API=flow[0][0],
    )

    logging.info(
        f"Insert DB Envios: Dia_Semana={dia_semana}, Data_Envio={strftime(FORMAT_DATA)}, ID_Flow_API={flow[0][0]}"
    )

    return Response("Success", status=200)


def responseGetNoticias(
    resp_noticias={},
    resp_gabarito={},
    qtd_noticias=False,
    qtd_fakenews=False,
    qtd_rodadas=False,
    db_noticias: dict = None,
    db_fakenews: dict = None,
):
    condicoesGetNoticias = {
        "rodadas+noticias+fake": qtd_rodadas and qtd_fakenews and qtd_noticias,
        "only_noticias": qtd_noticias and not qtd_fakenews,
        "only_fake": qtd_fakenews and not qtd_noticias,
        "fake+rodadas": qtd_fakenews and qtd_noticias and not qtd_rodadas,
    }

    resp_noticias = {}
    resp_gabarito = {}
    if condicoesGetNoticias["rodadas+noticias+fake"]:
        for _ in range(1, qtd_rodadas + 1):
            noticias_por_rodada = min(qtd_noticias // qtd_rodadas, len(db_noticias))
            fakenews_por_rodada = min(qtd_fakenews // qtd_rodadas, len(db_fakenews))

            rodada_noticias = random.sample(
                db_fakenews, fakenews_por_rodada
            ) + random.sample(db_noticias, noticias_por_rodada)
            random.shuffle(rodada_noticias)

            for i, noticia in enumerate(rodada_noticias):
                resp_noticias[f"noticia{i + 1}"] = noticia
                if noticia["fake"] == 1 or noticia["fake"] == "1":
                    resp_gabarito[f"rodada{i+1}"] = {
                        "id": noticia["id"],
                        "local": noticia["fake_local"],
                    }

    elif condicoesGetNoticias["only_noticias"]:
        for i, noticia in enumerate(db_noticias):
            resp_noticias[f"noticia{i + 1}"] = noticia

    elif condicoesGetNoticias["only_fake"]:
        for i, fake in enumerate(db_fakenews):
            resp_noticias[f"noticia{i + 1}"] = fake

    elif condicoesGetNoticias["fake+rodadas"]:
        for i, noticia in enumerate(db_noticias + db_fakenews):
            match noticia["fake"]:
                case 1:
                    resp_noticias[f"noticia{i+1}"] = noticia
                    resp_gabarito[f"rodada{i + 1}"] = {
                        "id": noticia["id"],
                        "local": noticia["fake_local"],
                    }

                case 0:
                    resp_noticias[f"noticia{i+1}"] = noticia

    else:
        return Response("error", status=400)

    return {"Noticias": resp_noticias, "Gabarito": resp_gabarito}


def formatacaoDbNoticias(select: dict):
    noticias = SQL.Noticias().select(**select)
    noticias = list(
        map(
            lambda noticia: {
                "id": noticia[0],
                "fake": noticia[5],
                "headline": noticia[3],
                "resumo": noticia[4],
                "link": noticia[2],
                "parceiro": SQL.Parceiros().confirm(ID_Parceiro=noticia[1]),
                "fake_local": noticia[6],
            },
            noticias,
        )
    )
    return noticias


def atualizar_noticias(db_noticias, db_fakenews, contact_id):
    if db_fakenews is None:
        db_fakenews = []
    if db_noticias is None:
        db_noticias = []

    if db_fakenews or db_noticias:
        ids_noticias = [noticia["id"] for noticia in db_noticias + db_fakenews]
        SQL.Noticias().noticias_usuario(contact_id, ids_noticias)


@app.route("/api/noticias", methods=["GET"])
def get_noticias():
    args = request.args.get
    if args("API_KEY") != os.getenv("SP_CONNECT_KEY"):
        return Response("Não Autorizado", status=400)

    SQL.connect_db(os.getenv("DB_SP_LOGIN"), os.getenv("SP_CONNECT_KEY"))

    if not args("contact_id"):
        return Response("error", status=400)

    qtd_noticias = int(args("qtd_noticias")) if args("qtd_noticias") else None
    qtd_fakenews = int(args("qtd_fakenews")) if args("qtd_fakenews") else None
    qtd_rodadas = int(args("qtd_rodadas")) if args("qtd_rodadas") else None
    producao = args("producao") if args("producao") else None
    contact_id = args("contact_id")

    API_SendPulse = Auth_SendPulse()
    preferencias_id = API_SendPulse.get_preferencias(contact_id)

    db_noticias = (
        formatacaoDbNoticias(
            {
                "formato": "qtd_noticias",
                "qtd_noticias": qtd_noticias,
                "contact_id": contact_id,
                "preferencias_id": preferencias_id,
            }
        )
        if qtd_noticias
        else None
    )

    db_fakenews = (
        formatacaoDbNoticias(
            {
                "formato": "qtd_fakenews",
                "qtd_fakenews": qtd_fakenews,
                "contact_id": contact_id,
                "preferencias_id": preferencias_id,
            }
        )
        if qtd_fakenews
        else None
    )

    if not "0" in producao:
        threading.Thread(
            target=atualizar_noticias, args=(db_noticias, db_fakenews, contact_id)
        ).start()

    return responseGetNoticias(
        qtd_noticias=qtd_noticias,
        qtd_fakenews=qtd_fakenews,
        qtd_rodadas=qtd_rodadas,
        db_noticias=db_noticias,
        db_fakenews=db_fakenews,
    )
