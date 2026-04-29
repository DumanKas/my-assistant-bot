from config import GEMINI_API_KEY
import httpx


async def ask_gemini2(messages: list):

    user_text = messages[-1]['content']

    async with httpx.AsyncClient() as client:
        try:

            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

            response = await client.post(
                url,
                headers={"Content-Type": "application/json"},
                json={
                    "contents": [{"parts": [{"text": user_text}]}]
                },
                timeout=30
            )
            data = response.json()

            if "error" in data:
                print(f"Ошибка Google API: {data['error']['message']}")
                return "Извини, произошла техническая ошибка на стороне Google."


            return data['candidates'][0]['content']['parts'][0]['text']

        except Exception as e:
            print(f"Ошибка запроса: {e}")
            return "Не удалось связаться с ИИ."