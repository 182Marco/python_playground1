from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

modello = "gpt-4o-mini"

print("temperature = 0:")

msg="non mi è arrivato il collo"


for _ in range(3):
    risposta = client.responses.create(
        model=modello,
        instructions="Sei un classifictore di ticket, rispondi con una sola parola tra commerciale, tecnico, fatturazione, spedizione, generale",
        input=msg,
        temperature=0
    )