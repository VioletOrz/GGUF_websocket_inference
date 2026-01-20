conda create -n llama_inf python=3.11

conda activate llama_inf

pip install -r requirements.txt

# Windows

if use cuda, you should download llama-server-cuda.exe, copy all dll file and llama-server.exe to ./llama/

https://github.com/ggml-org/llama.cpp/releases?utm_source=chatgpt.com

pip install pyinstaller

pyinstaller --onefile --noconsole --clean --exclude-module torch --exclude-module transformers --exclude-module tensorflow --exclude-module sentencepiece --exclude-module datasets --add-binary "E:\AIGC\env\llama\Lib\site-packages\llama_cpp\lib\*.dll;." --add-data "llama_server.py;." llama_server_websocket.py

# Launch llama_server_websocket.exe for testing

python api_test.py

# Linux and MacOS

python llama_server_websocket.py 

python api_test.py

if use cuda, pip install llama-cpp-python cuda version on linux and Mac, and modify the parameters in lines 74-79 of the code to use cuda.