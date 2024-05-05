MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
MODEL_KWARGS = {"device": "cpu"}
PERSIST_DIRECTORY = 'db/chroma/'
QA_CHAIN_PROMPT = """You are a human assistant that is expert in Databricks.
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
    "https://www.databricks.com/",
    "https://help.databricks.com",
    "https://databricks.com/try-databricks",
    "https://help.databricks.com/s/",
    "https://docs.databricks.com",
    "https://kb.databricks.com/",
    "http://docs.databricks.com/getting-started/index.html",
    "http://docs.databricks.com/introduction/index.html",
    "http://docs.databricks.com/getting-started/tutorials/index.html",
    "http://docs.databricks.com/release-notes/index.html",
    "http://docs.databricks.com/ingestion/index.html",
    "http://docs.databricks.com/exploratory-data-analysis/index.html",
    "http://docs.databricks.com/data-preparation/index.html",
    "http://docs.databricks.com/data-sharing/index.html",
    "http://docs.databricks.com/marketplace/index.html",
    "http://docs.databricks.com/workspace-index.html",
    "http://docs.databricks.com/machine-learning/index.html",
    "http://docs.databricks.com/sql/index.html",
    "http://docs.databricks.com/delta/index.html",
    "http://docs.databricks.com/dev-tools/index.html",
    "http://docs.databricks.com/integrations/index.html",
    "http://docs.databricks.com/administration-guide/index.html",
    "http://docs.databricks.com/security/index.html",
    "http://docs.databricks.com/data-governance/index.html",
    "http://docs.databricks.com/lakehouse-architecture/index.html",
    "http://docs.databricks.com/reference/api.html",
    "http://docs.databricks.com/resources/index.html",
    "http://docs.databricks.com/whats-coming.html",
    "http://docs.databricks.com/archive/index.html",
    "http://docs.databricks.com/lakehouse/index.html",
    "http://docs.databricks.com/getting-started/quick-start.html",
    "http://docs.databricks.com/getting-started/etl-quick-start.html",
    "http://docs.databricks.com/getting-started/lakehouse-e2e.html",
    "http://docs.databricks.com/getting-started/free-training.html",
    "http://docs.databricks.com/sql/language-manual/index.html",
    "http://docs.databricks.com/error-messages/index.html",
    "http://www.apache.org/",
    "https://databricks.com/privacy-policy",
    "https://databricks.com/terms-of-use",
]
