import feedparser
from services.sql.Noticias import Noticias
from services.sql.Parceiros import Parceiros
from services.SendPulse import SendPulse
import re
import lxml.html
import services.chatgpt as GPT
import random
from tools.timeManipulate import FORMAT_DATA
from tools.stringManipulate import removeBlankLines, sanitize
import logging


class FioDaMeada_Script_Crawling:
    def __init__(self) -> None:
        self.queue: dict = {}
        self.logica_script()

    def logica_script(self):
        info_raspagem = self.import_info_raspagem()
        logging.info(info_raspagem)

        if info_raspagem:
            self.add_in_queue(info_raspagem)
            self.import_noticias()
        SendPulse().syncFlows()

    def import_info_raspagem(self):
        info = Parceiros().select(categorizacao="script")
        logging.info(info)
        return info

    def add_in_queue(self, info: list) -> dict:
        import ast

        for feed in info:
            # feed = feed[i]
            ID_Parceiro = feed[0]
            Link_Parceiro = feed[3]
            Tags_HTML_Raspagem = feed[2]
            ID_Metodo_Coleta = feed[1]
            self.queue[ID_Parceiro] = {
                "metodo": ID_Metodo_Coleta,
                "link": Link_Parceiro,
                "tags_html": ast.literal_eval(Tags_HTML_Raspagem),
                "noticias": {},
            }

    def import_noticias(self):
        from time import strftime
        import json
        import logging

        for ID_Parceiro in self.queue:
            feed = self.queue[ID_Parceiro]
            feed_link_parse = feedparser.parse(feed["link"])
            tags_html = feed["tags_html"]
            tag_headline = tags_html["Headline"]
            tag_texto = tags_html["Text"]

            for entrie in feed_link_parse.entries:
                headline = getattr(entrie, tag_headline)
                headline = sanitize(headline, blankLines=True, url=True)

                if Noticias().confirm_noticia(headline):
                    continue

                else:
                    resumo = getattr(entrie, tag_texto)
                    resumo = sanitize(resumo, blankLines=True, url=True)

                    headline, resumo, local, fake = GPT.escolherFakeNews(
                        headline, resumo
                    )

                    logging.info(f"Inserting {ID_Parceiro} - {getattr(entrie, 'link')}")
                    Noticias().insert(
                        ID_Parceiro=ID_Parceiro,
                        Link_Publicacao=getattr(entrie, "link"),
                        Headline_Publicacao=f"""{headline}""",
                        Resumo_Publicacao=f"""{resumo}""",
                        Data_Publicacao_Parceiro=strftime(
                            FORMAT_DATA, entrie.published_parsed
                        ),
                        Fake=fake,
                        Fake_Local=local,
                    )
            Parceiros().update_ult_raspagem(ID_Parceiro)
        
