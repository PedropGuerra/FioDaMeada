from SQL.sql_fiodameada import connect_db, Noticias, Usuarios, disconnect_db

connect_db()
noticias = Noticias()
usuarios = Usuarios()
usuarios.select("2023-08-23")

disconnect_db()
