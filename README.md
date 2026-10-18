# AI Assistant Telegram Bot 🤖

A smart Telegram bot integrated with Large Language Models (LLMs) for intelligent conversations, note-taking, and task management.

## 🚀 Features
*   **LLM Integration:** Powered by OpenRouter API for advanced AI responses.
*   **Context Awareness:** Stores dialogue history so the bot remembers the context of the conversation.
*   **Note-taking System:** Users can save and retrieve personal notes directly through the bot.
*   **State Management:** Uses FSM (Finite State Machine) via `aiogram` for smooth multi-step user interactions.

## 🛠 Tech Stack
*   **Language:** Python 3.10+
*   **Framework:** aiogram 3 (Asynchronous Telegram Bot API)
*   **AI Integration:** OpenRouter API (LLM)
*   **State Management:** FSM (MemoryStorage / Database)

## ⚙️ How to run locally
1. Clone the repository:
   `git clone https://github.com/DumanKas/my-assistant-bot.git`
2. Install dependencies:
   `pip install -r requirements.txt`
3. Create a `.env` file and add your tokens:
   `BOT_TOKEN=your_telegram_token`
   `OPENROUTER_API_KEY=your_api_key`
4. Run the bot:
   `python main.py`

---
*Developed by [Duman Kasymkul](https://github.com/DumanKas)*
