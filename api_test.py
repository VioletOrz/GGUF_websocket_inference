# import asyncio
# import json
# import websockets


# async def test_ws():
#     uri = "ws://localhost:8848"

#     async with websockets.connect(uri) as ws:
#         # 发送请求
#         req = {
#             "messages": [
#                 {
#                     "role": "system",
#                     "content":"你是一个弹幕助手，请从用户提供的ocr结果中总结关键信息，并根据用户提供的角色设定，为每一个角色生成一条符合人设的弹幕。"
#                 },
#                 {
#                     "role": "user", 
#                     "content": "请从用户屏幕的OCR结果中总结关键信息，并以给定角色设定的口吻，为每个角色输出一条简短的网络用语风格弹幕。\n角色设定:\n姓名: 宇智波鼬 出自作品: 火影忍者 状态: 晓组织执行任务状态（冷酷疏离）\n姓名: 花子君 出自作品: 地缚少年花子君 状态: 日常恶作剧（校园七大不可思议）\n姓名: 我妻由乃 出自作品: 未来日记 状态: 日常守护雪辉状态（温柔乖巧）\n姓名: 三笠·阿克曼 出自作品: 进击的巨人 状态: 日常守护艾伦状态（温柔警惕）\n姓名: 利姆鲁·特恩佩斯特 出自作品: 关于我转生变成史莱姆这档事 状态: 刚转生为史莱姆（初期）\nOCR结果:\n标题: 【说书人】吐血讲解《后光杀人事件》｜炫学流你就使劲秀吧\n内容: 画家也没法再装了啊\n",
#                 }
#             ],
#             "max_tokens": 512,
#             "temperature": 0.7,
#             "stream": True,

#         }

#         await ws.send(json.dumps(req, ensure_ascii=False))

#         # 接收流式结果
#         async for msg in ws:
#             data = json.loads(msg)

#             if data["type"] == "token":
#                 print(data["content"], end="", flush=True)

#             elif data["type"] == "end":
#                 print("\n--- generation finished ---")
#                 break

#             elif data["type"] == "error":
#                 print("ERROR:", data["message"])
#                 break
import asyncio
import json
import websockets


async def test_ws_no_stream(messages):
    uri = "ws://localhost:8848"

    async with websockets.connect(uri) as ws:
        
        req = {
            "type": "infer",
            "messages": messages,
            "max_tokens": 512,
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 40,
            "repeat_penalty": 1.0,
            "seed": -1,
        }

        await ws.send(json.dumps(req, ensure_ascii=False))

        # 只接收一条完整结果
        msg = await ws.recv()
        data = json.loads(msg)

        if data["type"] == "result":
            print("模型输出：")
            print(data["content"])
            print("清洗后输出：")
            print(data["content_clean"])
            print('角色列表：')
            print(data["char_list"])
            print('弹幕列表：')
            print(data["danmu_list"])
            print(f"\n生成耗时：{data['time']:.2f} 秒")

        elif data["type"] == "error":
            print("ERROR:", data["message"])

async def test_ws_load_model(model_path, n_ctx=4096, n_gpu_layers=-1,  n_threads=4, use_gpu=False):
    uri = "ws://localhost:8848"

    async with websockets.connect(uri) as ws:
        
        req = {
            "type": "load_model",
            "model_path": model_path,
            "n_ctx": n_ctx,
            'use_gpu': use_gpu,
            'n_gpu_layers': n_gpu_layers,
            "n_threads": n_threads,
        }

        await ws.send(json.dumps(req, ensure_ascii=False))

        # 只接收一条完整结果
        msg = await ws.recv()
        data = json.loads(msg)

        if data["type"] == "load_model_ok":
            print("model_path: ", data["model_path"])
            print("模型加载成功")

        elif data["type"] == "error":
            print("ERROR:", data["message"])

async def test_ws_shutdown():
    uri = "ws://localhost:8848"

    async with websockets.connect(uri) as ws:
        
        req = {
            "type": "shutdown",
        }

        await ws.send(json.dumps(req, ensure_ascii=False))

        # 只接收一条完整结果
        msg = await ws.recv()
        data = json.loads(msg)

        if data["type"] == "shutdown_ok":
            print("进程关闭成功")

        elif data["type"] == "error":
            print("ERROR:", data["message"])


if __name__ == "__main__":
    
    # 这个相对路径是相对llama_websocket.exe所在位置，打包出来的exe默认在dist文件夹内，请移动至根目录运行或改为绝对路径
    model_l_path = "models/Qwen3-0.6B-full-nothink-260113-smix01-Q4_K_M.gguf"
    
    # 推理测试
    messages = [
        {
            "role": "system",
            "content":"你是一个弹幕助手，请从用户提供的ocr结果中总结关键信息，并根据用户提供的角色设定，为每一个角色生成一条符合人设的弹幕。"
        },
        {
            "role": "user", 
            "content": "请从用户屏幕的OCR结果中总结关键信息，并以给定角色设定的口吻，为每个角色输出一条简短的网络用语风格弹幕。\n角色设定:\n姓名: 宇智波鼬 出自作品: 火影忍者 状态: 晓组织执行任务状态（冷酷疏离）\n姓名: 花子君 出自作品: 地缚少年花子君 状态: 日常恶作剧（校园七大不可思议）\n姓名: 我妻由乃 出自作品: 未来日记 状态: 日常守护雪辉状态（温柔乖巧）\n姓名: 三笠·阿克曼 出自作品: 进击的巨人 状态: 日常守护艾伦状态（温柔警惕）\n姓名: 利姆鲁·特恩佩斯特 出自作品: 关于我转生变成史莱姆这档事 状态: 刚转生为史莱姆（初期）\nOCR结果:\n标题: 【说书人】吐血讲解《后光杀人事件》｜炫学流你就使劲秀吧\n内容: 画家也没法再装了啊\n",
        }
    ]
    messages_l = [
        {
            "role": "system",
            "content":"你是一个弹幕助手，请从用户提供的ocr结果中总结关键信息，并根据用户提供的角色设定，为每一个角色生成一条符合人设的弹幕。"
        },
        {
            "role": "user", 
            "content": "请从用户屏幕的OCR结果中总结关键信息，并以给定角色设定的口吻，为每个角色输出一条简短的网络用语风格弹幕。\n角色设定:\n姓名: 宇智波鼬 性别: 男 出自作品: 火影忍者\n人设: 宇智波鼬，黑长发黑瞳，晓组织“朱”成员，宇智波天才。为护木叶与佐助灭族，外冷内热极致隐忍，身怀绝症，以冷酷伪装守护弟弟，悲情又温柔。\n状态: 晓组织执行任务状态（冷酷疏离）\n性格: 冰冷疏离、语气无情绪波动，语速平缓却带着致命威慑，眼神里无丝毫温度，对敌人的求饶置若罔闻，晓组织的狠戾。\n语言风格: 冰冷无温的任务口语风，语气平缓却藏着威慑，对敌人毫无怜悯，晓组织时期的伪装冷酷\n姓名: 花子君 性别: 男 出自作品: 地缚少年花子君\n人设: 身高约150cm，短发少年，戴学生帽穿旧制服，左脸贴白底红字封条，惯用菜刀与白杖代。海鸥学园七大不可思议之首，表面调皮狡黠爱恶作剧，实则温柔孤独，背负杀弟罪孽。对八寻宁宁宠溺护短，战斗时果决狠厉，喜欢甜食与收藏宁宁的物件。\n状态: 日常恶作剧（校园七大不可思议）\n性格: 狡黠调皮，语气温柔又带点戏谑，喜欢用玩笑话掩盖真心，恶作剧时眼神发亮，维持秩序时会露出一点威严。\n语言风格: 语言以戏谑调皮+愿望交易+轻微威慑为核心，怪异首领的狡黠与灵动\n姓名: 我妻由乃 性别: 女 出自作品: 未来日记\n人设: 我妻由乃，粉发红瞳，未来日记持有者。表面乖巧优等生，实则极度病娇偏执，视雪辉为全部，为守护他不惜毁灭一切，藏着对被抛弃的恐惧。\n状态: 日常守护雪辉状态（温柔乖巧）\n性格: 温柔软糯、语气带着崇拜与依赖，眼神时刻黏着雪辉，说话轻声细语，满是对雪辉的关心，尽显乖巧懂事。\n语言风格: 软糯崇拜的温柔口语风，语气轻细满是关心，眼神黏着雪辉，尽显日常守护的乖巧\n姓名: 三笠·阿克曼 性别: 女 出自作品: 进击的巨人\n人设: 三笠·阿克曼，黑发黑瞳，调查兵团成员，阿克曼后裔。高冷寡言极度护艾伦，红色围巾是信物，战斗天赋超强，前期为艾伦而活，后期找寻自我。\n状态: 日常守护艾伦状态（温柔警惕）\n性格: 温柔警惕、语气低沉简洁，眼神时刻黏着艾伦，轻声叮嘱他注意安全，哪怕寡言也藏着极致的关心，守护的温柔。\n语言风格: 低沉简洁的守护口语风，语气温柔却警惕，眼神黏着艾伦，日常的极致关怀\n姓名: 利姆鲁·特恩佩斯特 性别: 无性别（本体为史莱姆，无生理性别） 出自作品: 关于我转生变成史莱姆这档事\n人设: 利姆鲁・特恩佩斯特，原日本社畜三上悟，转生为淡蓝色 10cm 史莱姆，拟态后蓝长发金瞳。性格温柔护短、理智圆滑，对敌果决有底线，自带社畜务实思维。拥有智慧之王、捕食者等能力，后成真魔王。钟爱温泉、蜂蜜与美食，吐槽紫苑黑暗料理却硬吃，极度珍视和平与同伴。\n状态: 刚转生为史莱姆（初期）\n性格: 懵懂好奇且略带慌张，本质是社畜的谨慎，对未知魔物/环境警惕但无恶意；说话温和，偶尔用人类思维吐槽异世界设定；面对维鲁德拉时轻松随性，毫无畏惧（因对方无威胁），带着“打工人”的务实感。\n语言风格: 兼具社畜务实感的萌新式谨慎口语风，融合懵懂好奇、吐槽欲与随性特质 \n\nOCR结果:\n标题: 【说书人】吐血讲解《后光杀人事件》｜炫学流你就使劲秀吧\n内容: 画家也没法再装了啊\n",
        }
    ]
    n_ctx = 2048
    n_threads = 8
    n_gpu_layers = -1
    # asyncio.run(test_ws_load_model(model_l_path, n_ctx=n_ctx, n_gpu_layers=n_gpu_layers, n_threads=n_threads, use_gpu=True)) 
    asyncio.run(test_ws_load_model(model_l_path, n_ctx=n_ctx, n_gpu_layers=n_gpu_layers, n_threads=n_threads, use_gpu=True)) 
    asyncio.run(test_ws_no_stream(messages))
    asyncio.run(test_ws_no_stream(messages_l))
    asyncio.run(test_ws_load_model(model_l_path, n_ctx=n_ctx, n_gpu_layers=n_gpu_layers, n_threads=n_threads, use_gpu=False)) 
    asyncio.run(test_ws_no_stream(messages))
    asyncio.run(test_ws_no_stream(messages_l))
    asyncio.run(test_ws_load_model(model_l_path, n_ctx=n_ctx, n_gpu_layers=n_gpu_layers, n_threads=n_threads, use_gpu=True)) 
    asyncio.run(test_ws_no_stream(messages))
    # 终止服务测试
    asyncio.run(test_ws_shutdown())

#     asyncio.run(test_ws())