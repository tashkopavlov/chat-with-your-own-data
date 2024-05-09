# chat-with-your-own-data

## How to run the application locally

    1. git clone <https://github.com/tashkopavlov/chat-with-your-own-data>
    2. python -m venv venv
    3. source venv/bin/activate (for Linux based systems)
    4. pip install -r requirements.txt

    5. Install Ollama locally:
        - curl -fsSL https://ollama.com/install.sh | sh
        - ollama pull llama2
        - ollama run llama2 [optional]
        - ollama serve [required]

    6. Load documents:
        - export PYTHONPATH="${PYTHONPATH}:util"
        - python util/document_loader.py

    7. Finally run the application:
        - chainlit run main.py
