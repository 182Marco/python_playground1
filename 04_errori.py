from dotenv import load_dotenv
from openai import OpenAI, AuthenticationError, RateLimitError, APIError

load_dotenv()
client = OpenAI()

modello = "gpt-4o-mini"

def classifica(testo, client=client):
    try:
        risposta = client.responses.create(
            model= modello,
            input= testo,
            instructions="Sei un classifictore di ticket, rispondi con una sola parola tra commerciale, tecnico, fatturazione, spedizione, generale",
        )
        return risposta.output_text
    except AuthenticationError:
        return "Errore autenticazione"
    except RateLimitError:
        return "Troppe richieste" # Qui si potrebbe ad esempio pensare di fargli rifare la chiamata dopo 10s
    except APIError as e:
        return f"Errore dell'api: {e}"
    

print(classifica("Non ho ricevuto il collo"))

client = OpenAI(api_key="-wrong-")


print(classifica("Non ho ricevuto il collo", client))
