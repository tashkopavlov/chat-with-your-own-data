from pathlib import Path


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
MODEL_KWARGS = {"device": "cpu"}
PERSIST_DIRECTORY = f'{str(Path(__file__).parent.parent)}/db/chroma-devcon/'
QA_CHAIN_PROMPT = """You are a helpful human assistant.
Use the following pieces of context to answer the users question.
If you don't know the answer, just say that you don't know, don't try to make \
up an answer.
The example of your response should be:

Context: {context}
Question: {question}

Only return the helpful answer below and nothing else. \
Always say "Thanks for asking!" at the end of the answer.
Helpful answer:
"""

WEB_LINKS = [
    "https://devcon.dev/",
    "https://devcon.dev/past-events/devcon-prishtina-2024/",
    "https://devcon.dev/past-events/devcon-skopje-2023/",
    "https://devcon.dev/past-events/devcon-prishtina-2022/",
    "https://devcon.dev/past-events/devcon-skopje-2022/",
    "https://devcon.dev/past-events/devcon-skopje-2019/"
]
