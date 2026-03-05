import asyncio
import json
import websockets
import time
import sys
from llama_server_new import start_llama_server
import requests
import httpx

proc = None

async def stream_chat_to_ws(ws, url: str, payload: dict):
    """
    将 OpenAI-compatible SSE 流 (data: {...}\n\n) 转发到 websocket
    前端将收到多条消息：
      - type=delta: 每次增量 token
      - type=done: 结束（附总耗时）
      - type=error: 出错
    """
    st_time = time.time()

    # 注意：stream=True 走 SSE
    payload = dict(payload)
    payload["stream"] = True

    try:
        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream("POST", url, json=payload) as resp:
                resp.raise_for_status()

                async for line in resp.aiter_lines():
                    if not line:
                        continue

                    # SSE 一般长这样：data: {...}
                    if line.startswith("data:"):
                        data = line[len("data:"):].strip()

                        # 结束标记
                        if data == "[DONE]":
                            await ws.send(json.dumps({
                                "type": "done",
                                "time": time.time() - st_time
                            }))
                            return

                        # 解析 chunk
                        try:
                            chunk = json.loads(data)
                        except Exception:
                            # 有些实现会夹杂奇怪的 keep-alive 行，忽略即可
                            continue

                        # OpenAI chat.completions streaming 常见结构：
                        # chunk["choices"][0]["delta"]["content"]
                        delta = ""
                        try:
                            choice0 = chunk.get("choices", [{}])[0]
                            delta = (choice0.get("delta", {}) or {}).get("content", "") or ""
                        except Exception:
                            delta = ""

                        if delta:
                            await ws.send(json.dumps({
                                "type": "delta",
                                "content": delta
                            }))

    except Exception as e:
        await ws.send(json.dumps({
            "type": "error",
            "message": f"流式推理失败: {e}"
        }))

# -------------------------
# 加载 / 重载模型
# -------------------------
def load_model(model_path, n_ctx, n_threads, use_gpu=False, **kwargs):
    global proc
    

    if proc is not None:
        print("[LLM] Shutdown llama server")
        proc.terminate()
        proc.wait()
        proc = None

    if use_gpu == False:
        print(f"[LLM] Loading model - llama server cpu: {model_path}")
        llama_server_path = kwargs.get("llama_server_path", "./llama/cpu/llama-server-cpu.exe")
    else:
        print(f"[LLM] Loading model - llama server cuda: {model_path}")
        llama_server_path = kwargs.get("llama_server_path", "./llama/cuda/llama-server-cuda.exe")

    n_gpu_layers = kwargs.get("n_gpu_layers", -1)
    # n_ctx = kwargs.get("n_ctx", 2048)
    # n_threads = kwargs.get("n_threads", 4)
    mmproj_path = kwargs.get("mmproj_path", None)
    llama_port = kwargs.get("llama_port", 8849)
    proc = start_llama_server(model_path, llama_server_path, n_gpu_layers=n_gpu_layers, n_ctx=n_ctx, n_threads=n_threads, port=llama_port, mmproj_path=mmproj_path)
    time.sleep(2) # 等待异步模型加载
    print("[LLM] Model loaded")


# -------------------------
# WS 处理逻辑
# -------------------------
async def handle_ws(ws):

    # global proc
    # proc = None
    # use_gpu = None
    # llama_port = None
    async for msg in ws:
        try:
            req = json.loads(msg)
            req_type = req.get("type", None)

            # -------------------------
            # 1. 启动 / 重载模型
            # -------------------------
            if req_type == "load_model":

                model_path = req["model_path"]
                mmproj_path = req.get("mmproj_path", None)
                n_ctx = req.get("n_ctx", 2048)
                n_threads = req.get("n_threads", 4)
                use_gpu = req.get("use_gpu", False)

                # llama_server_path = req.get("llama_server_path", "./llama/llama-server.exe")
                n_gpu_layers = req.get("n_gpu_layers", -1)
                llama_port = req.get("llama_port", 8849)

                load_model(model_path, n_ctx, n_threads, use_gpu=use_gpu, mmproj_path=mmproj_path, n_gpu_layers=n_gpu_layers, llama_port=llama_port)
                await ws.send(json.dumps({
                    "type": "load_model_ok",
                    "model_path": model_path
                }))
                continue

            # -------------------------
            # 2. 终止服务
            # -------------------------
            if req_type == "shutdown":

                if proc is not None:
                    proc.terminate()
                    proc.wait()

                await ws.send(json.dumps({
                    "type": "shutdown_ok" 
                }))

                print("[LLM] Shutdown requested")
                await ws.close()
                sys.exit(0)

            # -------------------------
            # 3. 推理请求
            # -------------------------
            
            if req_type == "infer":

                messages = req["messages"]                
                max_tokens = req.get("max_tokens", 512)
                temperature = req.get("temperature", 0.7)
                repeat_penalty = req.get("repeat_penalty", 1.0)
                top_p = req.get("top_p", 0.95)
                top_k = req.get("top_k", 40)
                seed = req.get("seed", -1)
                llama_port = req.get("llama_port", 8849)
                stream = req.get("stream", False)

                st_time = time.time()

                if proc is not None:

                    payload = {
                        "model": "llama",
                        "messages": messages,
                        "temperature": temperature,
                        "max_tokens": max_tokens,
                        "repeat_penalty": repeat_penalty,
                        "top_p": top_p,
                        "top_k": top_k,
                        "seed": seed,
                        # "stream": stream,
                    }

                    url = f"http://127.0.0.1:{llama_port}/v1/chat/completions"
                    if stream:
                        await stream_chat_to_ws(ws, url, payload)
                    else:
                        res = requests.post(url, json=payload)
                        text = res.json()["choices"][0]["message"]["content"]
                
                else:
                    await ws.send(json.dumps({
                        "type": "error",
                        "message": "Model not loaded"
                    }))
                    continue
                try:
                    print("[LLM] Response: ", text)
                    # try:
                    #     text_new, char_list, danmu_list = text, [], [] # clean_response(messages[-1]["content"], text)
                    # except Exception as e:
                    #     print(e)
                    #     text_new, char_list, danmu_list = text, [], []

                    await ws.send(json.dumps({
                        "type": "result",
                        "content": text,
                        # 'content_clean': text_new,
                        # "char_list": char_list,
                        # "danmu_list": danmu_list,
                        "time": time.time() - st_time
                    }))

                except Exception as e:
                    await ws.send(json.dumps({
                        "type": "error",
                        "message": "response解析错误: "+ str(e)
                    }))
            
            

            if req_type == None:
                await ws.send(json.dumps({
                    "type": "error",
                    "message" : "请求类型type不能为空"
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
    async with websockets.serve(handle_ws, "0.0.0.0", 8848, max_size=8 * 1024 * 1024):
        print("WebSocket LLaMA server running at ws://localhost:8848")
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())


# pyinstaller --onefile --noconsole --clean --exclude-module torch --exclude-module transformers --exclude-module llama_cpp_python --exclude-module tensorflow --exclude-module sentencepiece --exclude-module datasets --add-data "llama_server_new.py;." llama_server_websocket_new.py --name llama_server_260305