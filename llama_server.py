import subprocess
import os
import threading

def start_llama_server(model_path, llama_server_path, n_gpu_layers=-1, n_ctx=4096, n_threads=4, port=8848,):
    env = os.environ.copy()
    env["CUDA_VISIBLE_DEVICES"] = "0"

    cmd = [
        llama_server_path,
        "--model", model_path,
        "--n_gpu_layers", f"{n_gpu_layers}",
        "--port", f"{port}",
        "-c", f"{n_ctx}",
        "-t", f"{n_threads}",
    ]

    CREATE_NO_WINDOW = 0x08000000

    debug = False

    if debug:
        proc = subprocess.Popen(
            cmd,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            # stdout=subprocess.DEVNULL,
            # stderr=subprocess.DEVNULL,
            # creationflags=CREATE_NO_WINDOW,
            text=True,
            bufsize=1
        )
        def log_reader():
            for line in proc.stdout:
                print("[llama]", line.rstrip())

        threading.Thread(target=log_reader, daemon=True).start()

    else:
        proc = subprocess.Popen(
            cmd,
            env=env,
            # stdout=subprocess.PIPE,
            # stderr=subprocess.STDOUT,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=CREATE_NO_WINDOW,
            text=True,
            bufsize=1
        )

    return proc


if __name__ == "__main__":
    llama_server_path = './llama/llama-server.exe'
    model_path = r'G:\models\Qwen3-0.6B\Qwen3-0.6B-full-nothink-260113-smix01\Qwen3-0.6B-full-nothink-260113-smix01-Q4_K_M.gguf'
    proc = start_llama_server(model_path, llama_server_path, use_gpu=False, n_gpu_layers=-1, n_ctx=2048, n_threads=4, port=8848)

    proc.terminate()
    proc.wait()