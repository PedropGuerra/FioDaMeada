def sanitize(input, url=False, removeBlankLines=False):
    import bleach
    import lxml.html
    import re

    if input != None:
        input = lxml.html.document_fromstring(input).text_content()
        regexHTML = r"&.*?;|\/p&.*?;|p&.*?;|<.*?>|div class=.*|/div"
        regexURL = (
            r"(?:(https|http)\s?:\/\/)(\s)*(www\.)?(\s)*((\w|\s)+\.)*([\w\-\s]+\/)*([\w\-]+)((\?)?[\w\s]*=\s*[\w\%&]*)*"
            if not url
            else ""
        )
        compileRegex = re.compile(regexURL + "|" + regexHTML)
        input = bleach.clean(re.sub(compileRegex, "", input))
        return input if not removeBlankLines else removeBlankLines(input)

    else:
        return input


def removeBlankLines(texto):
    linhas = texto.split("\n")
    resultado = []
    linha_em_branco = False

    for linha in linhas:
        if linha.strip():  # Verifica se a linha não está em branco
            if linha_em_branco:
                resultado.append("")  # Adiciona uma linha em branco entre textos
            resultado.append(linha)
            linha_em_branco = False
        else:
            linha_em_branco = True

    return "\n".join(resultado)


def valuesToDatabaseString(tipo: str, values: dict) -> str:
    """Coloque todos os valores em uma lista ordenada por como será enviado ao DB
    tipo = "insert"/"update"
    """
    value_string = ""

    match tipo:
        case "insert":
            for count, index in enumerate(values):
                if values[index] is None or values[index] == "":
                    values[index] = "null"

                values[index] = (
                    f"'{values[index]}'" if values[index] != "null" else "null"
                )

                if count != len(values) - 1:
                    values[index] = values[index] + ","

                value_string += values[index]

            return value_string

        case "update":
            set_string: str = ""

            for index in values:
                if values[index] is None:
                    continue

                value_string = f"{index} = '{values[index]}' "  # manter espaço
                set_string += value_string

            return set_string
