from flask import *
from sql_fiodameada import Parceiros, connect_db, disconnect_db, dict_to_json
import feedparser

app = Flask(__name__)


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


@app.route("/cadastro", methods=["POST", "GET"])
def cadastro():
    error = None
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


@app.route("/", methods=["POST", "GET"])
def login():
    error = None
    if request.method == "POST":
        connect_db(user=request.form["user"], password=request.form["password"])

        return redirect(url_for("cadastro"))

    else:
        return render_template("login.html", error=error)


if __name__ == "__main__":
    app.run(debug=False)
