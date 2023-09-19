from SCRIPTS.sql_fiodameada import Noticias, connect_db


connect_db()
noticias = Noticias().select(
    formato="qtd_noticias",
    qtd_noticias=3,
    contact_id=123,
    preferencias_id=(1, 2, 2),
)

print(noticias)
