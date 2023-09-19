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


@app.route("/formatacao/", methods=["GET"])
def get_formatacao():
    return_value = {
        "noticias": {},
        "gabarito": {},
    }
    rodadas = {}

    contact_id = request.args.get("contact_id")
    qtd_noticias = int(request.args.get("qtd_noticias"))
    qtd_fakenews = int(request.args.get("qtd_fakenews"))
    qtd_rodadas = int(request.args.get("qtd_rodadas")) if qtd_fakenews else 0

    # API_SendPulse = Auth_SendPulse()
    # preferencias_id: tuple = API_SendPulse.get_preferencias(contact_id)
    preferencias_id = (1, 2, 2)

    noticias = SQL.Noticias().select(
        formato="qtd_noticias",
        qtd_noticias=qtd_noticias,
        contact_id=contact_id,
        preferencias_id=preferencias_id,
    )
    fakenews = SQL.Noticias().select(
        formato="qtd_fakenews",
        qtd_fakenews=qtd_fakenews,
        contact_id=contact_id,
        preferencias_id=preferencias_id,
    )
    # print(f"Noticias : {noticias}")
    # print(f"Fake : {fakenews}")

    if qtd_rodadas:
        # Refazer o sistema de rodadas e gabarito (acho que o tanto de FOR está atrapalhando)
        # Deveriam existir 6 noticias e 3 fake news, porém retornam apenas 3
        # Considerar condições que não existam noticias ou fake news
        # O código precisa estar mais organizado e escalável
        # Apesar das coisas ruins, este é o melhor caminho
        noticias_rodada = qtd_noticias // int(qtd_rodadas)
        fakenews_rodada = qtd_fakenews // int(qtd_rodadas)
        i_utilizado = []

        for rodada in range(qtd_rodadas):
            rodada += 1
            rodadas[f"rodada{rodada}"] = []

        for rodada in rodadas.values():
            diferente = False

            while diferente == False:
                choices_noticia = random.sample(noticias, noticias_rodada)
                choices_fake = random.sample(fakenews, fakenews_rodada)
                intersection = set(choices_noticia) | set(choices_fake)

                if len(intersection & set(i_utilizado)) == 0:
                    diferente = True

            for choice in choices_noticia:
                rodada.append(choice)
                i_utilizado.append(choice)

            for choice in choices_fake:
                rodada.append(choice)
                i_utilizado.append(choice)

        for i, rodada in enumerate(rodadas.values()):
            with open("rodadas.json", "w+") as txt:
                txt.write(SQL.dict_to_json(rodadas))

            # with open("rodada.txt", "w+") as txt:
            #     txt.write(rodada)

            for fake in rodada[fakenews_rodada * -1]:
                return_value["gabarito"] = {f"rodada{i}": fake}  # id_fake

            random.shuffle(rodada)

            for noticia in rodada:
                return_value["noticias"][f"noticia{i}"] = {
                    "id": noticia[0],
                    "fake": noticia[5],
                    "headline": noticia[3],
                    "resumo": noticia[4],
                    "link": noticia[2],
                    "parceiro": SQL.Parceiros().confirm(ID_Parceiro=noticia[1]),
                }

    elif qtd_noticias and not qtd_fakenews:
        for i, noticia in enumerate(noticias):
            return_value["noticias"][f"noticia{1}"] = {
                "id": noticia[0],
                "fake": noticia[5],
                "headline": noticia[3],
                "resumo": noticia[4],
                "link": noticia[2],
                "parceiro": SQL.Parceiros().confirm(ID_Parceiro=noticia[1]),
            }

    elif qtd_fakenews and not qtd_noticias:
        for i, fake in enumerate(fakenews):
            return_value["noticias"][f"noticia{i}"] = {
                "id": noticia[0],
                "fake": fake[5],
                "headline": fake[3],
                "resumo": noticia[4],
                "link": fake[2],
                "parceiro": SQL.Parceiros().confirm(ID_Parceiro=fake[1]),
            }

    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     executor.submit(
    #         SQL.Noticias().noticias_usuario,
    #         contact_id,
    #         list(set(noticias) | set(fakenews)),
    #     )

    return return_value


# código criado pelo ChatGPT
# É PRECISO INTEGRAR BANCO DE DADOS
# FORMAS DE TRANSFORMAR O SELECT DE NOTICIAS EM UM DICT ORGANIZADO
@app.route("/api/noticias", methods=["GET"])
def get_noticias():
    # Obtém os parâmetros da requisição
    contact_id = request.args.get("contact_id")
    qtd_noticias = int(request.args.get("qtd_noticias"))
    qtd_fakenews = int(request.args.get("qtd_fakenews"))
    qtd_rodadas = int(request.args.get("qtd_rodadas"))

    # Aqui, você deve se conectar ao seu banco de dados e buscar as notícias e fake news
    # Substitua isso com sua lógica de consulta ao banco de dados
    noticias = [
        {
            "id": 1,
            "fake": 0,
            "headline": "Notícia 1",
            "resumo": "Resumo da Notícia 1",
            "link": "http://noticia1.com",
            "parceiro": "Parceiro 1",
        },
        {
            "id": 2,
            "fake": 1,
            "headline": "Fake News 1",
            "resumo": "Resumo da Fake News 1",
            "link": "http://fakenews1.com",
            "parceiro": "Parceiro 2",
        },
        # Adicione mais notícias e fake news conforme necessário
    ]

    # Cria o objeto JSON de resposta
    response = {"Noticias": {}}

    # Preenche o objeto JSON de resposta com as notícias e fake news
    for i, noticia in enumerate(noticias[: qtd_noticias + qtd_fakenews]):
        tipo = "noticia"
        response["Noticias"][f"{tipo}{i + 1}"] = {
            "id": noticia["id"],
            "fake": noticia["fake"],
            "headline": noticia["headline"],
            "resumo": noticia["resumo"],
            "link": noticia["link"],
            "parceiro": noticia["parceiro"],
        }

    return jsonify(response)


# @app.route("/formatacao_manual")
# def formatacao_manual():
#     pass


if __name__ == "__main__":
    app.run(debug=True)
