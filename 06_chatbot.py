from dotenv import load_dotenv
from openai import OpenAI, APIError

load_dotenv()
client = OpenAI()

modello = "gpt-4o-mini"

messages = []

print("Ciao sono il tuo assistente personale. Scrivi 'esci' per terminare")


while True:
    text = input("Marco: ")
    if text == "esci":
        break

    messages.append({"role" : "user", "content" : text})
    risposta = ""
    print("Assistente:", end="", flush=True)

    try:
        stream = client.responses.create(
            model=modello,
            input=messages,
            instructions="Sei un assistente personale. Rispondi in maniera concisa",
            stream=True
        )
        for evento in stream:
            if evento.type == "response.output_text.delta":
              print(evento.delta, end="", flush=True)
              risposta += evento.delta
        messages.append({"role": "assistant", "content": risposta})

    except APIError as e:
        print(f"api Error {e}")