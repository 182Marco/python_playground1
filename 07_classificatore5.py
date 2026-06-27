from openai import OpenAI, AsyncOpenAI, APIError, AuthenticationError, RateLimitError
from dotenv import load_dotenv
from pydantic import BaseModel
import json


load_dotenv()

client = OpenAI()
async_client = AsyncOpenAI()

istruzioni = (
    "Sei un esperto di abeti "
    "rispondi in modo tecnico"
)

model ="chatgpt-4o-mini"

def classifica(testo):
    try:
        res = client.responses.create(
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
        return f"Api error: {e}"
    

async def async_classifica(testo):
    try:
        res = await async_client.responses.create(
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
        return f"Api error: {e}"
    

class Ticket(BaseModel):
    id: int
    messaggio: str


def getTickets():
    with open("tickets.json", encoding="utf-8") as f:
        dati = json.load(f)
        return [Ticket(**d) for d in dati]
 