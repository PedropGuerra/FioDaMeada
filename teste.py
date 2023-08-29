from SQL.sql_fiodameada import Noticias, connect_db, disconnect_db


connect_db()


instancia = Noticias()

print(instancia.select(categorização="tema", parceiro_id="3"))

disconnect_db()
