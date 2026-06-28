from openai import OpenAI, AsyncOpenAI, APIError, AuthenticationError
from dotenv import load_dotenv
from pydantic import BaseModel
import json
import asyncio

load_dotenv()

client = OpenAI()
client_async = AsyncOpenAI()

model="chatgpt-4o-mini"
istruzioni= (
    "Sei esperto in gnoseologia "
    "Rispondi con termini filosofici molto tecnici"
)


def callModel(text: str):
    try: 
        r =  client.responses.create(
           model=model,
           input=text,
           instructions=istruzioni  
        )
       
        return r.output_text.strip().lower()
    
    except AuthenticationError:
        return"Errore di autenticazione"
    except APIError as e:
        return f"APIError: {e}"
    

async def callModel_async(text: str):
    try: 
        r = await client_async.responses.create(
           model=model,
           input=text,
           instructions=istruzioni  
        )
       
        return r.output_text.strip().lower()
    
    except AuthenticationError:
        return"Errore di autenticazione"
    except APIError as e:
        return f"APIError: {e}"
    

class Ticket(BaseModel):
    id: int
    messaggio: str


def carica_tickets():
    with open("tickets.json", encoding="utf-8") as f:
        dati = json.load(f)
        return [Ticket(**t) for t in dati]




serialResps = [callModel(t.messaggio) for t in carica_tickets()]

async def GetPar():
    return await asyncio.gather(
        *[callModel_async(t.messaggio) for t in carica_tickets()]
    )

parResps = asyncio.run(GetPar())