import feedparser
from SCRIPTS.sql_fiodameada import (
    Noticias,
    Parceiros,
    json_to_dict,
    FORMAT_DATA,
)
from SCRIPTS.integracao import Auth_SendPulse
import re
import lxml.html
from SCRIPTS.chatgpt import criar_fakenews
import random

def remover_linhas_em_branco(texto):
    linhas = texto.split('\n')
    resultado = []
    linha_em_branco = False

    for linha in linhas:
        if linha.strip():  # Verifica se a linha não está em branco
            if linha_em_branco:
                resultado.append('')  # Adiciona uma linha em branco entre textos
            resultado.append(linha)
            linha_em_branco = False
        else:
            linha_em_branco = True

    return '\n'.join(resultado)


class FioDaMeada_Script_Crawling:
    def __init__(self) -> None:
        self.queue: dict = {}
        self.logica_script()

    def logica_script(self):
        info_raspagem = self.import_info_raspagem()
        if info_raspagem:
            self.add_in_queue(info_raspagem)
            self.import_noticias()
        self.sync_formatos()

    def import_info_raspagem(self):
        return Parceiros().select(categorizacao="script")

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
                headline = self.sanitize_text(headline)
                
                if Noticias().confirm_noticia(headline):
                    continue
                
                else:
                    resumo = getattr(entrie, tag_texto)
                    resumo = self.sanitize_text(resumo)
                    
                    headline, resumo, local, fake = self.transformar_fakenews(headline, resumo)
                
                    Noticias().insert(
                        ID_Parceiro=ID_Parceiro,
                        Link_Publicacao=getattr(entrie, "link"),
                        Headline_Publicacao=f"""{headline}""",
                        Resumo_Publicacao=f"""{resumo}""",
                        Data_Publicacao_Parceiro=strftime(
                            FORMAT_DATA, entrie.published_parsed
                        ),
                        Fake = fake,
                        Fake_Local = local,
                    )
            Parceiros().update_ult_raspagem(ID_Parceiro)

    def sync_formatos(self):
        API = Auth_SendPulse()
        API.sync_formatos()

    def sanitize_text(self, text: str):
        text = lxml.html.document_fromstring(text).text_content()
        tags_html = r"&.*?;|\/p&.*?;|p&.*?;|<.*?>|div class=.*|/div"
        urls = r"(?:(https|http)\s?:\/\/)(\s)*(www\.)?(\s)*((\w|\s)+\.)*([\w\-\s]+\/)*([\w\-]+)((\?)?[\w\s]*=\s*[\w\%&]*)*"
        comp = re.compile(urls + "|" + tags_html)
        text = re.sub(comp, "", text)

        return remover_linhas_em_branco(text)


    def transformar_fakenews(self, headline:str, text:str):
        escolha = random.choices(["s","n"], weights=[35,65], k=1) #35% de chance de se tornar uma FakeNews
        local = None
        

        if escolha == "s":
            local = random.choice(["contexto", "introducao", "conclusao"]) #escolhe apenas um local aleatoriamente
            fake = 1
            return (criar_fakenews(headline=headline, texto=text, local=local), local, fake)

        else:
            fake = 0
            return (headline, text, local, fake)








