from openai import OpenAI, AsyncOpenAI, APIError, AuthenticationError, RateLimitError
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()
client_async = AsyncOpenAI()

model = "chatgpt-4o-mini"
istruzioni = (
    "Sei un esperto di cucito "
    "rispondi con i termini tecnici del mestiere"
)

def callAi(testo):
    try:
        res = client.responses.create(
            input=testo,
            model=model,
            instructions=istruzioni
        )
        return res.output_text.strip().lower()

    except AuthenticationError:
        return "Autenticazione errata" 
    except RateLimitError:
        return "RateLimitError"
    except APIError as e:
        return f"C'è stato un errore nella chiamata api: {e}"
