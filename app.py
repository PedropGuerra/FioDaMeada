from flask import *
import SCRIPTS.sql_fiodameada as SQL
from SCRIPTS.integracao import Auth_SendPulse
from threading import Thread
import random
import logging
import psutil



logging.basicConfig(level=logging.INFO)

app = Flask(__name__)


@app.route("/api/noticias", methods=["GET"])
def get_noticias():
    return Response(status=200)
    # logging.info(f"Início Req, CPU(%): {psutil.cpu_percent(4)} / RAM(%): {psutil.virtual_memory()[2]} / RAM(GB): {psutil.virtual_memory()[3]/1000000000}")
    
    # args = request.args.get
    # # login_database(request.args.get("API_KEY"))
    # SQL.connect_db(user = "sendpulse", password=request.args.get("API_KEY"))
    
    # logging.info(f"Connect DB, CPU(%): {psutil.cpu_percent(4)} / RAM(%): {psutil.virtual_memory()[2]} / RAM(GB): {psutil.virtual_memory()[3]/1000000000}")

    # contact_id = args("contact_id")
    # if not contact_id:
    #     return Response("error", status=400)

    # qtd_noticias = int(args("qtd_noticias")) if args("qtd_noticias") else None
    # qtd_fakenews = int(args("qtd_fakenews")) if args("qtd_fakenews") else None
    # qtd_rodadas = int(args("qtd_rodadas")) if args("qtd_rodadas") else None
    # producao = args("producao") if args("producao") else None
    
    # logging.info(f"Args Lidos, CPU(%): {psutil.cpu_percent(4)} / RAM(%): {psutil.virtual_memory()[2]} / RAM(GB): {psutil.virtual_memory()[3]/1000000000}")

    # # API_SendPulse = Auth_SendPulse()
    # # preferencias_id = API_SendPulse.get_preferencias(contact_id)

    # # if not preferencias_id:
    # #     abort(400, "O usuário não possui preferências cadastradas")

    # condicoes_dict = {
    #     "rodadas+noticias+fake": qtd_rodadas and qtd_fakenews and qtd_noticias,
    #     "only_noticias": qtd_noticias and not qtd_fakenews,
    #     "only_fake": qtd_fakenews and not qtd_noticias,
    #     "fake+rodadas": qtd_fakenews and qtd_noticias and not qtd_rodadas,
    # }
    
    # logging.info(f"Condicoes Dict, CPU(%): {psutil.cpu_percent(4)} / RAM(%): {psutil.virtual_memory()[2]} / RAM(GB): {psutil.virtual_memory()[3]/1000000000}")

    # # return condicoes_dict

    

    # def formatacao_dict(noticia):
    #     return {
    #         "id": noticia[0],
    #         "fake": noticia[5],
    #         "headline": noticia[3],
    #         "resumo": noticia[4],
    #         "link": noticia[2],
    #         "parceiro": "Autor",
    #         "fake_local": noticia[6],
    #     }

    # db_noticias = (
    #     list(
    #         map(
    #             formatacao_dict,
    #             SQL.Noticias().select(
    #                 formato="qtd_noticias",
    #                 qtd_noticias=qtd_noticias,
    #                 contact_id=contact_id,
    #                 preferencias_id=[[1],[2],[3]],
    #             ),
    #         )
    #     )
    #     if qtd_noticias
    #     else None
    # )
    

    # db_fakenews = (
    #     list(
    #         map(
    #             formatacao_dict,
    #             SQL.Noticias().select(
    #                 formato="qtd_fakenews",
    #                 qtd_fakenews=qtd_fakenews,
    #                 contact_id=contact_id,
    #                 preferencias_id=[[1],[2],[3]],
    #             ),
    #         )
    #     )
    #     if qtd_fakenews
    #     else None
    # )

    # logging.info(f"Select Noticias + Fake News, CPU(%): {psutil.cpu_percent(4)} / RAM(%): {psutil.virtual_memory()[2]} / RAM(GB): {psutil.virtual_memory()[3]/1000000000}")

    # resp_noticias = {}
    # resp_gabarito = {}
    # response = {"Noticias": resp_noticias, "Gabarito": resp_gabarito}

    # if condicoes_dict["rodadas+noticias+fake"]:
    #     for rodada in range(1, qtd_rodadas + 1):
    #         noticias_por_rodada = min(qtd_noticias // qtd_rodadas, len(db_noticias))
    #         fakenews_por_rodada = min(qtd_fakenews // qtd_rodadas, len(db_fakenews))

    #         rodada_noticias = random.sample(
    #             db_fakenews, fakenews_por_rodada
    #         ) + random.sample(db_noticias, noticias_por_rodada)
    #         random.shuffle(rodada_noticias)

    #         for i, noticia in enumerate(rodada_noticias):
    #             resp_noticias[f"noticia{i + 1}"] = noticia
    #             if noticia["fake"] == 1:
    #                 resp_gabarito[f"rodada{i+1}"] = {
    #                     "id": noticia["id"],
    #                     "local": noticia["fake_local"],
    #                 }

    # elif condicoes_dict["only_noticias"]:
    #     for i, noticia in enumerate(db_noticias):
    #         response["Noticias"][f"noticia{i + 1}"] = noticia

    # elif condicoes_dict["only_fake"]:
    #     for i, fake in enumerate(db_fakenews):
    #         response["Noticias"][f"noticia{i + 1}"] = fake

    # elif condicoes_dict["fake+rodadas"]:

    #     for i, noticia in enumerate(db_noticias + db_fakenews):
    #         match noticia["fake"]:
    #             case 1:
    #                 resp_noticias[f"noticia{i+1}"] = noticia
    #                 resp_gabarito[f"rodada{i + 1}"] = {
    #                     "id": noticia["id"],
    #                     "local": noticia["fake_local"],
    #                 }

    #             case 0:
    #                 resp_noticias[f"noticia{i+1}"] = noticia

    # else:
    #     return Response("error", status=400)

    # if not "0" in producao:
    #     def atualizar_noticias(db_noticias, db_fakenews, contact_id):
    #         ids_noticias = [noticia["id"] for noticia in db_noticias + db_fakenews]
    #         SQL.Noticias().noticias_usuario(contact_id,ids_noticias)

    #     Thread(
    #         target=atualizar_noticias, args=(db_noticias, db_fakenews, contact_id)
    #     ).start()

    # logging.info(f"Response Criado, CPU(%): {psutil.cpu_percent(4)} / RAM(%): {psutil.virtual_memory()[2]} / RAM(GB): {psutil.virtual_memory()[3]/1000000000}")
    
    # return response
    
    