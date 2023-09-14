import feedparser
from sql_fiodameada import (
    Noticias,
    Parceiros,
    connect_db,
    json_to_dict,
    FORMAT_DATA,
)


class FioDaMeada_Script_Crawling:
    def __init__(self) -> None:
        self.queue: dict = {}
        self.logica_script()

    def logica_script(self) -> None:
        info_raspagem = self.import_info_raspagem()
        if not info_raspagem:
            print("Sem Parceiros Disponíveis")
            exit()
        self.add_in_queue(info_raspagem)
        self.import_noticias()

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
                # feed["noticias"][i] = {
                #     "Headline": getattr(entrie, tag_headline),
                #     "Text": getattr(entrie, tag_texto),
                #     "Resumo": getattr(entrie, tag_resumo),
                #     "Data": entrie.published,
                # }

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

    def insert_Noticias_Preferencias_DB(self):
        pass
        # posso tentar fazer algo na web que a pessoa possa nos ajudar
        # não consigo definir precisamente qual é o tema de uma notícia sem alguma inteligência artificial ou um humano


if __name__ == "__main__":
    instancia = FioDaMeada_Script_Crawling()
    print(instancia.import_links_parceiros())
