import asyncio
import json
import websockets

async def test_ws_no_stream(messages, reply = False):
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
            print(f"\n生成耗时：{data['time']:.2f} 秒")
            #清洗弹幕
            print(clean_response(data["content"], character_set, reply=reply))

        elif data["type"] == "error":
            print("ERROR:", data["message"])

async def test_ws_load_model(model_path, mmproj_path=None, n_ctx=4096, n_gpu_layers=-1,  n_threads=4, use_gpu=False):
    uri = "ws://localhost:8848"

    async with websockets.connect(uri) as ws:
        
        req = {
            "type": "load_model",
            "model_path": model_path,
            "mmproj_path": mmproj_path,
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
    model_l_path = "models\AndesVL-Qwen3-reply-smix06-lora-Q5_K_M.gguf"
    mmproj_path = "models/mmproj-model-Q8_0.gguf"
    template_path = 'template/prompt_template.jinja'
    
    # 推理测试

    messages_img = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "提取图像中的文字"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"F:/code/llama_inf/yg.png"
                    },
                },
            ],
        },
    ]

    from template.message_template import create_message_from_template, clean_response

    mode = 'reply_ocr'
    character_set = """姓名: 灶门祢豆子 出自作品: 鬼灭之刃 状态: 与炭治郎独处（温柔柔软状态）
姓名: 久保渚咲 出自作品: 久保同学不放过我 状态: 与久保明正面互动（羞涩局促状态）
姓名: 樱之宫莓香 出自作品: 调教咖啡厅 状态: 被客人误解（真的吓到人）
姓名: 夏目贵志 出自作品: 夏目友人帐 状态: 与猫咪老师相处（轻松惬意状态）"""
    ocr_result = """这里填什么信息都可以，基本没有格式限制和内容限制。\n但注意不要太长，也不要出现很多冗余的无用信息，内容尽量精简。"""
    image_description = """这里填一整段完整的图片描述。中间尽量不要用回车分割。(有应该也没什么影响)"""
    danmu_text = """申鹤：剑心澄澈
神里绫华：此游戏虽真实，望玩家珍视生命之重
八重神子：法医之戏？不如清酒配轻小说呢～
刻晴：攻略当简明高效，避免冗余恐怖"""

    message = create_message_from_template(template_path, mode, character_set, ocr_result, image_description = image_description, danmu_text = danmu_text)
    print(message[1]["content"])
    print('-'*100)

    n_ctx = 2048
    n_threads = 8
    n_gpu_layers = -1
    # asyncio.run(test_ws_load_model(model_l_path, n_ctx=n_ctx, n_gpu_layers=n_gpu_layers, n_threads=n_threads, use_gpu=True)) 
    asyncio.run(test_ws_load_model(model_l_path, mmproj_path=mmproj_path, n_ctx=n_ctx, n_gpu_layers=n_gpu_layers, n_threads=n_threads, use_gpu=True)) 
    asyncio.run(test_ws_no_stream(message, reply=True))
    asyncio.run(test_ws_load_model(model_l_path, mmproj_path=mmproj_path, n_ctx=n_ctx, n_gpu_layers=n_gpu_layers, n_threads=n_threads, use_gpu=False)) 
    asyncio.run(test_ws_no_stream(messages_img))
    # asyncio.run(test_ws_no_stream(messages))
    # asyncio.run(test_ws_no_stream(messages_reply))
    # asyncio.run(test_ws_no_stream(messages_l))
    # asyncio.run(test_ws_load_model(model_l_path, n_ctx=n_ctx, n_gpu_layers=n_gpu_layers, n_threads=n_threads, use_gpu=False)) 
    # asyncio.run(test_ws_no_stream(messages))
    # asyncio.run(test_ws_no_stream(messages_l))
    # asyncio.run(test_ws_load_model(model_l_path, n_ctx=n_ctx, n_gpu_layers=n_gpu_layers, n_threads=n_threads, use_gpu=True)) 
    # asyncio.run(test_ws_no_stream(messages))
    # # 终止服务测试g:\models\AndesVL\AndesVL-Qwen3-reply-smix06-lora\AndesVL-Qwen3-reply-smix06-lora-Q5_K_M.gguf
    # asyncio.run(test_ws_shutdown())

#     asyncio.run(test_ws())

