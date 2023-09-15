from datetime import date, timedelta
import feedparser
from flask import *
from dateutil.relativedelta import relativedelta
import SCRIPTS.sql_fiodameada as SQL
import SCRIPTS.Script_Crawl as Script_Crawl
from SCRIPTS.integracao import Envio, formatacao_html
from threading import Thread

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
        print(request_return)
        for id_noticia in request_return:
            if "Inutilizar" in request_return[id_noticia]:
                SQL.Noticias().update(ID_Noticia=id_noticia, Status="2")
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

        for envio in envios.keys():
            print("atualizando status")
            envio.atualizar_status_noticias()

    print("começando a criar")
    Thread(target=worker, args=(preferencias, formatos)).start()
    return "Success"


@app.route("/confirmar_envios", methods=["POST", "GET"])
def confirmar_envios():
    if request.method == "POST":
        # Auth_SendPulse().publicar_envios()
        pass

    else:
        envios = SQL.Envios().select()
        noticias = [envio[2] for envio in envios]
        noticias = SQL.Noticias().select(categorizacao="IDs", IDs_Noticias=noticias)

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


# @app.route("/formatacao_manual")
# def formatacao_manual():
#     pass


if __name__ == "__main__":
    app.run(debug=True)
