from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# User context（紀錄模式）
user_context = {}

# 角色圖片字典
character_images = {
  "原神": {
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
    "納西妲": "https://upload-os-bbs.hoyolab.com/upload/2023/06/26/248396204/96286609cb5cd4c507f1b438a4191c25_4194586395710844704.png"},
  "崩壞：星穹鐵道": {
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
    "Archer": "https://upload-os-bbs.hoyolab.com/upload/2025/07/01/248389735/48d6b1d28879b468f6721a994dd46874_3724605607459336321.jpg"},
  "絕區零": {
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
    "「扳機」": "https://upload-os-bbs.hoyolab.com/upload/2025/03/31/370699309/e4288113f121760254acc55dec278244_7842277090726115056.png"}}

# 版本活動資訊
activity_data = {
    "原神": {
        "月之三": "https://fastcdn.hoyoverse.com/mi18n/hk4e_global/m20251110hy2ebg1fy8/upload/c5864ab82c466958c72ec56529a63ffe_5873909476729017748.jpg",
        "next": None},
    "崩壞：星穹鐵道": {
        "3.7": "https://upload-os-bbs.hoyolab.com/upload/2025/11/04/248389732/0850ec1660cf3cb49ab4702b22af30cc_4548357368892651293.jpg",
        "3.8": "https://upload-os-bbs.hoyolab.com/upload/2025/12/07/248389732/23fc10410ba0bc077d367a8542fb9a30_4745388983360381307.jpg"},
    "絕區零": {
        "2.4": {"events": [
            "第一期調頻:琉音/雨果 11/26 - 12/17","第二期調頻:般岳/艾蓮 12/17 - 12/29",
            "全新放送 11/26 - 12/29","「嗯呢」從天降 12/17 - 12/29",
            "「嗯呢」棋俠傳 11/26 - 12/29","新黃金魔神戰士 11/28 - 12/29",
            "流光札記 12/3 - 12/29","擬境序列對決 12/8 - 12/29",
            "兔子小姐百分百 12/16 - 12/29","先遣賞金-區域巡防 12/11 - 12/16",
            "資料懸賞-實戰模擬 尚未公布時間"]},
        "next": None}}

# 遊戲副本攻略網址
dungeon_urls = {
    "原神": {
        "深境螺旋": {"url": "https://www.bilibili.com/video/BV1XMC1BdEZy/", "difficulty": "12層"},
        "幻想真境劇詩": {"url": "https://www.bilibili.com/video/BV1GDSzBxEEf/", "difficulty": "卓越、月諭"},
        "幽境危戰": {"url": "https://www.bilibili.com/video/BV1XMC1BdEZy/", "difficulty": "無畏"}},
    "崩壞：星穹鐵道": {
        "渾沌回憶": {"url": "https://www.bilibili.com/video/BV1LjmcB7EmH/", "difficulty": "其十二"},
        "虛構敘事": {"url": "https://www.bilibili.com/video/BV17GUTBMEWU/", "difficulty": "其四"},
        "末日幻影": {"url": "https://www.bilibili.com/video/BV1fNkRBdEuG/", "difficulty": "難度4"},
        "異相仲裁": {"url": "https://www.bilibili.com/video/BV1CV17BiE1A/", "difficulty": "騎士"}},
    "絕區零": {
        "式輿防衛戰": {"url": "https://www.bilibili.com/video/BV12q2LBKEFk/", "difficulty": "第七防線"},
        "危局強襲戰": {"url": "https://www.bilibili.com/video/BV1gbSVByEys/"}}}

def reply(msg):
    return {"fulfillmentMessages": [{"text": {"text": [msg]}}]}

def img_reply(msg, img_url):
    return {"fulfillmentMessages": [{"text": {"text": [msg]}},{"image": {"imageUri": img_url}}]}

# Dialogflow fulfillment webhook 主程式
@app.route("/callback", methods=["POST"])
def dialogflow_webhook():
    body = request.get_json(force=True)
    print("Webhook received:", json.dumps(body, ensure_ascii=False))
    text = body["queryResult"].get("queryText", "")
    params = body["queryResult"].get("parameters", {})
    session = body.get("session", "")
    user_id = session.split("/")[-1]

    # 角色培養攻略模式
    if text == "角色培養攻略":
        user_context[user_id] = "characterguide"
        return jsonify(reply("請輸入你想查詢的角色名稱(僅支援近期可抽取角色)"))
    # 版本活動資訊模式
    if text == "版本活動資訊":
        user_context[user_id] = "eventinformation"
        return jsonify(reply("請輸入你想查詢的遊戲版本"))
    # 週期副本攻略模式
    if text == "週期副本攻略":
        user_context[user_id] = "dungeonguide"
        return jsonify(reply("請輸入你想查詢的週期副本"))

    mode = user_context.get(user_id)

    # 使用者已進入角色培養攻略模式
    if mode == "characterguide":
        character=None
        params_name=["genshincharacter","hsrcharacter","zzzcharacter"]
        for name in params_name:
            character = params.get(name)
            if character:
                for game in character_images.keys():
                    img_url = character_images.get(game,{}).get(character)
                    if img_url:
                        break
                if img_url:
                    break
        if character:
            # 傳回文字+圖片
            return jsonify(img_reply(f"{character}的培養攻略：",img_url))
        else:
            character_list = []
            for game, characters in character_images.items():
                character_names = "、".join(characters.keys())
                character_list.append(f"{game} 角色：{character_names}")
            character_list="\n".join(character_list)
            return jsonify(reply(f"查無此角色，請重新輸入角色名稱\n目前支援角色如下：\n{character_list}"))
    
    # 使用者已進入版本活動資訊模式
    if mode == "eventinformation":
        user_game=None
        user_version=None
        # 取得使用者輸入
        user_game = params.get("game")                   # 遊戲
        user_version = str(params.get("gameversion"))    # 版本號
        # 補參數
        if user_game:
            game_data = activity_data[user_game]
            if not user_version:
                if "next" in game_data:
                    user_version = list(game_data.keys())[0]  #str
                else:
                    user_version = list(game_data.keys())  #list
        else:
            if user_version:
                for game in activity_data.keys():
                    game_data = activity_data[user_game]
                    if user_version in game_data.keys():
                        user_game=game
                        break
        #設定回傳內容
        if isinstance(user_version, str):
            data = activity_data.get(user_game, {}).get(user_version)
            # 根據遊戲回傳圖片或文字
            if user_game in ["原神", "崩壞：星穹鐵道"]:
                return jsonify(img_reply(f"{user_game}{user_version}版本活動資訊如下：",data))
            elif user_game == "絕區零" and "events" in data:
                activity_list = "\n".join(data["events"])
                return jsonify(reply(f"{user_game}{user_version}版本活動資訊如下：\n{activity_list}"))
        elif isinstance(user_version, list):
            # data是list表示有下個版本資訊
            now_ver = user_version[0]
            next_ver = user_version[1]
            return jsonify(reply(f"請問要查詢{now_ver}還是{next_ver}的版本活動資訊？"))
        else:
            version_list = []
            for game, game_data in activity_data.items():
                versions = list(game_data.keys())[0]
                if "next" not in game_data:
                    versions = ",".join(game_data.keys())
                version_list.append(f"{game} 版本：{versions}")
            version_list="\n".join(version_list)
            return jsonify(reply(f"查無此版本資訊，請重新輸入遊戲版本\n目前可查詢版本如下：\n{version_list}"))
    
    # 使用者已進入週期副本攻略模式
    if mode == "dungeonguide":
        user_game=None
        user_dungeon=None
        # 取得使用者輸入
        user_game = params.get("game")        # 遊戲
        user_dungeon = params.get("dungeon")  # 副本
        # 補參數
        if not user_game:
            if user_dungeon:
                for game in dungeon_urls.keys():
                    game_data = dungeon_urls[game]
                    if user_dungeon in game_data.keys():
                        user_game=game
                        break
        data = dungeon_urls.get(user_game,{}).get(user_dungeon)
        if data:
            url = data["url"]
            difficulty = data.get("difficulty")
            if difficulty:
                video_url = f"難度：{difficulty}\n攻略：{url}"
            else:
                video_url = f"攻略：{url}"
            return jsonify(reply(f"{user_game}{user_dungeon}副本攻略如下：\n{video_url}"))
        else:
            # 列出可查詢副本
            if not user_game:
                dungeon_list=[]
                for game in dungeon_urls.keys():
                    dungeons = "、".join(dungeon_urls[game].keys())
                    dungeon_list.append(f"{game} 副本：{dungeons}")
                dungeon_list="\n".join(dungeon_list)
                return jsonify(reply(f"查無副本，可查詢的副本有：{dungeon_list}"))
            else:
                dungeon_list = "、".join(dungeon_urls[user_game].keys())
                return jsonify(reply(f"{user_game}可查詢的副本有：{dungeon_list}"))
            
    # 預設回覆
    hint_dict = {
    "characterguide": "請輸入角色名稱查詢培養攻略。",
    "eventinformation": "請輸入遊戲版本查詢活動資訊。",
    "dungeonguide": "請輸入遊戲副本查詢攻略網址。"}
    hint = hint_dict.get(mode, "請點選功能選單開始查詢。")
    return jsonify(reply(f"抱歉，我不明白「{text}」的意思。\n{hint}"))
