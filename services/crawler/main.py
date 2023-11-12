from services.sql.Parceiros import Parceiros
from services.sql.Noticias import Noticias
from services.SendPulse import SendPulse
from services.crawler.crawl import crawl
from threading import Thread
import logging

logging.basicConfig(level=logging.DEBUG)


def queueBuild(parceiros):
    import ast

    queue = {}
    for info in parceiros:
        parceiroID = info[0]
        parceiroLink = info[3]
        parceiroHtmlTags = info[2]
        parceiroMetodoColeta = info[1]

        if Noticias().confirm_noticia(parceiroLink):
            continue

        queue[parceiroID] = {
            "id": parceiroID,
            "metodo": parceiroMetodoColeta,
            "link": parceiroLink,
            "tags_html": ast.literal_eval(parceiroHtmlTags),
            "noticias": {},
        }

    return queue


def run():
    Thread(target=SendPulse().syncFlows)
    parceirosToCrawl = Parceiros().select(categorizacao="script")
    queue: dict = queueBuild(parceirosToCrawl)
    logging.info(queue)

    for info in queue.values():
        logging.info(info)
        crawl(info)
