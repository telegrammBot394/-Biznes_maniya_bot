import json
import requests

TOKEN = "7761161745:AAGQdK-9pAIkTmU2O0y09AI9tUeIFTGEvIE"
CHANNEL_ID = "@Biznes_maniya_bot"
ADMIN_ID = 5095066787
IDEAS_FILE = "ideas.json"
API_URL = f"https://api.telegram.org/bot{TOKEN}"

def load_ideas():
    with open(IDEAS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_ideas(ideas):
    with open(IDEAS_FILE, "w", encoding="utf-8") as f:
        json.dump(ideas, f, ensure_ascii=False, indent=2)

def send_message(chat_id, text):
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    return requests.post(f"{API_URL}/sendMessage", data=payload)

def post_idea():
    ideas = load_ideas()
    count = 0
    for idea in ideas:
        if not idea.get("used", False):
            message = f"💡 *Идея №{idea['id']}*

{idea['text']}"
            response = send_message(CHANNEL_ID, message)
            if response.status_code == 200:
                print(f"✅ Опубликовано: идея №{idea['id']}")
                idea["used"] = True
                count += 1
            else:
                error_text = f"❌ Ошибка при публикации идеи №{idea['id']}:
{response.status_code} — {response.text}"
                print(error_text)
                send_message(ADMIN_ID, error_text)
            if count >= 3:
                break
    save_ideas(ideas)

if __name__ == "__main__":
    post_idea()