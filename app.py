from flask import Flask, request, jsonify
from google.oauth2 import service_account
import google.auth.transport.requests
import requests
import json
import os

app = Flask(__name__)

dialogflow_project_ID = "gameguide-w9ep"

# User context（紀錄模式）
user_context = {}

# 角色圖片字典
CHARACTER_IMAGES = {
    # ---- 原神 ----
    "杜林": "https://upload-os-bbs.hoyolab.com/upload/2025/12/03/248396204/0f4481279430a17e7df8546973f1bf45_1737055575909256174.jpg",
    "溫迪": "https://upload-os-bbs.hoyolab.com/upload/2023/09/16/248396282/d3c070cfea1cb91251921e52cc439e49_1631429753459849743.png",
    "雅珂達": "https://upload-os-bbs.hoyolab.com/upload/2025/12/03/248396204/0e9958023b33fcb34348d67103b1038a_1297440543828697616.jpg",
    "阿蕾奇諾": "https://upload-os-bbs.hoyolab.com/upload/2025/10/20/248396204/abfac41f0e4f604a01e36f7bd16a2cbd_2557934871374952669.jpg",
    "鍾離": "https://upload-os-bbs.hoyolab.com/upload/2023/05/17/248396204/18079dc0916553c1a6d6c56cc6384288_6032047032970909430.png",
    "奈芙爾": "https://upload-os-bbs.hoyolab.com/upload/2025/10/22/248396204/03efcd616004083b56f1236291a8168c_1765848458562635549.jpg",
    "芙寧娜": "https://upload-os-bbs.hoyolab.com/upload/2023/11/07/248396204/af48adb667fc252c7c19e78ae85a845e_2649553244189510984.png",
    "菲林斯": "https://upload-os-bbs.hoyolab.com/upload/2025/09/29/248396204/86565129968b752c57f54294a09f2274_8369161948052686452.jpg",
    "夜蘭": "https://upload-os-bbs.hoyolab.com/upload/2023/08/05/248396204/bf81220dce8368521e1f0c3c250ad447_1269170865623546364.png",
    "愛諾": "https://upload-os-bbs.hoyolab.com/upload/2025/09/10/248396204/d6dd3276c1e343e7556d4d8f292bcf64_2312607690677255983.jpg",
    "菈烏瑪": "https://upload-os-bbs.hoyolab.com/upload/2025/09/09/248396204/64021a3545318c8239fbe169207deee5_598967942769683403.jpg",
    "納西妲": "https://upload-os-bbs.hoyolab.com/upload/2023/06/26/248396204/96286609cb5cd4c507f1b438a4191c25_4194586395710844704.png",

    # ---- 星穹鐵道 ----
    "昔漣": "https://upload-os-bbs.hoyolab.com/upload/2025/11/04/248389735/475ff0615308b02decc6120a9c656695_4483968931015795177.jpg",
    "白厄": "https://upload-os-bbs.hoyolab.com/upload/2025/10/24/248389735/e9618ffc07facc57f433731ac474a966_491074884864979226.jpg",
    "賽飛兒": "https://upload-os-bbs.hoyolab.com/upload/2025/10/24/248389735/b394826ff48f7ccb07c60a810d0c3737_4024594253916700110.jpg",
    "萬敵": "https://upload-os-bbs.hoyolab.com/upload/2025/10/24/248389735/a22bf3613043b594706649b38ae144a0_6624641749719964122.jpg",
    "風菫": "https://upload-os-bbs.hoyolab.com/upload/2025/10/24/248389735/5041aa9b837b509c70c24f4dc210cbee_7694529708168387109.jpg",
    "遐蝶": "https://upload-os-bbs.hoyolab.com/upload/2025/10/24/248389735/d150d7f196dfdc8a05532573472b3a1a_8724397418293741727.jpg",
    "緹寶": "https://upload-os-bbs.hoyolab.com/upload/2025/10/24/248389735/f1ebb2d07777865ee59c172926a6058f_5788540008426415265.jpg",
    "丹恆•騰荒": "https://upload-os-bbs.hoyolab.com/upload/2025/10/14/248389735/3c4285d3dcef07e56c67d6e4f166d8b8_1173165742150616443.jpg",
    "那刻夏": "https://upload-os-bbs.hoyolab.com/upload/2025/09/14/248389735/2b9a6a9098e07e15809cea94e66189c1_8280043820105748653.jpg",
    "長夜月": "https://upload-os-bbs.hoyolab.com/upload/2025/09/22/248389735/a6a2216640c13108cf8ea5856781f332_1091069923873400384.jpg",
    "大黑塔": "https://upload-os-bbs.hoyolab.com/upload/2025/09/14/248389735/af0105189c217a22e16c178175ab2cce_6632122516925690103.jpg",
    "Saber": "https://upload-os-bbs.hoyolab.com/upload/2025/07/01/248389735/da1ce3c7208a8b26806143cdf6c662df_8358127939087283967.jpg",
    "Archer": "https://upload-os-bbs.hoyolab.com/upload/2025/07/01/248389735/48d6b1d28879b468f6721a994dd46874_3724605607459336321.jpg",

    # ---- 絕區零 ----
    "琉音": "https://upload-os-bbs.hoyolab.com/upload/2025/11/23/370699309/47a8f937769f28acbc2302052248a2e7_7167502227653853082.jpg",
    "雨果": "https://upload-os-bbs.hoyolab.com/upload/2025/05/08/370699309/f1c08028a356a2f9257999a33fa993de_268115483364083532.jpg",
    "伊德海莉": "https://upload-os-bbs.hoyolab.com/upload/2025/11/02/370699309/bc33cc231634cab44b360cb3bb4a750d_2180040413477663816.jpg",
    "橘福福": "https://upload-os-bbs.hoyolab.com/upload/2025/06/21/370699309/2418321b740d3001da2e3fa5ee148dec_8547786973576138117.jpg",
    "盧西婭": "https://upload-os-bbs.hoyolab.com/upload/2025/10/13/370699309/ac624e72c2be90541f664df339b0e349_1059825127900072960.jpg",
    "薇薇安": "https://upload-os-bbs.hoyolab.com/upload/2025/04/19/370699309/76975dcee9c115ea34ef8b69c7f713c9_8431175033744336911.png",
    "狛野真斗": "https://upload-os-bbs.hoyolab.com/upload/2025/10/13/370699309/fa0a1299e74b53f64f5d18bfaf604b26_4848228649664302985.jpg",
    "奧菲絲•馬格努森&「鬼火」": "https://upload-os-bbs.hoyolab.com/upload/2025/09/22/370699309/2221f1afd6080ce6dc4b90d97030d4ca_6158325346300109334.jpg",
    "伊芙琳": "https://upload-os-bbs.hoyolab.com/upload/2025/02/11/370699309/5469e4ac5bbbe07578c35cb8f112817c_6769450492245556957.png",
    "「席德」": "https://upload-os-bbs.hoyolab.com/upload/2025/09/02/370699309/29e9eb5ba9edeeaccb1fe88c943830bc_4293272389443311205.jpg",
    "「扳機」": "https://upload-os-bbs.hoyolab.com/upload/2025/03/31/370699309/e4288113f121760254acc55dec278244_7842277090726115056.png",}

# 遊戲版本日曆圖/文
ACTIVITY_DATA = {
    "原神 月之二": {"type": "image","url": "https://fastcdn.hoyoverse.com/mi18n/hk4e_global/m20251110hy2ebg1fy8/upload/c5864ab82c466958c72ec56529a63ffe_5873909476729017748.jpg"},
    "崩壞：星穹鐵道 3.7": {"type": "image","url": "https://upload-os-bbs.hoyolab.com/upload/2025/11/04/248389732/0850ec1660cf3cb49ab4702b22af30cc_4548357368892651293.jpg"},
    "崩壞：星穹鐵道 3.8": {"type": "image","url": "https://upload-os-bbs.hoyolab.com/upload/2025/12/07/248389732/23fc10410ba0bc077d367a8542fb9a30_4745388983360381307.jpg"},
    "絕區零 2.4": {"type": "text",
        "events": [
            {"name": "第一期調頻:琉音/雨果", "time": "11/26 - 12/17"},
            {"name": "第二期調頻:般岳/艾蓮", "time": "12/17 - 12/29"},
            {"name": "全新放送", "time": "11/26 - 12/29"},
            {"name": "「嗯呢」從天降", "time": "12/17 - 12/29"},
            {"name": "「嗯呢」棋俠傳", "time": "11/26 - 12/29"},
            {"name": "新黃金魔神戰士", "time": "11/28 - 12/29"},
            {"name": "流光札記", "time": "12/3 - 12/29"},
            {"name": "擬境序列對決", "time": "12/8 - 12/29"},
            {"name": "兔子小姐百分百", "time": "12/16 - 12/29"},
            {"name": "先遣賞金-區域巡防", "time": "12/11 - 12/16"},
            {"name": "資料懸賞-實戰模擬", "time": "尚未公布"}]}}

# 從 webhook 判斷角色名稱
def match_character_from_webhook(body):
    params = body["queryResult"].get("parameters", {})
    for e in ["genshincharacter", "starrailcharacter", "zzzcharacter"]:
        if params.get(e):
            return params[e]
    return None

# FLEX版本選單
def flex_choose_version():
    flex = {
        "type": "flex","altText": "請選擇遊戲版本活動更新資訊",
        "contents": {"type": "bubble","size": "mega",
            "header": {"type": "box","layout": "vertical",
                "contents": [{"type": "text","text": "活動更新資訊","weight": "bold","size": "xl","color": "#ffffff"}],
                "backgroundColor": "#5A8DEE","paddingAll": "20px"},
            "body": {"type": "box","layout": "vertical","spacing": "12px",
                "contents": [
                    {"type": "button","style": "secondary","color": "#F2F2F2",
                        "action": {"type": "message","label": "原神 月之三","text": "原神 月之三"}},
                    {"type": "button","style": "secondary","color": "#F2F2F2",
                        "action": {"type": "message","label": "崩壞：星穹鐵道 3.7","text": "崩壞：星穹鐵道 3.7"}},
                    {"type": "button","style": "secondary","color": "#F2F2F2",
                        "action": {"type": "message","label": "崩壞：星穹鐵道 3.8","text": "崩壞：星穹鐵道 3.8"}},
                    {"type": "button","style": "secondary","color": "#F2F2F2",
                        "action": {"type": "message","label": "絕區零 2.4","text": "絕區零 2.4"}}]}}}
    return flex

# Dialogflow fulfillment webhook 主程式
@app.route("/callback", methods=["POST"])
def dialogflow_webhook():
    body = request.get_json(force=True)
    print("Webhook received:", json.dumps(body, ensure_ascii=False))

    text = body["queryResult"].get("queryText", "")
    session = body.get("session", "")
    user_id = session.split("/")[-1]

    # 進入角色攻略模式
    if text == "角色培養攻略":
        user_context[user_id] = "characterguide"
        return jsonify({"fulfillmentText": "請輸入你想查詢的角色名稱"})

    # 使用者正在角色查詢模式
    if user_context.get(user_id) == "characterguide":
        character = match_character_from_webhook(body)
        if not character:
            return jsonify({"fulfillmentText": "查無此角色，請重新輸入角色名稱"})

        img_url = CHARACTER_IMAGES.get(character)
        if img_url:
            # 傳回文字+圖片
            return jsonify({
                "fulfillmentMessages": [
                    {"text": {"text": [f"{character} 的培養攻略："]}},
                    {"image": {"imageUri": img_url}}]})
    
    # 活動更新資訊模式
    if text == "活動更新資訊":
        user_context[user_id] = "eventupdates"
        return flex_choose_version()

        # 活動更新資訊選單 → 判斷版本文字
        if text in ACTIVITY_DATA:
            data = ACTIVITY_DATA[text]
    
            # 有活動日曆圖（原神/崩鐵）
            if data["type"] == "image":
                return jsonify({
                    "fulfillmentMessages": [
                        {"text": {"text": [f"{text} 活動日曆："]}},
                        {"image": {"imageUri": data["url"]}}]})
    
            # 純文字活動資訊（絕區零）
            elif data["type"] == "text":
                event_lines = [f"{e['name']}（{e['time']}）" for e in data["events"]]
                final_text = text + " 已公開活動：\n" + "\n".join(event_lines)
    
                return jsonify({
                    "fulfillmentMessages": [
                        {"text": {"text": [final_text]}}]})


    # 預設回覆
    return jsonify({"fulfillmentText": f"收到：{text}"})

# 啟動 server
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
