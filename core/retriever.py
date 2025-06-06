# agent/retriever.py

from core.vector_store import load_vector_store, embed_query


def get_relevant_chunks(query: str, k: int = 5):
    vector_db = load_vector_store()
    query_vector = embed_query(query)

    # Perform similarity search
    scores, indices = vector_db.search(query_vector, k)

    documents = []
    for idx in indices[0]:
        doc = vector_db.docstore[idx]
        documents.append(doc)

    return documents


# Example usage
if __name__ == '__main__':
    results = get_relevant_chunks("Create MVC for header")
    for r in results:
        print("\n---\n")
        print(r['file_path'])
        print(r['content'][:300])
