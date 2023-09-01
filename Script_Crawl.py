import feedparser
from SQL.sql_fiodameada import Noticias, Parceiros, connect_db, disconnect_db


class FioDaMeada_Script_Crawling:
    def __init__(self) -> None:
        connect_db()

    def logica_script(self) -> None:
        info_parceiros = self.import_links_parceiros()
        rss_feed, web_scrapping = self.definir_metodo(info_parceiros)

        rss_feed_dict = self.import_rss_feed(rss_feed) if rss_feed else None
        web_scrapping_dict = (
            self.import_web_scrapping(web_scrapping) if web_scrapping else None
        )

    def import_links_parceiros(self):
        return Parceiros().select(categorizacao="script")

    def definir_metodo(self, infos: list) -> tuple:
        rss_feed = []
        web_scrapping = []

        for info in infos:
            match info[1]:
                case 1:  # rss
                    rss_feed.append(info)

                case 2:  # web
                    web_scrapping.append(info)

        return (rss_feed, web_scrapping)

    def import_rss_feed(self, rss_feed_list: list) -> dict:
        rss_dict = {}

        for feed in rss_feed_list:
            ID_Parceiro = feed[0]
            Link_Parceiro = feed[3]
            rss_dict[ID_Parceiro] = feedparser.parse(Link_Parceiro)

        return rss_dict

    def import_web_scrapping(self, web_scrapping_list: list) -> dict:
        pass

    def update_Parceiros_DB(self):
        pass

    def resumir_publicacao(self):
        pass

    def insert_Noticias_DB(self):
        pass

    def insert_Noticias_Preferencias_DB(self):
        pass


if __name__ == "__main__":
    instancia = FioDaMeada_Script_Crawling()
    print(instancia.import_links_parceiros())
