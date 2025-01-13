import json
import os

# Load the inverted index from the JSON file
def load_inverted_index(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found.")
        return None
    with open(file_path, 'r', encoding='utf-8') as f:
        inverted_index = json.load(f)
    return inverted_index


# Function to process boolean queries and return matching documents
def boolean_query_processor(query, inverted_index):
    query_terms = query.lower().split(' ')
    if 'and' in query_terms:
        terms = [term for term in query_terms if term != 'and']
        matching_docs = set(inverted_index.get(terms[0], []))
        for term in terms[1:]:
            matching_docs &= set(inverted_index.get(term, []))
    elif 'or' in query_terms:
        terms = [term for term in query_terms if term != 'or']
        matching_docs = set(inverted_index.get(terms[0], []))
        for term in terms[1:]:
            matching_docs |= set(inverted_index.get(term, []))
    elif 'not' in query_terms:
        terms = [term for term in query_terms if term != 'not']
        matching_docs = set(inverted_index.get(terms[0], []))
        for term in terms[1:]:
            matching_docs -= set(inverted_index.get(term, []))
    else:
        matching_docs = set(inverted_index.get(query_terms[0], []))

    return matching_docs


# Function to calculate precision, recall, and F1-Score
def evaluate_metrics(matching_docs, relevant_docs):
    relevant_doc_keys = set(relevant_docs.keys())
    
    tp = len(matching_docs & relevant_doc_keys)
    fp = len(matching_docs - relevant_doc_keys)
    fn = len(relevant_doc_keys - matching_docs)
    
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    
    return precision, recall, f1_score


# Function to calculate Mean Average Precision (MAP)
def mean_average_precision(query_results, relevant_docs_for_queries):
    average_precision_scores = []
    for query, retrieved_docs in query_results.items():
        relevant_docs = relevant_docs_for_queries.get(query, {})
        ap = average_precision(retrieved_docs, relevant_docs)
        average_precision_scores.append(ap)
    
    map_score = sum(average_precision_scores) / len(average_precision_scores) if average_precision_scores else 0.0
    return map_score


# Function to calculate Average Precision (AP) for a single query
def average_precision(retrieved_docs, relevant_docs):
    retrieved_docs = list(retrieved_docs)
    relevant_docs_set = set(relevant_docs.keys())
    relevant_count = 0
    precision_at_k = []
    
    for i, doc in enumerate(retrieved_docs, start=1):
        if doc in relevant_docs_set:
            relevant_count += 1
            precision_at_k.append(relevant_count / i)
    
    ap = sum(precision_at_k) / len(relevant_docs) if relevant_docs else 0.0
    return ap


# Function to evaluate the search engine for a list of queries
def evaluate_search_engine(inverted_index):
    queries = [
        "python AND java",
        "content OR jump",
        "python NOT java"
    ]
    
    relevant_docs_for_queries = {
        "python AND java": {
            "https://en.wikipedia.org/wiki/Python_(programming_language)": 1,
            "https://en.wikipedia.org/wiki/Java_(programming_language)": 1
        },
        "content OR jump": {
            "https://en.wikipedia.org/wiki/Python_(programming_language)": 1,
            "https://en.wikipedia.org/wiki/JavaScript": 1
        },
        "python NOT java": {
            "https://en.wikipedia.org/wiki/Python_(programming_language)": 1
        }
    }

    query_results = {}
    print("Evaluation Results:\n")
    for query in queries:
        print(f"Query: {query}")
        matching_docs = boolean_query_processor(query, inverted_index)
        relevant_docs = relevant_docs_for_queries.get(query, {})
        precision, recall, f1_score = evaluate_metrics(matching_docs, relevant_docs)
        
        print(f"Matching Documents: {matching_docs}")
        print(f"Precision: {precision:.2f}")
        print(f"Recall: {recall:.2f}")
        print(f"F1-Score: {f1_score:.2f}\n")
        
        # Store query results for MAP calculation
        query_results[query] = matching_docs

    # Calculate Mean Average Precision (MAP)
    map_score = mean_average_precision(query_results, relevant_docs_for_queries)
    print(f"Mean Average Precision (MAP): {map_score:.2f}")


# Main function to load the inverted index and run the evaluation
def main():
    inverted_index = load_inverted_index('inverted_index.json')
    if inverted_index is not None:
        evaluate_search_engine(inverted_index)

if __name__ == "__main__":
    main()
