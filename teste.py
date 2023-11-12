import tools.flaskSupportTools as apiTools


dbFakeNews: dict = apiTools.dbSelectNoticias(
    {
        "formato": "qtd_fakenews",
        "qtd_fakenews": 2,
        "contact_id": "6500e99d564ffa8cf10d994f",
        "preferencias_id": [(1, "Política"), (2, "Saúde"), (3, "Entretenimento")],
    }
)

# for index, item in enumerate(dbFakeNews):
#     print(index)
#     print(item)
#     print(type(item))
#     print("\n")

teste = apiTools.apiFormatNoticias(dbFakeNews)

print(teste)
