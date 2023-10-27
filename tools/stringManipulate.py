def sanitize(input, url=False, blankLines=True):
    import bleach
    import lxml.html
    import re

    if input != None:
        try:
            input = lxml.html.document_fromstring(input).text_content()

        except:
            pass
        # input = bleach.clean(input)
        regexHTML = r"&.*?;|\/p&.*?;|p&.*?;|<.*?>|div class=.*|/div"
        # regexURL = (
        #     r"(?:(https|http)\s?:\/\/)(\s)*(www\.)?(\s)*((\w|\s)+\.)*([\w\-\s]+\/)*([\w\-]+)((\?)?[\w\s]*=\s*[\w\%&]*)*"
        #     if not url
        #     else ""
        # )
        regexURL = r"https?://\S+\s*"
        compileRegex = re.compile(regexURL + "|" + regexHTML)
        input = re.sub(compileRegex, "", input)
        return input if blankLines else removeBlankLines(input)

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
    "insert" - {variavel : valor, variavel : valor} == 'valor1', 'valor2'
    "insertMultiple" - {0:{variavel : valor, variavel : valor}} == ('valor1', 'valor2'), ('valor1', 'valor2')
    "update" - {variavel : valor, variavel : valor} == variavel1 = 'valor1', variavel2 = 'valor2'
    """
    value_string = ""

    match tipo:
        case "insert":
            for index, key in enumerate(values):
                value = values[key]
                if value is None or value == "":
                    value = "null"

                value = f"'{value}'"

                quantidadeValues = len(values) - 1
                if index != quantidadeValues:
                    value += ","

                value_string += value

            return value_string

        case "insertMultiple":
            set_string: str = ""
            for valueDict in values.values():
                valueDict = list(
                    map(lambda value: value if value else "null", valueDict.values())
                )
                for index, value in enumerate(valueDict):
                    if index == 0:
                        set_string += ", (" if len(set_string) != 0 else "("

                    set_string += f"'{value}'"
                    set_string += f"," if index != len(valueDict) - 1 else ""

                    if index == len(valueDict) - 1:
                        set_string += ")"

            return set_string

        case "update":
            set_string: str = ""

            for index in values:
                if values[index] is None:
                    continue

                value_string = f"{index} = '{values[index]}' "  # manter espaço
                set_string += value_string

            return set_string
