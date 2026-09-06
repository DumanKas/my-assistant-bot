from config import OPENROUTER_API_KEY
import httpx
import asyncio
from sentence_transformers import SentenceTransformer
async def ask_gemini2(messages: list, max_retries: int = 3,base = 1):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}",
               "Content-Type": "application/json"}
    payload = {
        "model": "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
        "messages": messages
    }
    async with httpx.AsyncClient() as client:
        for attempt in range(max_retries):
            try:
                response = await client.post(url, headers=headers, json=payload, timeout=30)
                if response.status_code >= 500 or response.status_code == 429:
                    wait = base * (2 ** attempt)
                    await asyncio.sleep(wait)
                    continue
                data = response.json()
                if "error" in data:
                    return f"Ошибка: {data['error']['message']}"
                return data["choices"][0]["message"]["content"]
            except httpx.TimeoutException:
                if attempt == max_retries - 1:
                    return f"Не удалось получить ответ, сервер долго не отвечает. Попробуйте позже"
                wait = base * (2 ** attempt)
                await asyncio.sleep(wait)
                continue
            except httpx.RequestError:
                if attempt == max_retries - 1:
                    return f"Сетевые проблемы. Не получается получить ответ от ИИ. Попробуйте позже"
                wait = base * (2 ** attempt)
                await asyncio.sleep(wait)
                continue

        return "Большое количество попыток, попробуйте позже "