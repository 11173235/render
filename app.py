from flask import Flask, request, jsonify

app = Flask(__name__)

charImages = {
    "奈芙爾": "https://upload-os-bbs.hoyolab.com/upload/2025/10/22/248396204/03efcd616004083b56f1236291a8168c_1765848458562635549.jpg",
    "菲林斯": "https://upload-os-bbs.hoyolab.com/upload/2025/09/29/248396204/86565129968b752c57f54294a09f2274_8369161948052686452.jpg",
}

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    print(data)
    character = data["queryResult"]["parameters"].get("GenshinCharacter")  # 從你的聊天機器人接收角色名
    image_url = charImages.get(character, "")
    if character in charImages:
        image_url = charImages[character]
        text_reply = f"{character} 的培養攻略"
    return jsonify({
        "fulfillmentText": text_reply,
        "fulfillmentMessages": [{"text": {"text": [text_reply]}},{"image": {"imageurl": image_url}}]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
