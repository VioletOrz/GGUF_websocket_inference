import requests
from llama_server import start_llama_server

llama_server_path = r'./llama/llama-server.exe'
model_path = r'G:\models\Qwen3-0.6B\Qwen3-0.6B-full-nothink-260113-smix01\Qwen3-0.6B-full-nothink-260113-smix01-Q4_K_M.gguf'
proc = start_llama_server(model_path, llama_server_path, n_gpu_layers=10, n_ctx=2048, n_threads=4, port=8848)

    
url = "http://127.0.0.1:8848/v1/chat/completions"

import time
payload = {
    "model": "llama",
    "messages": [
        {
            "role": "system",
            "content":"你是一个弹幕助手，请从用户提供的ocr结果中总结关键信息，并根据用户提供的角色设定，为每一个角色生成一条符合人设的弹幕。"
        },
        {
            "role": "user", 
            "content": "请从用户屏幕的OCR结果中总结关键信息，并以给定角色设定的口吻，为每个角色输出一条简短的网络用语风格弹幕。\n角色设定:\n姓名: 宇智波鼬 出自作品: 火影忍者 状态: 晓组织执行任务状态（冷酷疏离）\n姓名: 花子君 出自作品: 地缚少年花子君 状态: 日常恶作剧（校园七大不可思议）\n姓名: 我妻由乃 出自作品: 未来日记 状态: 日常守护雪辉状态（温柔乖巧）\n姓名: 三笠·阿克曼 出自作品: 进击的巨人 状态: 日常守护艾伦状态（温柔警惕）\n姓名: 利姆鲁·特恩佩斯特 出自作品: 关于我转生变成史莱姆这档事 状态: 刚转生为史莱姆（初期）\nOCR结果:\n标题: 【说书人】吐血讲解《后光杀人事件》｜炫学流你就使劲秀吧\n内容: 画家也没法再装了啊\n",
        }
    ],
    "temperature": 0.7,
    "max_tokens": 200
}
time.sleep(3)
st_time = time.time()
r = requests.post(url, json=payload)

print(r.json()["choices"][0]["message"]["content"])
print(time.time() - st_time)

proc.terminate()
proc.wait()