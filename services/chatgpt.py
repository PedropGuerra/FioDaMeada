import openai
import services.secrets as os
import logging

openai.api_key = os.getenv("CGPT_KEY")


def escolherFakeNews(headline: str, text: str, test=False) -> tuple:
    import random

    escolha = random.choices(["s", "n"], weights=[35, 65], k=1)[
        0
    ]  # 35% de chance de se tornar uma FakeNews
    local = None

    if escolha == "s":
        local = random.choice(
            ["contexto", "introducao", "conclusao"]
        )  # escolhe apenas um local aleatoriamente
        fake = 1
        if not test:
            headline, text = criar_fakenews(headline=headline, texto=text, local=local)
            return (
                headline,
                text,
                local,
                fake,
            )

        else:
            return (headline, text, local, fake)

    else:
        fake = 0
        return (headline, text, local, fake)


def criar_fakenews(headline: str, texto: str, local: str):
    """
    local = "contexto" / "introducao" / "conclusao"
    """

    user_input = f"""
	Headline: {headline}

	Texto: {texto}
	"""
    try:
        default_system = f"Altere o/a {local} do texto para criar uma mentira e, se caso necessário, altere a Headline para condizer com o texto."

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": default_system},
                {"role": "user", "content": user_input},
            ],
            temperature=0,
            max_tokens=1024,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )

        # tratamento da resposta para retornar
        resp_headline = response["choices"][0]["message"]["content"].split("\n")[0]
        resp_texto = (
            response["choices"][0]["message"]["content"]
            .removeprefix(resp_headline)
            .strip()
            .removeprefix("Texto: ")
        )

        resp_headline = resp_headline.removeprefix("Headline: ")

        return (resp_headline, resp_texto)

    except Exception as e:
        logging.info(e)
        return (headline, texto)
