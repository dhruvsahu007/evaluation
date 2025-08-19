import os
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from textwrap import dedent
import numpy as np

CHUNK_SIZE = 400
CHUNK_OVERLAP = 100
TOP_K = 3
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

def split_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    chunks = []
    start = 0
    while start < len(text):
        end = min(len(text), start + chunk_size)
        chunk = text[start:end]
        chunks.append(chunk.strip())
        start += chunk_size - overlap
    return [c for c in chunks if c]

embedder = SentenceTransformer(MODEL_NAME)

def embed_texts(texts):
    return embedder.encode(texts, normalize_embeddings=True)

def load_documents():
    docs = {}
    for fname in os.listdir("docs"):
        path = os.path.join("docs", fname)
        if not fname.lower().endswith((".txt", ".md")):
            continue
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
        chunks = split_text(text)
        docs[fname] = chunks
    return docs

def build_index(docs):
    texts, meta = [], []
    for fname, chunks in docs.items():
        for i, chunk in enumerate(chunks):
            texts.append(chunk)
            meta.append({"source": fname, "chunk_id": i})
    embeddings = embed_texts(texts)
    return texts, embeddings, meta

def search(query, texts, embeddings, meta, top_k=TOP_K):
    q_emb = embed_texts([query])
    sims = cosine_similarity(q_emb, embeddings)[0]
    idx = np.argsort(sims)[::-1][:top_k]
    return [(texts[i], meta[i], sims[i]) for i in idx]

def answer(query, texts, embeddings, meta):
    hits = search(query, texts, embeddings, meta)
    context = "\n\n---\n\n".join(
        f"[{m['source']}#{m['chunk_id']}] {t}" for t, m, _ in hits
    )
    print(dedent(f"""
    Q: {query}
    
    Context from docs:
    {context}
    
    (You can now copy this context into an LLM like GPT or just read it)
    """))

if __name__ == "__main__":
    os.makedirs("docs", exist_ok=True)
    print(" Put your .txt files into ./docs and rerun if empty.\n")
    docs = load_documents()
    if not docs:
        print("No documents found in ./docs. Exiting.")
        exit()
    texts, embeddings, meta = build_index(docs)
    print(f"Ingested {len(texts)} chunks from {len(docs)} documents.\n")
    while True:
        q = input("Ask: ").strip()
        if not q or q.lower() in {"exit", "quit"}:
            break
        answer(q, texts, embeddings, meta)



