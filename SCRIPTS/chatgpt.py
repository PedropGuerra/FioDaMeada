import openai
import os

openai.api_key = os.getenv("CGPT_KEY")

def criar_fakenews(headline:str ,texto:str, local:str):
	"""
	local = "contexto" / "introducao" / "conclusao"
	"""

	user_input = f"""
	Headline: {headline}

	Texto: {texto}
	"""

	default_system = f"Altere o/a {local} do texto para criar uma mentira e, se caso necessário, altere a Headline para condizer com o texto."

	response = openai.ChatCompletion.create(
		model = "gpt-3.5-turbo",
		messages =[
			{
			"role" : "system",
			"content" : default_system
			},
			{
			"role" : "user",
			"content" :user_input
			}
		],
		temperature=0,
		max_tokens=1024,
		top_p=1,
		frequency_penalty=0,
		presence_penalty=0)

	#tratamento da resposta para retornar
	resp_headline = response["choices"][0]["message"]["content"].split("\n")[0]
	resp_texto = response["choices"][0]["message"]["content"].removeprefix(resp_headline).strip().removeprefix("Texto: ")

	resp_headline = resp_headline.removeprefix("Headline: ")


	return (resp_headline, resp_texto)
	
