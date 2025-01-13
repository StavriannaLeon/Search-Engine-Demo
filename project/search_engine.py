import json
from tfidf_ranking import compute_tf_idf
from boolean_query_processor import boolean_query_processor
from rank_bm25 import BM25Okapi

# Load the inverted index
with open("inverted_index.json", "r", encoding="utf-8") as f:
    inverted_index = json.load(f)

# Load the processed data
with open("processed_programming_languages_text.json", "r", encoding="utf-8") as f:
    processed_data = json.load(f)

# Function for BM25 ranking
def bm25_ranking(query, matching_docs, processed_data):
    tokenized_docs = [doc.split() for doc in processed_data.values()]
    bm25 = BM25Okapi(tokenized_docs)
    query_tokens = query.split()
    scores = bm25.get_scores(query_tokens)
    
    doc_score_pairs = [(doc, score) for doc, score in zip(processed_data.keys(), scores) if doc in matching_docs]
    ranked_results = sorted(doc_score_pairs, key=lambda x: x[1], reverse=True)
    
    return [doc for doc, _ in ranked_results]

# Main search engine function
def search_engine():
    print("Welcome to the Search Engine!")
    print("Type your query using Boolean operators (AND, OR, NOT).")
    print("Example: python AND java OR javascript\n")
    
    while True:
        query = input("Enter your query (or type 'exit' to quit): ").strip()
        if query.lower() == "exit":
            print("Goodbye!")
            break

        # Process query using Boolean retrieval
        matching_docs = boolean_query_processor(query, inverted_index)
        if not matching_docs:
            print(f"No documents matched your query: {query}")
            continue

        print(f"\nDocuments matching '{query}': {matching_docs}")

        # Allow user to choose ranking method
        print("\nChoose a ranking method:")
        print("1. Boolean Retrieval (Default)")
        print("2. TF-IDF Ranking")
        print("3. BM25 Ranking")
        choice = input("Enter the number of your choice (1, 2, or 3): ").strip()

        if choice == "2":
            ranked_docs = compute_tf_idf(query, matching_docs, processed_data)
            print("\nTF-IDF Ranked Results:")
        elif choice == "3":
            ranked_docs = bm25_ranking(query, matching_docs, processed_data)
            print("\nBM25 Ranked Results:")
        else:
            ranked_docs = list(matching_docs)
            print("\nBoolean Retrieval Results:")

        # Display ranked results
        for rank, doc in enumerate(ranked_docs, start=1):
            print(f"{rank}. {doc}")

# Run the search engine
if __name__ == "__main__":
    search_engine()
