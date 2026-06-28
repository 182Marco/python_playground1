from openai import RateLimitError, AuthenticationError, APIError, OpenAI,AsyncOpenAI
from dotenv import load_dotenv
from pydantic import BaseModel
import json
import asyncio

load_dotenv()

client = OpenAI()
client_async = AsyncOpenAI()

model="chatgpt-4o-mini"

intruzioni = (
    "Sei un esperto di moto d'acqua "
    "rispondi citando le specifiche tecniche dei motori"
)

def call_model(text: str):
    try:
        r = client.responses.create(
            input=text,
            model=model,
            instructions=intruzioni
        )
        return r.output_text.strip().lower()
    
    except RateLimitError as e:
        return f"RateLimitError {e}"
    except AuthenticationError:
        return "AuthenticationError"
    except APIError as e:
        return f"APIError {e}"
    

async def call_model_async(text: str):
    try:
        r =  await client_async.responses.create(
            input=text,
            model=model,
            instructions=intruzioni
        )
        return r.output_text.strip().lower()
    
    except RateLimitError as e:
        return f"RateLimitError {e}"
    except AuthenticationError:
        return "AuthenticationError"
    except APIError as e:
        return f"APIError {e}"
    

class Ticket(BaseModel):
    id: int
    messaggio: str
    

def getTickets():
    with open("tickets.json", encoding="utf-8") as f:
        data = json.load(f)
        return [Ticket(**t) for t in data]
    

def getRes():
    return [call_model(t.messaggio) for t in getTickets()]

async def getResParall():
    return await asyncio.gather(
        *[call_model_async(t.messaggio) for t in getTickets()]
    )

resParall = asyncio.run(getResParall())