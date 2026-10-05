import os
import base64

from dotenv import load_dotenv
from groq import Groq


load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if GROQ_API_KEY:
    client = Groq(api_key=GROQ_API_KEY)
else:
    client = None


VISION_MODEL = "qwen/qwen3.8-27b"


def analyze_plant_image(image_file):

    if not client:
        return (
            "❌ Groq API key is missing. "
            "Please check your .env file."
        )

    try:

        image_bytes = image_file.getvalue()

        base64_image = base64.b64encode(
            image_bytes
        ).decode("utf-8")

        image_type = image_file.type

        prompt = """
You are an AI Farmer Assistant.

Analyze the uploaded plant or leaf image.

Give the answer in this format:

🦠 Possible Disease / Problem:
Give the most likely disease or plant-health problem.

🔍 What I Observe:
Describe the visible symptoms.

🌱 Possible Causes:
Give general possible causes.

💡 Suggestions:
Give safe, general suggestions.

🛡️ Prevention:
Give general prevention practices.

⚠️ Important Note:
Mention that image-based identification is not
a definitive diagnosis and that an agricultural
expert should be consulted for serious problems.

Rules:
- If the image is unclear, say that the result is uncertain.
- Do not invent a disease.
- Use simple English.
- Do not give dangerous or highly specific chemical instructions.
- Keep the answer useful for farmers.
"""

        response = client.chat.completions.create(
            model=VISION_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": (
                                    f"data:{image_type};"
                                    f"base64,{base64_image}"
                                )
                            }
                        }
                    ]
                }
            ],
            temperature=0.3,
            max_completion_tokens=700
        )

        answer = response.choices[0].message.content

        if not answer:
            return "❌ AI could not analyze the image."

        return answer.strip()

    except Exception as error:

        return f"❌ Image analysis error: {error}"