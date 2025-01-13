import json
from sklearn.feature_extraction.text import TfidfVectorizer

# Load the inverted index
with open('inverted_index.json', 'r', encoding='utf-8') as file:
    inverted_index = json.load(file)

# Load the processed data
with open('processed_programming_languages_text.json', 'r', encoding='utf-8') as file:
    processed_data = json.load(file)

# Function to get matching documents for a query
def get_matching_docs(query):
    query_terms = query.lower().split()
    matching_docs = set()

    for term in query_terms:
        if term in inverted_index:
            matching_docs.update(inverted_index[term])

    return list(matching_docs)

# Function to compute TF-IDF and rank documents
def compute_tf_idf(query, matching_docs, processed_data):
    # Prepare corpus: only include matching docs
    corpus = [processed_data[doc_id] for doc_id in matching_docs]
    
    # Add the query as the last item in the corpus
    corpus.append(query)

    # Use TfidfVectorizer
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)

    # Get the query vector (last row in the matrix)
    query_vector = tfidf_matrix[-1]

    # Compute cosine similarity between query and each document
    cosine_similarities = (tfidf_matrix[:-1] @ query_vector.T).toarray().flatten()

    # Pair each document ID with its similarity score
    ranked_docs = sorted(
        zip(matching_docs, cosine_similarities),
        key=lambda x: x[1],
        reverse=True
    )

    return ranked_docs

if __name__ == "__main__":
    # Prompt the user to enter a query
    query = input("Enter your query (TF-IDF ranking): ").strip()

    # Get matching documents
    matching_docs = get_matching_docs(query)
    
    if not matching_docs:
        print("No matching documents found.")
    else:
        # Compute and rank documents using TF-IDF
        ranked_docs = compute_tf_idf(query, matching_docs, processed_data)

        # Display the results
        print("\nRanked results:")
        for doc_id, score in ranked_docs:
            print(f"{doc_id}: {score:.4f}")
