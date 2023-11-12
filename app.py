from flask import Flask
from flaskApi.apiGetNoticias import apiGetNoticias
from flaskApi.apiPostMensagens import apiPostMensagens
from flaskApi.apiPostScript import apiPostScript
from flaskAdmin.adminParceirosHtmlTags import adminParceirosHtmlTags
from flaskAdmin.adminAssociacaoNoticias import (
    adminAssociacaoNoticias,
    adminAssociacaoNoticias_Render,
)
from flaskAdmin.adminCadastroParceiros import (
    adminCadastroParceiros,
    adminCadastroParceiros_tags,
)


app = Flask(__name__)

# API ENDPOINTS
app.add_url_rule("/api/noticias", view_func=apiGetNoticias, methods=["GET"])
app.add_url_rule("/api/mensagens/enviar", view_func=apiPostMensagens)
app.add_url_rule("/api/script", view_func=apiPostScript)


# ADMIN ENDPOINTS
app.add_url_rule("/admin/html-parceiros", view_func=adminParceirosHtmlTags)

app.add_url_rule("/admin/associar-noticias", view_func=adminAssociacaoNoticias)
app.add_url_rule(
    "/admin/associar-noticias/render",
    view_func=adminAssociacaoNoticias_Render,
    methods=["POST"],
)

app.add_url_rule(
    "/admin/cadastro-parceiros",
    view_func=adminCadastroParceiros,
    methods=["POST", "GET"],
)
app.add_url_rule(
    "/admin/cadastro-parceiros/tags",
    view_func=adminCadastroParceiros_tags,
    methods=["POST", "GET"],
)

if __name__ == "__main__":
    app.run(debug=True)
