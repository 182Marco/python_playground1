from dotenv import load_dotenv
from openai import OpenAI, AuthenticationError, RateLimitError, APIError

load_dotenv()
client = OpenAI()

modello = "gpt-4o-mini"


risposta = client.responses.create(
    model= modello,
    input="Ciao, raccontami la storia degli LLM",
    stream= True
)

print("streaming: ")

for evento in risposta:
    if evento.type == "response.output_text.delta":
        print(evento.delta, end="", flush=True) # end è per non andare a capo ogni tocken / flush evita di accumulare cose