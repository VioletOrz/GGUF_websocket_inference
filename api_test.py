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
            "stream": False,
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

async def test_ws_load_model(model_path, n_ctx=4096, n_threads=4):
    uri = "ws://localhost:8848"

    async with websockets.connect(uri) as ws:
        
        req = {
            "type": "load_model",
            "model_path": model_path,
            "n_ctx": n_ctx,
            "n_threads": n_threads
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
    asyncio.run(test_ws_load_model(model_l_path)) 
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
    asyncio.run(test_ws_no_stream(messages))
    # 终止服务测试
    asyncio.run(test_ws_shutdown())

#     asyncio.run(test_ws())