import feedparser
from SCRIPTS.sql_fiodameada import (
    Noticias,
    Parceiros,
    connect_db,
    json_to_dict,
    FORMAT_DATA,
)
from SCRIPTS.integracao import Auth_SendPulse


class FioDaMeada_Script_Crawling:
    def __init__(self) -> None:
        self.queue: dict = {}
        self.logica_script()

    def logica_script(self):
        info_raspagem = self.import_info_raspagem()
        if not info_raspagem:
            return "SemParceiros"
        self.add_in_queue(info_raspagem)
        self.import_noticias()
        self.sync_formatos()

        return 200


    def import_info_raspagem(self):
        connect_db()
        return Parceiros().select(categorizacao="script")

    def add_in_queue(self, info: list) -> dict:
        for feed in info:
            # feed = feed[i]
            print(feed)
            ID_Parceiro = feed[0]
            Link_Parceiro = feed[3]
            Tags_HTML_Raspagem = feed[2]
            ID_Metodo_Coleta = feed[1]
            self.queue[ID_Parceiro] = {
                "metodo": ID_Metodo_Coleta,
                "link": Link_Parceiro,
                "tags_html": json_to_dict(Tags_HTML_Raspagem),
                "noticias": {},
            }

    def import_noticias(self):
        from time import strftime

        for ID_Parceiro in self.queue:
            feed = self.queue[ID_Parceiro]
            feed_link_parse = feedparser.parse(feed["link"])
            tag_headline = feed["tags_html"]["Headline"]
            tag_texto = feed["tags_html"]["Text"]
            # tag_resumo = feed["tags_html"]["Resumo"]

            for entrie in feed_link_parse.entries:

                Noticias().insert(
                    ID_Parceiro=ID_Parceiro,
                    Link_Publicacao=getattr(entrie, "link"),
                    Headline_Publicacao=f"""{getattr(entrie, tag_headline)}""",
                    Resumo_Publicacao=f"""{getattr(entrie, tag_texto)}""",
                    Data_Publicacao_Parceiro=strftime(
                        FORMAT_DATA, entrie.published_parsed
                    ),
                )
            Parceiros().update_ult_raspagem(ID_Parceiro)


    def sync_formatos(self):
        API = Auth_SendPulse()
        API.sync_formatos()