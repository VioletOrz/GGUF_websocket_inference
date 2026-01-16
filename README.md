conda create -n llama_inf python=3.11

conda activate llama_inf

pip install -r requirements.txt

# Windows

pip install pyinstaller

pyinstaller --onefile --noconsole --clean --exclude-module torch --exclude-module transformers --exclude-module tensorflow --exclude-module sentencepiece --exclude-module datasets --add-binary "YOUR_CONDA_ENV_PATH\llama_inf\Lib\site-packages\llama_cpp\lib\*.dll;." llama_websocket.py

# Launch llama_websocket.exe for testing

python llama_test.py

# Linux

python llama_websocket.py 

python llama_test.py