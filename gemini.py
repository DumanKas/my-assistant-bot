from config import OPENROUTER_API_KEY
import httpx

async def ask_gemini2(messages: list):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "inclusionai/ling-2.6-flash-20260421:free",
                    "messages": messages
                },
                timeout=30
            )
            data = response.json()
            if "error" in data:
                return f"Ошибка: {data['error']['message']}"
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            return f"Ошибка: {e}"