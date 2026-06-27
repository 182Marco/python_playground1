from openai import OpenAI, AsyncOpenAI, APIError, AuthenticationError, RateLimitError
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()
client_async = AsyncOpenAI()

model ="chatgpt-4o-mini"
istruzioni = (
    "Sei un esperto teologo "
    "Rispondi con citazioni colte di Tommaso D'Acquino"
)

def callAi(text: str):
    try:
        res = client.responses.create(
            input=text,
            model=model,
            instructions=istruzioni
        )

        return res.output_text.strip().lower()
    
    except RateLimitError:
        return "RateLimitError"
    except AuthenticationError:
        return "AuthenticationError"
    except APIError as e:
        return f"APIError: {e}"
    


async def asyncCallAi(text: str):
    try:
        res = await client_async.responses.create(
            input=text,
            model=model,
            instructions=istruzioni
        )

        return res.output_text.strip().lower()
    
    except RateLimitError:
        return "RateLimitError"
    except AuthenticationError:
        return "AuthenticationError"
    except APIError as e:
        return f"APIError: {e}"