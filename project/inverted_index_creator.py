import json

# Load the preprocessed data
with open('processed_programming_languages_text.json', 'r', encoding='utf-8') as file:
    processed_data = json.load(file)

# Initialize the inverted index
inverted_index = {}

# Create the inverted index
for doc_id, text in processed_data.items():
    # Split the text into words
    words = text.split()
    
    for word in words:
        # Add the word to the inverted index
        if word not in inverted_index:
            inverted_index[word] = []  # Initialize an empty list for the word
        if doc_id not in inverted_index[word]:
            inverted_index[word].append(doc_id)

# Save the inverted index to a file
output_index_path = 'inverted_index.json'
with open(output_index_path, 'w', encoding='utf-8') as file:
    json.dump(inverted_index, file, ensure_ascii=False, indent=4)

print(f"Inverted index has been saved to {output_index_path}")
