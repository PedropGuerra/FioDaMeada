from flask import render_template, request, redirect, url_for
from services.sql.Preferencia_Usuarios import Preferencia_Usuarios
from services.sql.Noticias import Noticias


def adminAvailableNewsToAssociate():
    from datetime import date
    import logging

    dictNoticias = {}

    noticias = Noticias().select(formato="associacao")
    if len(noticias) >= 1:
        """
        {1: {ID : ID, Link:Link, Headline:Headline, Resumo:Resumo, data_desde:desde, data_ate:ate}
        """
        if isinstance(noticias, list) and len(noticias[0]) == 4:
            noticias = list(
                map(
                    lambda noticia: {
                        "ID": noticia[0],
                        "Link": noticia[1],
                        "Headline": noticia[2][:150],
                        "Resumo": noticia[3][:400],
                    },
                    noticias,
                )
            )

            for noticia in noticias:
                proxIndex = len(dictNoticias) + 1
                dictNoticias[proxIndex] = noticia

    else:
        logging.info(noticias)

    return dictNoticias


def adminAssociacaoNoticias_Render():
    data = request.form.to_dict(flat=False)

    print(data)

    for idNoticia in data:
        if "Inutilizar" in data:
            Noticias().update(ID_Noticia=idNoticia, Status="1")
            continue

        for idPref in data[idNoticia]:
            if idPref == "":
                continue

            else:
                Noticias.insert_preferencia(
                    ID_Pref_Usuario=idPref, ID_Noticia=idNoticia
                )

    return redirect(url_for("adminAssociacaoNoticias"))


def adminAssociacaoNoticias():
    preferencias = Preferencia_Usuarios().select()
    noticias = adminAvailableNewsToAssociate()

    return render_template(
        "associacaoNoticias.html", noticias=noticias, preferencias=preferencias
    )
