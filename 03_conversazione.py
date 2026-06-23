from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

modello = "gpt-4o-mini"


print("\n Senza contesto:")

noContentRisposta = client.responses.create(
    model = modello,
    input="spiegamela",
)

print(f"\n Con contesto: {noContentRisposta.output_text}")

msgs=[
    { "role": "user", "content": "raccontami una barzelletta" },
    { "role": "assistant", "content": "Perchè il libro di matematica è triste? perchè ha troppi problemi" }, 
    { "role": "user", "content": "spiegamela" },
]

risposta = client.responses.create(
    model = modello,
    input=msgs,
)

print(risposta.output_text)
