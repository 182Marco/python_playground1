from openai import OpenAI, AsyncOpenAI, APIError, AuthenticationError, RateLimitError
from dotenv import load_dotenv
from pydantic import BaseModel
import json


load_dotenv()

model="chatgpt-4o-mini"
client = OpenAI()
async_client = AsyncOpenAI()
istruzioni = (
    "Sei esperto di botanica "
    "rispondi in modo tecnico e aggiungendo le reazioni chimiche sottostanti ai processi"
)

def callAi(testo):
    try:
        res = client.responeses.create(
            input=testo,
            instructions=istruzioni,
            model=model
        )

        return res.output_text
    
    except RateLimitError as e:
        return f"RateLimitError: {e}"
    except AuthenticationError:
        return "AuthenticationError"
    except APIError as e:
        return f"APIError: {e}"
    
async def async_callAi(testo):
    try:
        res = await async_client.responeses.create(
            input=testo,
            instructions=istruzioni,
            model=model
        )

        return res.output_text.strip().lower()
    
    except RateLimitError as e:
        return f"RateLimitError: {e}"
    except AuthenticationError:
        return "AuthenticationError"
    except APIError as e:
        return f"APIError: {e}"
    

class Ticket(BaseModel):
    id: int
    messaggio: str


def getTickets():
    with open("tickets.json", encoding="utf-8") as f:
        dati = json.load(f)
        return [Ticket(**d) for d in dati]
    


tickets = getTickets()

responses = [callAi(t.messaggio) for t in tickets]
