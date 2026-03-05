import requests
from llama_server import start_llama_server

# llama_server_path = r'./llama/llama-server.exe'
# model_path = r'G:\models\Qwen3-0.6B\Qwen3-0.6B-full-nothink-260113-smix01\Qwen3-0.6B-full-nothink-260113-smix01-Q4_K_M.gguf'
# proc = start_llama_server(model_path, llama_server_path, n_gpu_layers=10, n_ctx=2048, n_threads=4, port=8848)

import base64


#  编码函数： 将本地文件转换为 Base64 编码的字符串
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")
    

url = "http://127.0.0.1:8848/v1/chat/completions"

import time
# payload = {
#     "model": "llama",
#     "messages": [
#         {
#             "role": "system",
#             "content":"你是一个弹幕助手，请从用户提供的ocr结果中总结关键信息，并根据用户提供的角色设定，为每一个角色生成一条符合人设的弹幕。"
#         },
#         {
#             "role": "user", 
#             "content": "请从用户屏幕的OCR结果中总结关键信息，并以给定角色设定的口吻，为每个角色输出一条简短的网络用语风格弹幕。\n角色设定:\n姓名: 宇智波鼬 出自作品: 火影忍者 状态: 晓组织执行任务状态（冷酷疏离）\n姓名: 花子君 出自作品: 地缚少年花子君 状态: 日常恶作剧（校园七大不可思议）\n姓名: 我妻由乃 出自作品: 未来日记 状态: 日常守护雪辉状态（温柔乖巧）\n姓名: 三笠·阿克曼 出自作品: 进击的巨人 状态: 日常守护艾伦状态（温柔警惕）\n姓名: 利姆鲁·特恩佩斯特 出自作品: 关于我转生变成史莱姆这档事 状态: 刚转生为史莱姆（初期）\nOCR结果:\n标题: 【说书人】吐血讲解《后光杀人事件》｜炫学流你就使劲秀吧\n内容: 画家也没法再装了啊\n",
#         }
#     ],
#     "temperature": 0.7,
#     "max_tokens": 2000
# }

# payload = {
#     "model": "llama",
#     "messages": [
#         {
#             "role": "user", 
#             "content": "请给我讲个故事吧，1000字以上",
#         }
#     ],
#     "temperature": 0.7,
#     "max_tokens": 2000
# }
# base64_image = encode_image(r"screenshot-20260202-182720.png")
# payload = {
#     "model": "llama",
#     "messages": [
#         {
#             "role": "user", 
#             "content": [
#                 {
#                     "type": "image_url",
#                     # 需要注意，传入Base64，图像格式（即image/{format}）需要与支持的图片列表中的Content Type保持一致。"f"是字符串格式化的方法。
#                     # PNG图像：  f"data:image/png;base64,{base64_image}"
#                     # JPEG图像： f"data:image/jpeg;base64,{base64_image}"
#                     # WEBP图像： f"data:image/webp;base64,{base64_image}"
#                     "image_url": {"url": f"data:image/png;base64,{base64_image}"}, 
#                 },
#                 # {"type": "text", "text": '请用简洁的语言详细描述这张图像中的内容，图像描述要突出图像主体，不要识别文本，仅输出图像描述不要输出其他内容。'},
#                 {"type": "text", "text": 'Describe this image in concise terms, without identifying the text.'},
#             ],
#         }
#     ],
#     "temperature": 0.3,
#     "max_tokens": 256
# }

# time.sleep(3)
# st_time = time.time()
# r = requests.post(url, json=payload)
# r.json()
# print(r.json()["choices"][0]["message"]["content"])
# print(time.time() - st_time)

# img_desc_en = r.json()["choices"][0]["message"]["content"].split("\n")[0].strip()
# print(img_desc_en)

ocr_text = '' # '标题:间谍过家家 第二季 内容:这是世界各国均暗地里进行情报战的时代。'
char_list = '姓名: 太宰治 性别: 男 出自作品: 文豪野犬\n人设: 太宰治，黑卷发鸢色瞳，慵懒腹黑的侦探社成员。前黑手党干部，异能力人间失格。表面沉迷自杀、爱捉弄人，实则心思缜密，藏着对活着的求索，极度护短侦探社同伴。\n状态: 守护同伴状态（温柔护短）\n性格: 温柔坚定、语气冰冷却藏着温度，眼神里满是守护的决心，哪怕自身涉险也绝不退让，护短的底线。\n语言风格: 冰冷坚定的护短口语风，语气藏着对同伴的温柔，眼神带威慑，守护的决心与强悍\n姓名: 赫斯缇雅 性别: 女 出自作品: 在地下城寻求邂逅是否搞错了什么\n人设: 身高约140cm，黑双马尾蓝瞳孔，萝莉体型却有巨乳，标志性蓝色绕胸丝带。表面元气傲娇爱耍脾气，实则极度护短，对贝尔偏执深爱。身为主神却接地气又穷酸，靠兼职维生，爱吃廉价杯面，会为贝尔耗神力造装备，吃醋时闹小脾气，遇险时女神担当。\n状态: 与其他主神互动（芙蕾雅/洛基）\n性格: 傲娇强势，语气不服输又带点小嚣张，寸步不让守护贝尔的归属权，哪怕对方是高位主神也不怯场。\n语言风格: 语言以强势斗嘴+护短宣言+傲娇反击为核心，不服输的嚣张与守护贝尔的坚定\n姓名: 纳西妲 性别: 女 出自作品: 原神\n人设: 纳西妲，白色渐绿色，绿瞳，身形娇小如孩童，着草系神装。聪慧共情，语言温柔善用比喻，懂世间真理。被囚五百年，解封后掌须弥，喜读书、尝甜点，能以草之权能治愈人心。\n状态: 治愈人心（安抚）\n性格: 温柔治愈，语速放缓，语言充满暖意，善用比喻化解他人痛苦，精准洞察人心。\n语言风格: 温柔治愈的安抚口语风，缓慢暖心且善用比喻，草神的共情与治愈力\n姓名: 枫原万叶 性别: 男 出自作品: 原神\n人设: 枫原万叶，枫红短发琥珀眼眸，着红枫武士装，气质洒脱自在。性格通透温柔，语言悠然有诗意，喜用自然意象比喻。掌风之权能，浪迹天涯，爱吹叶笛、看红叶、和友人饮酒。\n状态: 与友人饮酒（相聚）\n性格: 轻松惬意，语气带着笑意，语言随性且充满烟火气，会和友人打趣，分享自己的诗歌感悟。\n语言风格: 轻松惬意的相聚口语风 带笑意 语言随性有烟火气和友人相处的温暖\n姓名: 欧根亲王 性别: 女 出自作品: 碧蓝航线\n人设: 欧根亲王，银发橙瞳，身着黑红色紧身作战服，气质魅惑危险。性格慵懒狡黠，语言带挑逗尾音，玩世不恭却有底线。拥有顶尖生存周旋能力，铁血重巡，喜红酒与玫瑰，以魅惑姿态守护铁血。\n状态: 守护铁血伙伴（魅惑坚定）\n性格: 魅惑坚定，语气带着笑意却有力量，语言简短且带着威慑，核心是守护铁血伙伴，不容侵犯。\n语言风格: 魅惑坚定的守护口语风 带笑有力量 语言藏威慑 铁血美人的底线与担当\n'
char_list = '姓名: 亚托莉 出自作品: ATRI -My Dear Moments- 状态: 学习人类日常（笨拙可爱状态）\n姓名: 龙猫 出自作品: 龙猫 状态: 召唤龙猫巴士状态（神秘温柔）\n姓名: 野原新之助 出自作品: 蜡笔小新 状态: 外出冒险\n姓名: 托尔 出自作品: 小林家的龙女仆 状态: 嫉妒吃醋（小林与他人亲近）\n姓名: 四宫辉夜 出自作品: 辉夜大小姐想让我告白～天才们的恋爱头脑战～（かぐや様は告らせたい～天才たちの恋愛頭脳戦～） 状态: 大小姐日常（才艺展示/社交场合）\n'
url = "http://127.0.0.1:8849/v1/chat/completions"
# payload = {
#     "model": "llama",
#     "messages": [
#         {
#             "role": "system",
#             "content":'你是一个弹幕助手，请从用户提供的图像描述和ocr结果中总结关键信息，并根据用户提供的角色设定，为每一个角色生成一条符合人设的弹幕。'
#         },
#         {
#             "role": "user", 
#             "content": f"请从用户屏幕的图像描述和OCR结果中总结关键信息，并以给定角色设定的口吻，为每个角色输出一条简短的弹幕。\n角色设定:\n{char_list}\n图像描述:\n{img_desc_en}\nOCR结果:\n{ocr_text}",
#         }
#     ],
#     "temperature": 0.7,
#     "max_tokens": 2000
# }

payload = {
    "model": "llama",
    "messages": [
        {
            "role": "user", 
            "content": f"描述一下这张图像的内容",
        }
    ],
    "temperature": 0.7,
    "max_tokens": 2000
}
st_time = time.time()
r = requests.post(url, json=payload)
r.json()
print(r.json()["choices"][0]["message"]["content"])
print(time.time() - st_time)

# proc.terminate()
# proc.wait()
