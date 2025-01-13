import json
import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer

# Download required NLTK resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Set the input and output file paths
input_json_path = 'programming_languages_text.json'
output_json_path = 'processed_programming_languages_text.json'

# Load stopwords
stop_words = set(stopwords.words('english'))

# Initialize stemmer and lemmatizer
stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

# Debug: Print the stopwords set
print("Stopwords used:", stop_words)

# Define a function to clean the text
def clean_text(text):
    # Tokenize the text into words
    words = word_tokenize(text)
    
    # Remove stopwords and punctuation
    cleaned_words = [
        word.lower() for word in words 
        if word.lower() not in stop_words and word not in string.punctuation
    ]
    
    # Stemming
    stemmed_words = [stemmer.stem(word) for word in cleaned_words]
    
    # Lemmatization
    lemmatized_words = [lemmatizer.lemmatize(word) for word in stemmed_words]
    
    # Join the cleaned, stemmed, and lemmatized words back into a string
    return ' '.join(lemmatized_words)

# Read the input JSON file
with open(input_json_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Process the text data and save the cleaned version only
processed_data = {}
for key, value in data.items():
    processed_value = clean_text(value)
    processed_data[key] = processed_value

# Save the processed data to the output JSON file
with open(output_json_path, 'w', encoding='utf-8') as file:
    json.dump(processed_data, file, ensure_ascii=False, indent=4)

print(f"Processed data has been saved to {output_json_path}")
