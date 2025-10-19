# shopunow_faq.py
import os
import json
from typing import List, Tuple

import faiss
import numpy as np
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_core.documents import Document

# Cache globals
_FAQ_VECTOR_STORE: FAISS = None
_FAQ_DOCS: List[Document] = []
_FAQ_PATH: str = None

def resolve_faq_path() -> str:
    """
    Resolve the path to the shopunow_faqs.jsonl file.
    Looks in common locations: /content, ./data/, ./ (repo root).
    Raises FileNotFoundError if not found.
    """
    candidates = [
        "/content/shopunow_faqs.jsonl",
        os.path.join(os.getcwd(), "data", "shopunow_faqs.jsonl"),
        os.path.join(os.getcwd(), "shopunow_faqs.jsonl"),
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    raise FileNotFoundError("❌ shopunow_faqs.jsonl not found in common paths.")

def load_faq_documents(path: str) -> List[Document]:
    """
    Read the JSONL file and parse into a list of Documents.
    Each JSON line should have `question`, `answer`, `department` fields.
    """
    docs: List[Document] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
                question = rec.get("question", "").strip()
                answer   = rec.get("answer", "").strip()
                dept     = rec.get("department", "unknown").strip()
                if not question or not answer:
                    continue
                combined = f"Q: {question}\nA: {answer}"
                docs.append(Document(
                    page_content=combined,
                    metadata={
                        "department": dept,
                        "question": question,
                        "answer": answer
                    }
                ))
            except json.JSONDecodeError as e:
                print(f"⚠️ Skipping invalid JSON line: {e}")
    return docs

def build_faq_vector_store(docs: List[Document]) -> Tuple[FAISS, List[Document]]:
    """
    Build a FAISS vector store from the given documents using OpenAI embeddings.
    Returns the vector store and the docs list.
    """
    if not docs:
        raise ValueError("No FAQ documents to build vector store.")
    embedding_model = OpenAIEmbeddings(model="text-embedding-ada-002")
    # compute dimension by doing a dummy query
    dummy = embedding_model.embed_query("hello world")
    dim   = len(dummy)
    index = faiss.IndexFlatIP(dim)  # Inner-product (cosine normalized) or L2
    # If using cosine, you may normalize embeddings before adding (see your code)
    store = FAISS(
        embedding_function=embedding_model,
        index=index,
        docstore=InMemoryDocstore(),
        index_to_docstore_id={}
    )
    ids = [f"faq_{i+1}" for i in range(len(docs))]
    store.add_documents(documents=docs, ids=ids)
    return store, docs

def get_faq_vector_store() -> Tuple[FAISS, List[Document]]:
    """
    Lazy initializer: returns an existing vector store if built, otherwise builds it.
    """
    global _FAQ_VECTOR_STORE, _FAQ_DOCS, _FAQ_PATH
    if _FAQ_VECTOR_STORE is not None:
        return _FAQ_VECTOR_STORE, _FAQ_DOCS
    _FAQ_PATH = resolve_faq_path()
    _FAQ_DOCS = load_faq_documents(_FAQ_PATH)
    _FAQ_VECTOR_STORE, _FAQ_DOCS = build_faq_vector_store(_FAQ_DOCS)
    dept_set = { d.metadata.get("department", "unknown") for d in _FAQ_DOCS }
    print(f"✅ Built vector store with {len(_FAQ_DOCS)} FAQs across {len(dept_set)} departments")
    return _FAQ_VECTOR_STORE, _FAQ_DOCS
