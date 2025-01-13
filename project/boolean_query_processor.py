import json

# Load the inverted index
with open('inverted_index.json', 'r', encoding='utf-8') as file:
    inverted_index = json.load(file)

def boolean_query_processor(query, inverted_index):
    """
    Process a Boolean query and return matching document IDs.
    """
    def parse_query(query):
        # Split the query into terms and operators
        tokens = query.split()
        terms = []
        operators = []
        for token in tokens:
            if token in {"AND", "OR", "NOT"}:
                operators.append(token)
            else:
                terms.append(token)
        return terms, operators

    def get_documents(term):
        # Get documents for a term from the inverted index
        return set(inverted_index.get(term, []))

    terms, operators = parse_query(query)
    if not terms:
        return set()  # No terms, return empty result

    # Initialize the result set with the first term
    result = get_documents(terms[0])

    # Process operators and combine results
    for i, operator in enumerate(operators):
        next_term_docs = get_documents(terms[i + 1])
        if operator == "AND":
            result = result.intersection(next_term_docs)
        elif operator == "OR":
            result = result.union(next_term_docs)
        elif operator == "NOT":
            result = result.difference(next_term_docs)

    return result

# Example test
query = "python AND java"
matching_docs = boolean_query_processor(query, inverted_index)
print(f"Documents matching '{query}': {matching_docs}")
