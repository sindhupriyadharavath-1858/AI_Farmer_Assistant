import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

print("API key loaded:", bool(api_key))

if not api_key:
    print("❌ GROQ_API_KEY is missing from .env")
    exit()

client = Groq(
    api_key=api_key
)

response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {
            "role": "user",
            "content": "Answer in one sentence: What is crop rotation?"
        }
    ],
    temperature=0.4,
    max_completion_tokens=200
)

print("\nAI Response:")
print(response.choices[0].message.content)