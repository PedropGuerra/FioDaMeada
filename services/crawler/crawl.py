from time import strftime
import feedparser
from tools.stringManipulate import sanitize
from tools.timeManipulate import FORMAT_DATA
from services.chatgpt import escolherFakeNews
from services.sql.Noticias import Noticias
from services.sql.Parceiros import Parceiros
from threading import Thread


def crawl(info: dict):
    parse = feedparser.parse(info["link"])

    for entrie in parse.entries:
        headline = getattr(entrie, info["tags_html"]["Headline"])
        headline = sanitize(headline, blankLines=True, url=True)

        resumo = getattr(entrie, info["tags_html"]["Text"])
        resumo = sanitize(resumo, blankLines=True, url=True)

        escolhaFakeNews = escolherFakeNews(headline, resumo)
        headline, resumo, local, fake = escolhaFakeNews

        parceiroID = info["id"]

        def insertInDB():
            Noticias().insert(
                ID_Parceiro=parceiroID,
                Link_Publicacao=getattr(entrie, "link"),
                Headline_Publicacao=headline,
                Resumo_Publicacao=resumo,
                Data_Publicacao_Parceiro=strftime(FORMAT_DATA, entrie.published_parsed),
                Fake=fake,
                Fake_Local=local,
            )

        Thread(target=insertInDB).start()

        Thread(
            target=Parceiros().update_ult_raspagem,
            args=(str(parceiroID),),
        ).start()
