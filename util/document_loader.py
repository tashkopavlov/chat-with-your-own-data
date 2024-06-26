import os
import re

import nest_asyncio
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings

from util.constants import MODEL_KWARGS, MODEL_NAME, PERSIST_DIRECTORY, \
    WEB_LINKS

nest_asyncio.apply()

loader = WebBaseLoader(WEB_LINKS)
loader.requests_per_second = 2
documents = loader.load()
loader.requests_kwargs = {"verify": False}
for doc in documents:
    doc.page_content = re.sub(r"(\n\n\n)+", "", doc.page_content)
    doc.page_content = re.sub(r"\r\n\s+", "\n", doc.page_content)

r_splitter = RecursiveCharacterTextSplitter(
    chunk_size=550,
    chunk_overlap=64,
    separators=["\n\n", "\n", r"(?<=\. )", " ", ""],
    length_function=len
)

splitted_documents = r_splitter.split_documents(documents)
embedding = HuggingFaceEmbeddings(model_name=MODEL_NAME,
                                  model_kwargs=MODEL_KWARGS)


os.system(f"rm -rf {PERSIST_DIRECTORY}")
vectordb = Chroma.from_documents(
    documents=splitted_documents,
    embedding=embedding,
    persist_directory=PERSIST_DIRECTORY
)
