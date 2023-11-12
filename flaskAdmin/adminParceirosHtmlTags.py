from flask import request, render_template, Response


def adminParceirosHtmlTags():
    import feedparser
    from services.sql.Parceiros import Parceiros
    from urllib.parse import unquote

    rsslink = unquote(request.args.get("rsslink"))
    parse = feedparser.parse(rsslink)
    tags = Parceiros().confirm_tags(parse=parse)

    parseFeedItem = parse.entries[3]

    return render_template(
        "parceiroTagsView.html", tags=tags, parseFeedItem=parseFeedItem
    )
