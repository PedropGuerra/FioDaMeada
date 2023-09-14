from flask import *
from sql_fiodameada import (
    Parceiros,
    connect_db,
    dict_to_json,
    Noticias,
    Preferencia_Usuarios,
)
import feedparser
import Script_Crawl
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

app = Flask(__name__)

error = None


def html_tags(link: str) -> str:
    tags_string = """"""
    options_string = """"""

    parse = feedparser.parse(link)
    tags = Parceiros().confirm_tags(parse=parse)

    for i, tag in enumerate(tags):
        tags_string += f"""
        <h1>{tag}</h1>
        <p>: {getattr(parse.entries[0], tag)}</p>"""

        options_string += f"""
        <option value="{tag}">{tag}</option>"""

    html_string = f"""
    {tags_string}
    <br>
    <form method="POST">
        Titulo Noticia <select name="Headline">
            {options_string}
        </select>
        <br>
        Texto_Publicacao <select name="Text">
           {options_string}
        </select>
        <br>
        Resumo_Publicacao <select name="Resumo">
           {options_string}
        </select>
        <input type="submit" value="Enviar">
    </form>
    """

    return html_string


@app.route("/cadastro_parceiro", methods=["POST", "GET"])
def cadastro():
    parceiros = Parceiros()
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
                ID_Parceiro=parceiro_id, Tags_HTML_Raspagem=dict_to_json(dict_tags)
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


@app.route("/hub")
def hub():
    hub_string = f"""
    <a href="{url_for("cadastro")}">Cadastro Parceiro</a> <br>
    <a href="{url_for("script")}">Script Raspagem Notícias (Manual)</a> <br>
    """
    return hub_string


@app.route("/associacao_preferencias", methods=["POST", "GET"])
def associacao_preferencias():
    if request.method == "POST":
        request_return = request.form.to_dict(flat=False)
        print(request_return)
        for id_noticia in request_return:
            if "Inutilizar" in request_return[id_noticia]:
                Noticias().update(ID_Noticia=id_noticia, Status="2")
                continue

            for id_pref in request_return[id_noticia]:
                if id_pref == "":
                    continue

                Noticias().insert_preferencia(
                    ID_Pref_Usuario=id_pref, ID_Noticia=id_noticia
                )
                print(id_noticia, " + ", id_pref)

        return redirect(url_for("associacao_preferencias"))

    else:
        today = date.today()
        data_desde = today + relativedelta(day=1)
        data_ate = today + relativedelta(day=31)
        noticias_string = """<form method="POST">
        <input type="submit" value="Enviar">"""
        options_string = """<option></option>"""

        noticias = [None]
        preferencias = Preferencia_Usuarios().select()

        for i, option in enumerate(preferencias):
            id, option = option
            options_string += f"""
            <option value="{id}">{option}</option>
            """
            if i == len(preferencias) - 1:
                options_string += f"""
                <option value="Inutilizar">Inutilizar</option>
                """

        # print(len(noticias))
        while len(noticias) != 0:
            noticias = Noticias().select(
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
                <select name="{noticia[0]}" multiple>
                <{options_string}
                </select>
                <p>Segure CTRL para selecionar +1</p>
                <p>CUIDADO: Ao selecionar 'Inutilizar' a notícia não será associada</p>
                <br>
                """

            today = date.today() - timedelta(days=30)
            data_desde = today + relativedelta(day=1)
            data_ate = today + relativedelta(day=31)

        noticias_string += """
        </form>
        """

        return noticias_string
    # exibir todas as notícias da separadas por semana
    # exibir todas as preferências
    # campo para associar preferências ao lado de cada uma
    # atualizar todas de uma vez


@app.route("/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        connect_db(user=request.form["user"], password=request.form["password"])

        return redirect(url_for("hub"))

    else:
        return render_template("login.html", error=error)


@app.route("/script")
def script():
    Script_Crawl.FioDaMeada_Script_Crawling()
    return "Success"


if __name__ == "__main__":
    app.run(debug=True)
