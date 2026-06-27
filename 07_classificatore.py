import json
import time
import asyncio
from collections import Counter
from dotenv import load_dotenv
from openai import (
    OpenAI,
    AsyncOpenAI,
    APIError,
    AuthenticationError,
    RateLimitError
)
from pydantic import BaseModel
from utils import stampa_risultati

load_dotenv()

client = OpenAI()
client_async = AsyncOpenAI()

modello = "gpt-4o-mini"

istruzioni = (
    "Sei un classificatore di ticket. "
    "Rispondi con una sola parola tra: "
    "commerciale, tecnico, fatturazione, spedizione, generale"
)


# ---------------- MODEL ----------------

class Ticket(BaseModel):
    id: int
    messaggio: str


# ---------------- CARICAMENTO DATI ----------------

def carica_ticket():
    with open("tickets.json", encoding="utf-8") as f:
        dati = json.load(f)
        return [Ticket(**d) for d in dati] # dictionary unpacking



# ---------------- CLASSIFICAZIONE SYNC ----------------

def classifica(testo):
    try:
        risposta = client.responses.create(
            model=modello,
            input=testo,
            instructions=istruzioni,
        )
        return risposta.output_text.strip().lower()

    except AuthenticationError:
        return "errore_auth"
    except RateLimitError:
        return "rate_limit"
    except APIError as e:
        return f"api_error: {e}"


# ---------------- CLASSIFICAZIONE ASYNC ----------------

async def classifica_async(testo):
    try:
        risposta = await client_async.responses.create(
            model=modello,
            input=testo,
            instructions=istruzioni,
        )
        return risposta.output_text.strip().lower()

    except AuthenticationError:
        return "errore_auth"
    except RateLimitError:
        return "rate_limit"
    except APIError:
        return "api_error"


async def in_parallelo(tickets):
    return await asyncio.gather(
        *[classifica_async(t.messaggio) for t in tickets]
    )


    print("\n" + "=" * 90)
    print(f"{titolo}".center(90))
    print("=" * 90)

    print(f"{'ID':<5} {'CATEGORIA':<15} MESSAGGIO")
    print("-" * 90)

    for t, r in zip(tickets, risultati):
        msg = (t.messaggio[:55] + "...") if len(t.messaggio) > 55 else t.messaggio
        print(f"{t.id:<5} {r.upper():<15} {msg}")

    print("-" * 90)

    print("\n📊 RIEPILOGO")
    print("-" * 40)

    conteggio = Counter(risultati)

    for categoria, n in conteggio.most_common():
        barra = "█" * n
        print(f"{categoria:<15} {n:<3} {barra}")

    print("-" * 40)
    print(f"⏱ Tempo totale: {tempo}s")
    print("=" * 90 + "\n")


# ---------------- MAIN ----------------

tickets = carica_ticket()


# ===== SERIALE =====
start = time.time()
risultati_sync = [classifica(t.messaggio) for t in tickets]
tempo_sync = round(time.time() - start, 2)

stampa_risultati(
    tickets,
    risultati_sync,
    "RISULTATI SERIALE",
    tempo_sync
)


# ===== PARALLELO =====
start = time.time()
risultati_async = asyncio.run(in_parallelo(tickets))
tempo_async = round(time.time() - start, 2)

stampa_risultati(
    tickets,
    risultati_async,
    "RISULTATI PARALLELO",
    tempo_async
)


