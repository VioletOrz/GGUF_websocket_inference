import asyncio
import json
import websockets
from llama_cpp import Llama
import time
import sys

llm = None   # 全局模型实例

def clean_response(prompt, response):

    # prompt = '"请从用户屏幕的OCR结果中总结关键信息，并以给定角色设定的口吻，为每个角色输出一条简短的网络用语风格弹幕。\n角色设定:\n姓名: 宇智波鼬 出自作品: 火影忍者 状态: 晓组织执行任务状态（冷酷疏离）\n姓名: 花子君 出自作品: 地缚少年花子君 状态: 日常恶作剧（校园七大不可思议）\n姓名: 我妻由乃 出自作品: 未来日记 状态: 日常守护雪辉状态（温柔乖巧）\n姓名: 三笠·阿克曼 出自作品: 进击的巨人 状态: 日常守护艾伦状态（温柔警惕）\n姓名: 利姆鲁·特恩佩斯特 出自作品: 关于我转生变成史莱姆这档事 状态: 刚转生为史莱姆（初期）\nOCR结果:\n标题: 【说书人】吐血讲解《后光杀人事件》｜炫学流你就使劲秀吧\n内容: 画家也没法再装了啊\n'
    res = response
    res = res.replace('<', '')
    res = res.replace('>', '')
    id_danmu_list = res.split('\n')

    char_text = prompt.strip().split('角色设定:\n')[1].split('OCR结果:')[0].strip().split('\n')
    char_list = []

    for char in char_text:
        if char.strip() != '':
            char_list.append(char.split('姓名: ')[1].split(' ')[0])

    res_char_list = []
    res_danmu_list = []
    for id_danmu in id_danmu_list:

        if len(id_danmu.split('：')) != 2:
            continue
        else:
            res_char = id_danmu.split('：')[0].strip()
            for char in char_list:
                if res_char in char:
                    res = res.replace(res_char, char)
                    res_char = char
                    break
            
            if res_char not in char_list:
                continue
            res_char_list.append(res_char)
            res_danmu_list.append(id_danmu.split('：')[1].strip())
    res_new = ''
    for i in range(len(res_char_list)):
        res_new += res_char_list[i] + '：' + res_danmu_list[i] + '\n'
    return res_new, res_char_list, res_danmu_list



# -------------------------
# 加载 / 重载模型
# -------------------------
def load_model(model_path, n_ctx, n_threads):
    global llm
    print(f"[LLM] Loading model: {model_path}")
    llm = Llama(
        model_path=model_path,
        n_ctx=n_ctx,
        n_batch=512,
        n_threads=n_threads,
    )
    print("[LLM] Model loaded")


# -------------------------
# WS 处理逻辑
# -------------------------
async def handle_ws(ws):
    global llm

    async for msg in ws:
        try:
            req = json.loads(msg)
            req_type = req.get("type", "infer")

            # -------------------------
            # 1. 启动 / 重载模型
            # -------------------------
            if req_type == "load_model":
                model_path = req["model_path"]
                n_ctx = req.get("n_ctx", 4096)
                n_threads = req.get("n_threads", 4)

                load_model(model_path, n_ctx, n_threads)

                await ws.send(json.dumps({
                    "type": "load_model_ok",
                    "model_path": model_path
                }))
                continue

            # -------------------------
            # 2. 终止服务
            # -------------------------
            if req_type == "shutdown":
                await ws.send(json.dumps({
                    "type": "shutdown_ok"
                }))
                print("[LLM] Shutdown requested")
                await ws.close()
                sys.exit(0)

            # -------------------------
            # 3. 推理请求
            # -------------------------
            if llm is None:
                await ws.send(json.dumps({
                    "type": "error",
                    "message": "Model not loaded"
                }))
                continue

            messages = req["messages"]
            max_tokens = req.get("max_tokens", 512)
            temperature = req.get("temperature", 0.7)
            stream = req.get("stream", False)
            repeat_penalty = req.get("repeat_penalty", 1.0)
            top_p = req.get("top_p", 0.95)
            top_k = req.get("top_k", 40)
            seed = req.get("seed", -1)

            st_time = time.time()

            if stream:
                for out in llm.create_chat_completion(
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    stream=True,
                    repeat_penalty=repeat_penalty,
                    top_p=top_p,
                    top_k=top_k,
                    seed=seed
                ):
                    delta = out["choices"][0]["delta"].get("content")
                    if delta:
                        await ws.send(json.dumps({
                            "type": "token",
                            "content": delta
                        }))

                await ws.send(json.dumps({"type": "end"}))

            else:
                out = llm.create_chat_completion(
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    repeat_penalty=repeat_penalty,
                    top_p=top_p,
                    top_k=top_k,
                    stream=False,
                    seed=seed
                )

                text = out["choices"][0]["message"]["content"]
                text_new, char_list, danmu_list = clean_response(messages[-1]["content"], text)
                await ws.send(json.dumps({
                    "type": "result",
                    "content": text,
                    'content_clean': text_new,
                    "char_list": char_list,
                    "danmu_list": danmu_list,
                    "time": time.time() - st_time
                }))

        except Exception as e:
            await ws.send(json.dumps({
                "type": "error",
                "message": str(e)
            }))

# -------------------------
# 启动 WS Server
# -------------------------
async def main():
    async with websockets.serve(handle_ws, "0.0.0.0", 8848):
        print("WebSocket LLaMA server running at ws://localhost:8848")
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())


# pyinstaller --onefile --noconsole --clean --exclude-module torch --exclude-module transformers --exclude-module tensorflow --exclude-module sentencepiece --exclude-module datasets --add-binary "E:\AIGC\env\llama\Lib\site-packages\llama_cpp\lib\*.dll;." llama_websocket.py