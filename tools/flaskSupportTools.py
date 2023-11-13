from services.sql.Noticias import Noticias
from services.sql.Parceiros import Parceiros
from services.sql.SendPulse_Flows import SendPulse_Flows

import services.secrets as os
from flask import Response, abort
from services.SendPulse import SendPulse
import logging

logging.basicConfig(level=logging.DEBUG)


def apiKeyValidate(apiKey):
    authenticated = apiKey == os.getenv("SP_CONNECT_KEY")
    if not authenticated:
        abort(400, Response("Não Autorizado"))


def apiArgsTransform(argsPassed, argsConfig, argsRequired):
    argsPassed = argsPassed.to_dict(flat=True)

    for required in argsRequired:
        if not required in argsPassed:
            abort(400, Response(f"Error: {required} inexistente"))

    argsTransformed = {}

    for htmlArgument, argType in argsConfig.items():
        if not htmlArgument in argsPassed:
            argsTransformed[htmlArgument] = None
            continue

        argsTransformed[htmlArgument] = argType(argsPassed[htmlArgument])

    return argsTransformed


def contactPreferences(contact_id):
    prefsDefault = [(1, "Política"), (2, "Saúde"), (3, "Entretenimento")]
    try:
        prefs = SendPulse().getPreferencias(contact_id)
        return prefs

    except Exception as e:
        logging.error(e)
        return prefsDefault


def apiFormatNoticias(noticias: list):  # POR ALGUM MOTIVO, ELE ESTÁ DIVINDO UMA STRING
    for index, noticia in enumerate(noticias.copy()):
        if not isinstance(noticia, tuple):
            logging.info(f"{noticia} foi retirado")
            noticias.pop(index)

    noticias = list(
        map(
            lambda noticia: {
                "id": noticia[0],
                "fake": noticia[5],
                "headline": noticia[3],
                "resumo": noticia[4],
                "link": noticia[2],
                "parceiro": Parceiros().confirm(ID_Parceiro=noticia[1]),
                "fake_local": noticia[6],
            },
            noticias,
        )
    )
    return noticias


def dbSelectNoticias(select: dict):
    noticias = Noticias().select(**select)

    if "qtd_fakenews" in select:
        if len(noticias) < select["qtd_fakenews"]:
            select["valoresUnicos"] = False
            noticias = Noticias().select(**select)

    elif "qtd_noticias" in select:
        if len(noticias) != select["qtd_noticias"]:
            select["valoresUnicos"] = False
            noticias = Noticias().select(**select)

    return noticias


def dbAtualizarNoticiasContatos(contact_id, dbNoticias, dbFakeNews):
    try:
        if dbFakeNews is None:
            dbFakeNews = []

        if dbNoticias is None:
            dbNoticias = []

        if dbFakeNews or dbNoticias:
            ids_noticias = [noticia["id"] for noticia in dbNoticias + dbFakeNews]

            Noticias().noticias_usuario(contact_id, ids_noticias)

    except Exception as e:
        logging.error(e)
        pass


# def apiResponseNoticias(
#     qtd_noticias=False,
#     qtd_fakenews=False,
#     qtd_rodadas=False,
#     db_noticias: dict = None,
#     db_fakenews: dict = None,
# ):
#     import random

#     resp_gabarito = {}
#     resp_noticias = {}

#     condicoesGetNoticias = {
#         "rodadas+noticias+fake": qtd_rodadas and qtd_fakenews and qtd_noticias,
#         "only_noticias": qtd_noticias and not qtd_fakenews,
#         "only_fake": qtd_fakenews and not qtd_noticias,
#         "fake+rodadas": qtd_fakenews and qtd_noticias and not qtd_rodadas,
#     }

#     resp_noticias = {}
#     resp_gabarito = {}
#     if condicoesGetNoticias["rodadas+noticias+fake"]:
#         for _ in range(1, qtd_rodadas + 1):
#             noticias_por_rodada = min(qtd_noticias // qtd_rodadas, len(db_noticias))
#             fakenews_por_rodada = min(qtd_fakenews // qtd_rodadas, len(db_fakenews))

#             rodada_noticias = random.sample(
#                 db_fakenews, fakenews_por_rodada
#             ) + random.sample(db_noticias, noticias_por_rodada)
#             random.shuffle(rodada_noticias)

#             for i, noticia in enumerate(rodada_noticias):
#                 resp_noticias[f"noticia{i + 1}"] = noticia
#                 if noticia["fake"] == 1 or noticia["fake"] == "1":
#                     resp_gabarito[f"rodada{i+1}"] = {
#                         "id": noticia["id"],
#                         "local": noticia["fake_local"],
#                     }

#     elif condicoesGetNoticias["only_noticias"]:
#         for i, noticia in enumerate(db_noticias):
#             resp_noticias[f"noticia{i + 1}"] = noticia

#     elif condicoesGetNoticias["only_fake"]:
#         for i, fake in enumerate(db_fakenews):
#             resp_noticias[f"noticia{i + 1}"] = fake

#     elif condicoesGetNoticias["fake+rodadas"]:
#         for i, noticia in enumerate(db_noticias + db_fakenews):
#             match noticia["fake"]:
#                 case 1:
#                     resp_noticias[f"noticia{i+1}"] = noticia
#                     resp_gabarito[f"rodada{i + 1}"] = {
#                         "id": noticia["id"],
#                         "local": noticia["fake_local"],
#                     }

#                 case 0:
#                     resp_noticias[f"noticia{i+1}"] = noticia

#     else:
#         return Response("error", status=400)

#     return {"Noticias": resp_noticias, "Gabarito": resp_gabarito}


def apiResponseNoticias(
    qtd_rodadas=1,
    db_noticias: dict = None,
    db_fakenews: dict = None,
):
    def roundsCreate(roundsQtd, news: dict = None, fakenews: dict = None):
        import random

        if news:
            newsPerRound = len(news) // qtd_rodadas
            if newsPerRound < 1:
                abort(400, "Erro: Noticias insuficientes para as rodadas")

        if not news:
            newsPerRound = 0

        if fakenews:
            fakenewsPerRound = len(fakenews) // qtd_rodadas
            if fakenewsPerRound < 1:
                abort(400, "Erro: FakeNews insuficientes para as rodadas")

        if not fakenews:
            fakenewsPerRound = 0

        rounds = {}
        for roundIndex in range(roundsQtd):
            roundIndex += 1  # retirar index = 0

            # SELECT RANDOMLY NEWS + FAKENEWS
            if news:
                roundNews = random.sample(news, newsPerRound)
            else:
                roundNews = []

            if fakenews:
                roundFakenews = random.sample(fakenews, fakenewsPerRound)
            else:
                roundFakenews = []

            roundCombined = roundNews + roundFakenews
            random.shuffle(roundCombined)

            # CREATING NEWS INDEX (1,2,3,4,5,6,7,8,9,...)
            rounds[roundIndex] = []
            if roundIndex == 1:
                itemIndex = 0
            else:
                itemIndex = (roundIndex - 1) * (newsPerRound + fakenewsPerRound)

            # BUILDING ROUNDS DICT
            # logging.info(roundCombined)
            for item in roundCombined:
                rounds[roundIndex].append({f"Noticia{itemIndex + 1}": item})
                itemIndex += 1

            # REMOVING SELECTED NEWS+FAKENEWS FROM RESPECTIVE DICT
            if roundNews:
                for item in roundNews:
                    i = news.index(item)
                    news.pop(i)

            if roundFakenews:
                for item in roundFakenews:
                    i = fakenews.index(item)
                    fakenews.pop(i)

        return rounds

    def gabaritoCreate(roundsDict: dict):
        gabarito = {}
        for roundIndex, rounds in roundsDict.items():
            for newsDict in rounds:
                for noticiaIndex, news in newsDict.items():
                    if not news["fake"]:
                        continue

                    gabarito[roundIndex] = {
                        "noticiaID": noticiaIndex,
                        "id": news["id"],
                        "local": news["fake_local"],
                    }

        return gabarito

    if not isinstance(qtd_rodadas, int):
        qtd_rodadas = 1

    if qtd_rodadas < 1:
        qtd_rodadas = 1

    rounds = roundsCreate(qtd_rodadas, db_noticias, db_fakenews)
    gabarito = gabaritoCreate(rounds)

    return {"Gabarito": gabarito, "Noticias": rounds}


def apiTodayFlow(weekday):
    todayFlow = SendPulse_Flows().select(categorizacao="dia", Dia_Semana=weekday)

    if not todayFlow:
        return Response("Sem Envios Hoje", status=200)

    return todayFlow


def threadGroups4(contacts):
    threadLength = len(contacts) // 3
    groups = {
        1: contacts[0:threadLength],
        2: contacts[threadLength : threadLength * 2],
        3: contacts[threadLength * 2 : threadLength * 3],
    }

    lastGroupLimit = threadLength * 3
    contactsRemaining = len(contacts) - lastGroupLimit

    if contactsRemaining:
        fromIndex = lastGroupLimit
        toIndex = fromIndex + len(contacts) - lastGroupLimit
        groups[4] = contacts[fromIndex:toIndex]

    return groups


def apiRegisterSend(weekday, ID_Flow_API):
    from time import strftime
    from tools.timeManipulate import FORMAT_DATA
    from services.sql.Envios import Envios

    Envios().insert(
        Dia_Semana=weekday,
        Data_Envio=strftime(FORMAT_DATA),
        ID_Flow_API=ID_Flow_API,
    )
