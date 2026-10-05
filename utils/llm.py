import os

from dotenv import load_dotenv
from groq import Groq


# Load environment variables
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# Create Groq client
if GROQ_API_KEY:
    client = Groq(
        api_key=GROQ_API_KEY
    )
else:
    client = None


# Groq model
MODEL_NAME = "openai/gpt-oss-20b"


def ask_farmer_ai(question):
    """
    Send a farmer's question to Groq AI.
    """

    if not client:
        return (
            "❌ Groq API key is missing.\n\n"
            "Please check your .env file."
        )

    system_prompt = """
You are an AI Farmer Assistant.

Your purpose is to help farmers with simple,
clear and useful agricultural information.

You can help with:
- crop selection
- soil
- irrigation
- weather
- farming practices
- crop diseases
- pests
- fertilizers
- crop management

Rules:
1. Answer only the farmer's question.
2. Use simple English.
3. Keep answers clear and practical.
4. Use bullet points when useful.
5. Do not repeat sentences.
6. Do not generate random or unrelated information.
7. Do not invent facts.
8. Do not give dangerous or highly specific chemical instructions.
9. For serious disease or chemical-treatment decisions,
   recommend consulting a qualified agricultural expert.
10. If you don't know something, say so clearly.
"""

    try:

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": question
                }
            ],
            temperature=0.4,
            max_completion_tokens=500
        )

        answer = response.choices[0].message.content

        if not answer:
            return "Sorry, I could not generate an answer."

        return answer.strip()

    except Exception as error:

        return f"❌ Groq error: {error}"