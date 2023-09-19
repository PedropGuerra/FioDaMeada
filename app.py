from datetime import date, timedelta
import feedparser
from flask import *
from dateutil.relativedelta import relativedelta
import SCRIPTS.sql_fiodameada as SQL
import SCRIPTS.Script_Crawl as Script_Crawl
from SCRIPTS.integracao import Envio, formatacao_html, Auth_SendPulse
import concurrent.futures
from threading import Thread
import random
import json


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


@app.route("/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        SQL.connect_db(user=request.form["user"], password=request.form["password"])

        return redirect(url_for("hub"))

    else:
        return render_template("login.html", error=error)


@app.route("/hub")
def hub():
    hub_string = f"""
    <a href="{url_for("cadastro")}">Cadastro Parceiro</a> <br>
    <a href="{url_for("script")}">Script Raspagem Notícias (Manual)</a> <br>
    <a href="{url_for("associacao_noticias")}">Associar Preferências às Notícias (Manual)</a> <br>
    <a href="{url_for("criar_envios")}">Criar Novos Envios (Manual)</a> <br>
    """
    return hub_string


@app.route("/cadastro_parceiro", methods=["POST", "GET"])
def cadastro():
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


@app.route("/associacao_noticias", methods=["POST", "GET"])
def associacao_noticias():
    if request.method == "POST":
        request_return = request.form.to_dict(flat=False)
        # print(request_return)
        for id_noticia in request_return:
            if "Inutilizar" in request_return[id_noticia]:
                SQL.Noticias().update(ID_Noticia=id_noticia, Status="1")  # inutilizada
                continue

            for id_pref in request_return[id_noticia]:
                # Valor concatenado com "f" é formato, senão preferência
                if id_pref == "":
                    continue

                elif "f" in id_pref:
                    # Noticias_Formatos().insert(id_noticia, id_pref)
                    formato = id_pref.removesuffix("f")
                    SQL.Noticias().insert_formato(
                        ID_Formato=formato, ID_Noticia=id_noticia
                    )

                else:
                    SQL.Noticias().insert_preferencia(
                        ID_Pref_Usuario=id_pref, ID_Noticia=id_noticia
                    )
                    print(id_noticia, " + ", id_pref)

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
        # formatos = Formatos().select()
        formatos = SQL.Formatos().select(categorizacao="todos")

        for i, option in enumerate(preferencias):
            id_pref, option = option
            options_pref_string += f"""
            <option value="{id_pref}">{option}</option>
            """
            if i == len(preferencias) - 1:
                options_pref_string += """
                <option value="Inutilizar">Inutilizar</option>
                """

        for i, formato in enumerate(formatos):
            id_format, formato = formato
            options_format_string += f"""
            <option value="{id_format}f">{formato}</option>
            """

        # print(len(noticias))
        while len(noticias) != 0:
            noticias = SQL.Noticias().select(
                categorizacao="associacao",
                data_desde=str(data_desde),
                data_ate=str(data_ate),
            )
            if len(noticias) == 0:
                continue

            noticias_string += f"""
            <h1>De {data_desde} até {data_ate}</h1>"""

            for i, noticia in enumerate(noticias):
                noticias_string += f"""
                <h3>{noticia[3][:150]}</h3>
                <p>{noticia[4][:400]}</p>
                <a href="{noticia[2]}">Link Noticia</a> <br>
                Preferências<select name="{noticia[0]}" multiple>
                <{options_pref_string}
                </select>
                Formatos<select name="{noticia[0]}">
                <{options_format_string}
                </select>
                <br>
                """

            today = date.today() - timedelta(days=30)
            data_desde = today + relativedelta(day=1)
            data_ate = today + relativedelta(day=31)

        noticias_string += """
        </form>
        """

        return noticias_string


@app.route("/script")
def script():
    Script_Crawl.FioDaMeada_Script_Crawling()
    return "Success"


@app.route("/criar_envios")
def criar_envios():
    # criar envios em um loop por preferencia
    # é preciso criar todos os formatos da semana por cada preferencia
    # importar todos os formatos e preferencias e fazer um for loop

    formatos = SQL.Formatos().select(categorizacao="todos")
    print(formatos)
    preferencias = SQL.Preferencia_Usuarios().select()
    print(preferencias)

    def worker(preferencias, formatos):
        print("começando o worker")
        envios = {}
        for pref in preferencias:
            for formato in formatos:
                envio = Envio(formato=formato, preferencia_usuarios=pref)
                envio.criar()
                envios[envio.id_envio] = envio
                print(f"envio {envio.id_envio}\n pref:{pref}\nformat:{formato}")

        # for envio in envios.keys():
        #     print("atualizando status")
        #     envio.atualizar_status_noticias()

    print("começando a criar")
    # Thread(target=worker, args=(preferencias, formatos)).start()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.submit(worker, preferencias, formatos)
    return "Success"


@app.route("/confirmar_envios", methods=["POST", "GET"])
def confirmar_envios():
    if request.method == "POST":
        # Auth_SendPulse().publicar_envios()
        # request_return = request.form.to_dict(flat=False)
        pass

    else:
        envios = SQL.Envios().select()
        noticias = [envio[2] for envio in envios]
        noticias = SQL.Noticias().select(formato="IDs", IDs_Noticias=noticias)

        envios_string = """<form method="post">
        <input type="submit" value="Enviar">"""

        for envio in envios:
            formato = SQL.Formatos().select(categorizacao="id", ID_Formato=envio[3])
            envios_string += f"""
            {formatacao_html(noticias=noticias, html_format= formato)}
            <select name="{envio[0]}">
                <option value="Aprovado"></option>
                <option value="Repovado"></option>
            </select>
            <br>
            """
        return envios_string


# @app.route("/enviar_mensagens/<dia_semana>")
# def enviar_mensagens(dia_semana):
#     envios_confirmados = SQL.Envios().select(
#         categorizacao="confirmados/dia", dia_semana=dia_semana
#     )
#     # API_SendPulse = Auth_SendPulse().auth()
#     # bots = API_SendPulse.get_bots()

#     # Divide a quantidade de envios por 3
#     # Atribui os as quantidades para os 3 threads
#     # Caso sobre alguma requisição, é atribuida ao 4 thread
#     tamanho_thread = len(envios_confirmados) // 3
#     grupo_req1 = envios_confirmados[0:tamanho_thread]
#     grupo_req2 = envios_confirmados[tamanho_thread : tamanho_thread * 2]
#     grupo_req3 = envios_confirmados[tamanho_thread * 2 : tamanho_thread * 3]

#     if len(envios_confirmados) - tamanho_thread * 3 != 0:
#         de = tamanho_thread * 3
#         ate = de + len(envios_confirmados) - tamanho_thread * 3
#         grupo_req4 = envios_confirmados[de:ate]

#     def enviar_req(requisicoes):
#         for req in requisicoes:


# puxar todas os envios confirmados com o dia da semana correspondente (ok)
# puxar a autenticacao da SendPulse (ok)
# puxar todos os bots -> contatos (ok)
# confirmar todas as requisições
# dividir as requisições para utilizar em diferentes workerss
# utilizar alguns workers para enviar mais ao mesmo tempo


@app.route("/api/noticias", methods=["GET"])
def get_noticias():
    # Obtém os parâmetros da requisição
    args = request.args.get

    contact_id = args("contact_id")
    if not contact_id:
        return Response("error", status=400)

    qtd_noticias = int(args("qtd_noticias")) if args("qtd_noticias") else None
    qtd_fakenews = int(args("qtd_fakenews")) if args("qtd_fakenews") else None
    qtd_rodadas = int(args("qtd_rodadas")) if args("qtd_rodadas") else None
    producao = args("producao") if args("producao") else None

    API_SendPulse = Auth_SendPulse()
    preferencias_id = API_SendPulse.get_preferencias(contact_id)

    condicoes_dict = {
        "rodadas+noticias+fake": qtd_rodadas and qtd_fakenews and qtd_noticias,
        "only_noticias": qtd_noticias and not qtd_fakenews,
        "only_fake": qtd_fakenews and not qtd_noticias,
        "fake+rodadas": qtd_fakenews and qtd_noticias and not qtd_rodadas,
    }

    def formatacao_dict(noticia):
        return {
            "id": noticia[0],
            "fake": noticia[5],
            "headline": noticia[3],
            "resumo": noticia[4],
            "link": noticia[2],
            "parceiro": SQL.Parceiros().confirm(ID_Parceiro=noticia[1]),
        }

    db_noticias = list(
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

    db_fakenews = list(
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
    resp_noticias = {}
    resp_gabarito = {}
    response = {"Noticias": resp_noticias, "Gabarito": resp_gabarito}

    if condicoes_dict["rodadas+noticias+fake"]:
        for rodada in range(1, qtd_rodadas + 1):
            noticias_por_rodada = min(qtd_noticias // qtd_rodadas, len(db_noticias))
            fakenews_por_rodada = min(qtd_fakenews // qtd_rodadas, len(db_fakenews))
            print(f"noticias_por_rodada : {noticias_por_rodada}")
            print(f"fakenews_por_rodada : {fakenews_por_rodada}")

            rodada_noticias = random.sample(
                db_fakenews, fakenews_por_rodada
            ) + random.sample(db_noticias, noticias_por_rodada)
            random.shuffle(rodada_noticias)
            print(f"rodada_noticias : {rodada_noticias}")

            for i, noticia in enumerate(rodada_noticias):
                resp_noticias[f"noticia{i + 1}"] = noticia
                if noticia["fake"] == 1:
                    resp_gabarito[f"rodada{i+1}"] = noticia["id"]

    elif condicoes_dict["only_noticias"]:
        for i, noticia in enumerate(noticias):
            response["Noticias"][f"noticia{i + 1}"] = noticia

    elif condicoes_dict["only_fake"]:
        for i, fake in enumerate(fakenews):
            response["Noticias"][f"noticia{i + 1}"] = fake

    elif condicoes_dict["fake+rodadas"]:
        # juncao_noticias_fakenews = {}
        # juncao_noticias_fakenews.update(db_noticias)
        # juncao_noticias_fakenews.update(db_fakenews)

        for i, noticia in enumerate(db_noticias + db_fakenews):
            match noticia["fake"]:
                case 1:
                    resp_noticias[f"fakenews{i+1}"] = noticia
                    resp_gabarito[i + 1] = noticia["id"]

                case 0:
                    resp_noticias[f"noticia{i+1}"] = noticia

    else:
        return Response("error", status=400)

    if producao:

        def atualizar_noticias(db_noticias, db_fakenews, contact_id):
            ids_noticias = [noticia["id"] for noticia in db_noticias + db_fakenews]
            SQL.Noticias().noticias_usuario(contact_id, ids_noticias)

        Thread(
            target=atualizar_noticias, args=(db_noticias, db_fakenews, contact_id)
        ).start()

    return response


# @app.route("/formatacao_manual")
# def formatacao_manual():
#     pass


if __name__ == "__main__":
    SQL.connect_db()
    app.run(debug=True)
