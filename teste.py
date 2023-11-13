import json

with open("response.json", "r") as file:
    file = json.loads(file.read())

# print(file["Noticias"]["1"]["Noticia1"]["headline"])
print(file["Noticias"]["2"][0])
