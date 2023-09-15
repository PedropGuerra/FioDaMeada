from datetime import date

def replace_space(text:str, replacements:dict):
    for to_replace in replacements:
        old = to_replace
        new = replacements[to_replace]
        text = text.replace(old,new)

    return text

with open('teste.txt', 'r') as text:
    text = text.read()

    replacements = {
        "{data}" : str(date.today()),
        "{headline}" : "Hoje é dia de bolo",
        "{noticia1}" : "Lula come bolo",
        "{noticia2}" : "Dilma come bolo",
        "{noticia3}" : "Temer come bolo",
        "{noticia4}" : "Bozo come bolo",
        "{link1}" : "google.com",
        "{link2}" : "netflix.com",
        "{link3}" : "facebook.com",
        "{link4}" : "twitter.com",
    }
    text = replace_space(text, replacements)

    print(text)

with open('teste.txt', 'r') as teste:
    teste = teste.read()
    print(teste.count("{noticia"))
