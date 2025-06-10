import os
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from core.parser import parse_repo
from core.utillls import load_config

CONFIG = load_config()

EMBEDDING_MODEL = CONFIG['embedding']['model']
VECTOR_DIR = CONFIG['vector_store']['persist_directory']
IGNORE_PATHS = CONFIG.get('ignore_paths', [])

class VectorStore:
    def __init__(self):
        self.model = SentenceTransformer(EMBEDDING_MODEL)
        self.index = None
        self.docstore = []

    def embed_texts(self, texts):
        """Embed a list of texts into vectors."""
        embeddings = self.model.encode(texts, convert_to_numpy=True, show_progress_bar=True)
        # Ensure embeddings is always 2D
        if embeddings.ndim == 1:
            embeddings = np.expand_dims(embeddings, axis=0)
        return embeddings

    def build_index(self, docs):
        """Build FAISS index from docs (list of dict with 'content')."""
        texts = [doc['content'] for doc in docs]
        embeddings = self.embed_texts(texts)
        
        print(f"Embeddings shape: {embeddings.shape}")  # Debug line

        if embeddings.shape[0] == 0:
            raise ValueError("No embeddings were created. Check document contents.")

        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(embeddings)

        self.docstore = docs
        self.save_index()

    def save_index(self):
        os.makedirs(VECTOR_DIR, exist_ok=True)
        faiss.write_index(self.index, os.path.join(VECTOR_DIR, "index.faiss"))
        with open(os.path.join(VECTOR_DIR, "docstore.pkl"), "wb") as f:
            pickle.dump(self.docstore, f)
        print(f"Saved FAISS index and documents to {VECTOR_DIR}")

    def load_index(self):
        index_path = os.path.join(VECTOR_DIR, "index.faiss")
        docstore_path = os.path.join(VECTOR_DIR, "docstore.pkl")

        if not os.path.exists(index_path) or not os.path.exists(docstore_path):
            raise FileNotFoundError("Vector store files not found. Please build the index first.")

        self.index = faiss.read_index(index_path)
        with open(docstore_path, "rb") as f:
            self.docstore = pickle.load(f)
        print(f"Loaded FAISS index and documents from {VECTOR_DIR}")

    def search(self, query, k=3):
        """Search for top k relevant documents for the query."""
        query_vec = self.model.encode([query], convert_to_numpy=True)
        distances, indices = self.index.search(query_vec, k)
        results = [self.docstore[idx] for idx in indices[0]]
        return results


# Singleton instance
vector_store_instance = VectorStore()


def build_vector_store(repo_path=None):
    """
    Parse repo files and build/save the vector index.
    If repo_path is None, it will get path from github_loader.
    """
    if repo_path is None:
        from core.github_loader import get_repository
        repo_path = get_repository()

    # Parse repo to get list of documents
    docs = parse_repo(repo_path)

    # Filter out any docs that are empty or ignored
    docs = [doc for doc in docs if doc['content'].strip() != '']

    if not docs:
        raise ValueError("No valid documents found to index. Ensure the repo is not empty or ignored.")

    vector_store_instance.build_index(docs)


def load_vector_store():
    """
    Load the FAISS index and document metadata.
    Returns the FAISS index.
    """
    vector_store_instance.load_index()
    return vector_store_instance.index


def embed_query(query):
    """
    Embed a single query string to vector.
    """
    return vector_store_instance.model.encode([query], convert_to_numpy=True)
