from services.sql.Noticias import Noticias
from services.sql.Parceiros import Parceiros
from services.sql.SendPulse_Flows import SendPulse_Flows

import services.secrets as os
from flask import Response, abort
from services.SendPulse import SendPulse


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

        argsTransformed[htmlArgument] = argType(htmlArgument)

    return argsTransformed


def contactPreferences(contact_id):
    return SendPulse().getPreferencias(contact_id)


def apiFormatNoticias(noticias: dict):
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
    return Noticias().select(**select)


def dbAtualizarNoticiasContatos(contact_id, dbNoticias, dbFakeNews):
    if dbFakeNews is None:
        dbFakeNews = []

    if dbNoticias is None:
        dbNoticias = []

    if dbFakeNews or dbNoticias:
        ids_noticias = [noticia["id"] for noticia in dbNoticias + dbFakeNews]
        Noticias().noticias_usuario(contact_id, ids_noticias)


def apiResponseNoticias(
    qtd_noticias=False,
    qtd_fakenews=False,
    qtd_rodadas=False,
    db_noticias: dict = None,
    db_fakenews: dict = None,
):
    import random

    resp_gabarito = {}
    resp_noticias = {}

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


def apiTodayFlow(weekday):
    todayFlow = SendPulse_Flows().select(categorizacao="dia", Dia_Semana=weekday)

    if not todayFlow:
        abort(200, Response("Sem Envios Hoje"))

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
