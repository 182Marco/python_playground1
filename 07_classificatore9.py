from openai import OpenAI, AuthenticationError, APIError, AsyncOpenAI
from dotenv import load_dotenv
from pydantic import BaseModel
import asyncio
import json


load_dotenv()

model="gpt-4o-mini"
istruzioni= (
    "Sei un esperto della filosofia di Nietzsche "
    "usa ogni appiglio che possa dare il messaggio per rispondere con i concetti di Nietzsche a costo di andare fuori tema"
)

client = OpenAI(max_retries=3, timeout=30)
client_async = AsyncOpenAI(max_retries=3, timeout=30)


def classifica(text: str):
    try:
        r = client.responses.create(
            input=text,
            model=model,
            temperature=2,
            instructions=istruzioni
        )

        return r.output_text.strip().lower()

    except RuntimeError as e:
        return f"RuntimeError: {type(e).__name__}"
    except AuthenticationError:
        return "AuthenticationError"
    except APIError as e:
        return f"APIError: {type(e).__name__}"
    

async def async_classifica(text: str):
    try:
        r = await client_async.responses.create(
            input=text,
            model=model,
            temperature=2,
            instructions=istruzioni
        )

        return r.output_text.strip().lower()

    except RuntimeError as e:
        return f"RuntimeError: {type(e).__name__}"
    except AuthenticationError:
        return "AuthenticationError"
    except APIError as e:
        return f"APIError: {type(e).__name__}"


class Ticket(BaseModel):
    id: int
    messaggio: str


def caricaTicket():
    with open("tickets.json", encoding="utf-8") as f:
        dati = json.load(f)
        return [Ticket(**t) for t in dati]
    
allTicketsFormatted = caricaTicket()
    
resp = [classifica(t.messaggio) for t in allTicketsFormatted]

async def getParalleliTicketsResp():
    return await asyncio.gather(
        *[async_classifica(t.messaggio) for t in allTicketsFormatted]
    )

respParallel = asyncio.run(getParalleliTicketsResp())