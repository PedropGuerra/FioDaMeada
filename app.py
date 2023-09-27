from datetime import date, timedelta
import feedparser
from flask import *
from dateutil.relativedelta import relativedelta
import SCRIPTS.sql_fiodameada as SQL
from SCRIPTS.integracao import Auth_SendPulse
import SCRIPTS.Script_Crawl as Script_Crawl
from threading import Thread
import random
import SCRIPTS.secrets as os
import time
import logging

logging.basicConfig(level=logging.INFO, filename="logs.log", format="%(asctime)s - %(levelname)s - %(funcName)s - %(message)s")


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


def login_database(API_KEY=None):
    if request.cookies.get("db_login"):
        pass

    elif API_KEY:
        SQL.connect_db(user=os.getenv("DB_SP_LOGIN"), password=API_KEY)

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
                ID_Parceiro=parceiro_id, Tags_HTML_Raspagem=SQL.dict_to_json(dict_tags)
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


@app.route("/admin/associacao_noticias", methods=["POST", "GET"])
def associacao_noticias():
    login_database()
    if request.method == "POST":
        request_return = request.form.to_dict(flat=False)
        for id_noticia in request_return:
            if "Inutilizar" in request_return[id_noticia]:
                SQL.Noticias().update(ID_Noticia=id_noticia, Status="1")  # inutilizada
                continue

            for id_pref in request_return[id_noticia]:
                if id_pref == "":
                    continue

                else:
                    SQL.Noticias().insert_preferencia(
                        ID_Pref_Usuario=id_pref, ID_Noticia=id_noticia
                    )

        return redirect(url_for("associacao_noticias"))

    else:
        today = date.today()
        data_desde = today + relativedelta(day=1)
        data_ate = today + relativedelta(day=31)

        noticias_string = """<form method="POST">
        <input type="submit" value="Enviar">"""
        options_pref_string = """<option></option>"""
        options_format_string = """<option></option>"""

        noticias = [None]
        preferencias = SQL.Preferencia_Usuarios().select()

        for i, option in enumerate(preferencias):
            id_pref, option = option
            options_pref_string += f"""
            <option value="{id_pref}">{option}</option>
            """
            if i == len(preferencias) - 1:
                options_pref_string += """
                <option value="Inutilizar">Inutilizar</option>
                """

        while len(noticias) != 0:
            noticias = SQL.Noticias().select(
                formato="associacao",
                data_desde=str(data_desde),
                data_ate=str(data_ate),
            )
            if len(noticias) == 0:
                continue

            noticias_string += f"""
            <h1>De {data_desde} até {data_ate}</h1>"""

            for i, noticia in enumerate(noticias):
                noticias_string += f"""
                <h3>{noticia[2][:150]}</h3>
                <p>{noticia[3][:400]}</p>
                <a href="{noticia[1]}">Link Noticia</a> <br>
                Preferências<select name="{noticia[0]}" multiple>
                <{options_pref_string}
                </select>
                """

            today = date.today() - timedelta(days=30)
            data_desde = today + relativedelta(day=1)
            data_ate = today + relativedelta(day=31)

        noticias_string += """
        </form>
        """

        return noticias_string


@app.route("/api/script")
def script():
    login_database(request.args.get("API_KEY"))
    Script_Crawl.FioDaMeada_Script_Crawling()
    return Response(status=200)


@app.route("/api/mensagens/enviar/<dia_semana>")
def enviar_mensagens(dia_semana):
    try:
        login_database(request.args.get("API_KEY"))
        API_SendPulse = Auth_SendPulse()
        contatos = API_SendPulse.get_contatos()

        if dia_semana == "today":
            dia_semana = date.today().weekday() + 1

        flow = SQL.SendPulse_Flows().select(categorizacao="dia", Dia_Semana=dia_semana)

        if len(flow) == 0:
            return Response("SemEnviosHoje", status=200)

        tamanho_thread = len(contatos) // 3
        grupos = {
            1: contatos[0:tamanho_thread],
            2: contatos[tamanho_thread : tamanho_thread * 2],
            3: contatos[tamanho_thread * 2 : tamanho_thread * 3],
        }

        if len(contatos) - tamanho_thread * 3 != 0:
            de = tamanho_thread * 3
            ate = de + len(contatos) - tamanho_thread * 3
            grupos[4] = contatos[de:ate]

        for grupo in grupos.values():
            Thread(target=API_SendPulse.run_flows, args=(flow, grupo)).start()

        SQL.Envios().insert(
            Dia_Semana=dia_semana,
            Data_Envio=time.strftime(SQL.FORMAT_DATA),
            ID_Flow_API=flow,
        )

        return Response("Success", status=200)

    except:
        return Response("Error", status=400)


@app.route("/api/noticias", methods=["GET"])
def get_noticias():
    args = request.args.get
    login_database(request.args.get("API_KEY"))

    contact_id = args("contact_id")
    if not contact_id:
        return Response("error", status=400)

    qtd_noticias = int(args("qtd_noticias")) if args("qtd_noticias") else None
    qtd_fakenews = int(args("qtd_fakenews")) if args("qtd_fakenews") else None
    qtd_rodadas = int(args("qtd_rodadas")) if args("qtd_rodadas") else None
    producao = args("producao") if args("producao") else None
    
    logging.info(f"Contact ID: {contact_id}")
    logging.info(f"Qtd_Noticias: {qtd_noticias}")
    logging.info(f"Qtd_FakeNews: {qtd_fakenews}")
    logging.info(f"Qtd_Rodadas: {qtd_rodadas}")
    logging.info(f"Produção: {producao}")

    API_SendPulse = Auth_SendPulse()
    preferencias_id = API_SendPulse.get_preferencias(contact_id)

    if not preferencias_id:
        abort(400, "O usuário não possui preferências cadastradas")

    condicoes_dict = {
        "rodadas+noticias+fake": qtd_rodadas and qtd_fakenews and qtd_noticias,
        "only_noticias": qtd_noticias and not qtd_fakenews,
        "only_fake": qtd_fakenews and not qtd_noticias,
        "fake+rodadas": qtd_fakenews and qtd_noticias and not qtd_rodadas,
    }
    
    map(lambda condicao: logging.info(f"{condicao}: {condicoes_dict[condicao]}"), condicoes_dict)

    def formatacao_dict(noticia):
        return {
            "id": noticia[0],
            "fake": noticia[5],
            "headline": noticia[3],
            "resumo": noticia[4],
            "link": noticia[2],
            "parceiro": SQL.Parceiros().confirm(ID_Parceiro=noticia[1]),
            "fake_local": noticia[6],
        }

    db_noticias = (
        list(
            map(
                formatacao_dict,
                SQL.Noticias().select(
                    formato="qtd_noticias",
                    qtd_noticias=qtd_noticias,
                    contact_id=contact_id,
                    preferencias_id=preferencias_id,
                ),
            )
        )
        if qtd_noticias
        else None
    )

    db_fakenews = (
        list(
            map(
                formatacao_dict,
                SQL.Noticias().select(
                    formato="qtd_fakenews",
                    qtd_fakenews=qtd_fakenews,
                    contact_id=contact_id,
                    preferencias_id=preferencias_id,
                ),
            )
        )
        if qtd_fakenews
        else None
    )

    resp_noticias = {}
    resp_gabarito = {}
    response = {"Noticias": resp_noticias, "Gabarito": resp_gabarito}

    if condicoes_dict["rodadas+noticias+fake"]:
        for rodada in range(1, qtd_rodadas + 1):
            noticias_por_rodada = min(qtd_noticias // qtd_rodadas, len(db_noticias))
            fakenews_por_rodada = min(qtd_fakenews // qtd_rodadas, len(db_fakenews))

            rodada_noticias = random.sample(
                db_fakenews, fakenews_por_rodada
            ) + random.sample(db_noticias, noticias_por_rodada)
            random.shuffle(rodada_noticias)

            for i, noticia in enumerate(rodada_noticias):
                resp_noticias[f"noticia{i + 1}"] = noticia
                if noticia["fake"] == 1:
                    resp_gabarito[f"rodada{i+1}"] = {
                        "id": noticia["id"],
                        "local": noticia["fake_local"],
                    }

    elif condicoes_dict["only_noticias"]:
        for i, noticia in enumerate(db_noticias):
            response["Noticias"][f"noticia{i + 1}"] = noticia

    elif condicoes_dict["only_fake"]:
        for i, fake in enumerate(db_fakenews):
            response["Noticias"][f"noticia{i + 1}"] = fake

    elif condicoes_dict["fake+rodadas"]:

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

    if not "0" in producao:
        def atualizar_noticias(db_noticias, db_fakenews, contact_id):
            ids_noticias = [noticia["id"] for noticia in db_noticias + db_fakenews]
            SQL.Noticias().noticias_usuario(contact_id,ids_noticias)

        Thread(
            target=atualizar_noticias, args=(db_noticias, db_fakenews, contact_id)
        ).start()

    logging.info(response)
    return response
