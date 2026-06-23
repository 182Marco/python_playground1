import json
import time
import asyncio
from dotenv import load_dotenv
from openai import (
    OpenAI,
    AsyncOpenAI,
    APIError,
    AuthenticationError,
    RateLimitError
)
from pydantic import BaseModel

load_dotenv()
client = OpenAI()
client_async = AsyncOpenAI()
modello = "gpt-4o-mini"

istruzioni = "Sei un classificatore di ticket, rispondi con una sola parola tra commerciale, tecnico, fatturazione, spedizione, generale"

class Ticket(BaseModel):
    id: int
    messaggio: str

def carica_ticket():
    with open("tickets.json", encoding="utf-8") as f:
        dati = json.load(f)
        return [Ticket(**d) for d in dati]


def classifica(testo, client=client):
    try:
        risposta = client.responses.create(
            model= modello,
            input= testo,
            instructions=istruzioni,
        )
        return risposta.output_text.strip().lower()
    except AuthenticationError:
        return "Errore autenticazione"
    except RateLimitError:
        return "Troppe richieste" # Qui si potrebbe ad esempio pensare di fargli rifare la chiamata dopo 10s
    except APIError as e: # questo è il generico, mai metterlo per primo che si mangia gli altri
        return f"Errore dell'api: {e}"
    

async def classifica_async(testo, client_async=client_async):
        try:
            risposta = await client.responses.create( #questo await è l'unica cosa diversa dal metodo senza await
                model= modello,
                input= testo,
                instructions=istruzioni,
            )
            return risposta.output_text.strip().lower()
        except AuthenticationError:
            return "Errore autenticazione"
        except RateLimitError:
            return "Troppe richieste" # Qui si potrebbe ad esempio pensare di fargli rifare la chiamata dopo 10s
        except APIError as e: # questo è il generico, mai metterlo per primo che si mangia gli altri
            return f"Errore dell'api: {e}"

async def in_parallelo(tickets):
    return await asyncio.gather(*[classifica_async(t.messaggio) for t in tickets]) 


tickets = carica_ticket()

# SERIE
inizio = time.time()
risultati = [classifica(t.messaggio) for t in tickets]
print("Risultati seriale", f"{risultati} in {round(time.time() - inizio, 2)} secondi" )

# PARALLELO
inizio = time.time()
risultati = [classifica_async(t.messaggio) for t in tickets]
print("Risultati seriale", f"{risultati} in {round(time.time() - inizio, 2)} secondi" )