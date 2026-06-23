from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

modello = "gpt-4o-mini"

msg="non mi è arrivato il collo"

risposta = client.responses.create(
    model=modello,
    instructions="Sei un classifictore di ticket, rispondi con una sola parola tra commerciale, tecnico, fatturazione, spedizione, generale",
    input=msg,
)

print(risposta.output_text)