from config import OPENROUTER_API_KEY
import httpx

async def ask_gemini2(messages: list):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers= {
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json",
                },
                json = {
                    "model": "google/gemma-4-31b-it:free", "messages": messages
                },
                timeout = 30
            )
            data = response.json()
            print(data)
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"Ошибка {e}")