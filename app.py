from flask import Flask, request, jsonify
from linebot import LineBotApi
from linebot.models import ImageSendMessage, TextSendMessage
import requests

app = Flask(__name__)

LINE_CHANNEL_ACCESS_TOKEN = "你的ChannelAccessToken"
LINE_CHANNEL_SECRET = "你的ChannelSecret"
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)

# 簡單 session context 記錄使用者模式
user_context = {}

@app.route("/webhook", methods=['POST'])
def webhook():
    req = request.get_json()
    event = req.get("originalDetectIntentRequest", {}).get("payload", {})
    reply_token = event.get("replyToken")
    user_id = event.get("source", {}).get("userId")

    # 1️⃣ 處理 Rich Menu Postback，進入「角色培養攻略模式」
    if event.get("type") == "postback":
        data = event["postback"]["data"]  # e.g., "mode=character_build"
        if "character_build" in data:
            user_context[user_id] = "character_build"
            line_bot_api.reply_message(
                reply_token,
                TextSendMessage(text="已切換到角色培養攻略模式，請輸入角色名字。"))
            return jsonify({}), 200

    # 2️⃣ 處理文字訊息
    elif event.get("type") == "message" and event["message"]["type"] == "text":
        user_text = event["message"]["text"].lower()

        # 只在角色培養攻略模式才處理名字查詢
        if user_context.get(user_id) == "character_build":
            # 從 Dialogflow 取得三個 entity
            params = req["queryResult"]["parameters"]
            genshin_name = params.get("genshincharacter")
            starrail_name = params.get("starrailcharacter")
            zzz_name = params.get("zzzcharacter")

            # 依序取第一個有值的角色名字
            character_name = genshin_name or starrail_name or zzz_name

            if character_name:
                # 假設 Render API 可以回傳培養攻略圖片 URL
                img_url = f"https://render-server.com/build/{character_name}.png"
                line_bot_api.reply_message(
                    reply_token,
                    ImageSendMessage(original_content_url=img_url,
                                     preview_image_url=img_url))
            else:
                # 三個 entity 都沒找到
                line_bot_api.reply_message(
                    reply_token,
                    TextSendMessage(text="找不到角色，請確認名字或使用中文/英文別名。"))
        else:
            # 非角色培養攻略模式，可給一般回覆
            line_bot_api.reply_message(
                reply_token,
                TextSendMessage(text="請先從選單選擇要查詢的模式。"))

    return jsonify({}), 200

if __name__ == "__main__":
    app.run(port=5000)
