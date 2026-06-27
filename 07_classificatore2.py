from dotenv import load_dotenv
from openai import OpenAI, AsyncOpenAI, APIError, RateLimitError, AuthenticationError

load_dotenv()

client = OpenAI()
client_async = AsyncOpenAI()

model = "gpt-4o-mini"

istruzioni = (
    "Sei un esperto di medicina "
    "Risponi con linguaggio tecnico"
    )

def classificaTesto(testo):
    try:
        res = client.responses.create(
            input=testo,
            model=model,
            instructions=istruzioni,
        )
        return res.output_text.strip().lower()
    
    except AuthenticationError:
        return "AuthenticationError"
    except RateLimitError:
        return "Errore RateLimitError"
    except APIError as e:
        return f"C'è stato un errore con l'api: {e}"
