from flask import request, redirect, url_for, make_response, render_template, flash
import json


def adminCadastroParceiros_tags(tags, parseFeedItem, parceiroID):
    if request.method == "POST":
        from services.sql.Parceiros import Parceiros

        tagsDict = {
            "Headline": request.form["Headline"],
            "Text": request.form["Text"],
            "Resumo": request.form["Resumo"],
        }
        Parceiros().update(
            ID_Parceiro=parceiroID, Tags_HTML_Raspagem=json.dumps(tagsDict)
        )

        redirect(url_for("adminCadastroParceiros"))

    return render_template(
        "parceiroTags.html",
        tags=tags,
        parseFeedItem=parseFeedItem,
        parceiroID=parceiroID,
    )


def adminCadastroParceiros():
    if request.method == "POST":
        from services.sql.Parceiros import Parceiros
        import feedparser

        formDict = request.form.to_dict(flat=True)

        print(formDict)
        print(formDict["Nome_Parceiro"])
        parceiroID = Parceiros().confirm(Nome_Parceiro=formDict["Nome_Parceiro"])

        if not parceiroID:
            Parceiros().insert(
                Nome_Parceiro=formDict["Nome_Parceiro"],
                Link_Parceiro=formDict["Link_Parceiro"],
                ID_Metodo_Coleta=request.form["ID_Metodo_Coleta"],
                Nome_Responsavel=request.form["Nome_Responsavel"],
                Contato_Responsavel=request.form["Contato_Responsavel"],
                Licenca_Distrib=request.form["Licenca_Distrib"],
            )
            parse = feedparser.parse(formDict["Link_Parceiro"])
            tags = Parceiros().confirm_tags(parse=parse)
            parseFeedItem = parse.entries[3]

            adminCadastroParceiros_tags(tags, parseFeedItem, parceiroID)

        else:
            return render_template("erroParceiroCadastrado.html")

    return render_template("cadastro.html")
