from SQL.sql_fiodameada import Noticias, connect_db, Preferencia_Usuarios

connect_db()

# noticias = Noticias().select(categorizacao="data", data_desde="2023/09/01")
preferencias = Preferencia_Usuarios().select()

print(preferencias)
