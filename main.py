from flask import Flask, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1500100111571751024/fd3czVzGvYqk4kr697pzkAg5avsqQexfqZZaqrjvlXrLjGtl7irCQ_4qynqbrnqeva5k"

MENTION_USERS = [531729236491239424]

def send_discord_alert(user_id, message):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mentions = " ".join([f"<@{uid}>" for uid in MENTION_USERS])
    payload = {
        "content": mentions,
        "embeds": [
            {
                "title": "📩 카카오 채널 새 메시지",
                "color": 0xFEE500,
                "fields": [
                    {"name": "👤 사용자 ID", "value": f"`{user_id}`", "inline": True},
                    {"name": "🕐 시간", "value": now, "inline": True},
                    {"name": "💬 메시지", "value": message, "inline": False},
                ],
                "footer": {"text": "카카오 상담톡 알림"}
            }
        ]
    }
    requests.post(DISCORD_WEBHOOK_URL, json=payload)

@app.route("/skill", methods=["POST"])
def skill():
    data = request.get_json(silent=True) or {}

    user_request = data.get("userRequest", {})
    message = user_request.get("utterance", "(내용 없음)")
    user_id = user_request.get("user", {}).get("id", "알 수 없음")

    send_discord_alert(user_id, message)

    # 카카오 오픈빌더 필수 응답 형식 (고객에게 메시지 미전송)
    return jsonify({
        "version": "2.0",
        "template": {
            "outputs": []
        }
    })

@app.route("/health", methods=["GET"])
def health():
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
