import requests
from bs4 import BeautifulSoup
import json
import re

# Λίστα με τα 10 URLs
urls = [
    'https://en.wikipedia.org/wiki/Python_(programming_language)',
    'https://en.wikipedia.org/wiki/JavaScript',
    'https://en.wikipedia.org/wiki/Java_(programming_language)',
    'https://en.wikipedia.org/wiki/C_(programming_language)',
    'https://en.wikipedia.org/wiki/Ruby_(programming_language)',
    'https://en.wikipedia.org/wiki/HTML',
    'https://en.wikipedia.org/wiki/C%2B%2B',
    'https://en.wikipedia.org/wiki/Go_(programming_language)',
    'https://en.wikipedia.org/wiki/Swift_(programming_language)',
    'https://en.wikipedia.org/wiki/Kotlin'
]

# Συνάρτηση για να τραβήξουμε δεδομένα από κάθε URL
def crawl_page(url):
    print(f"Crawling: {url}")
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Εξαγωγή όλων των λέξεων από την σελίδα
            # Επιλέγουμε τα tags που περιέχουν κείμενο: p (paragraphs), li (list items), span, a (links) και άλλα
            text = []
            for tag in soup.find_all(['p', 'li', 'span', 'a', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
                text.append(tag.get_text())
            
            # Συνενώνουμε όλα τα κείμενα και καθαρίζουμε από περιττά κενά
            full_text = ' '.join(text)
            # Καθαρισμός κειμένου (π.χ. αφαιρούμε περιττές λευκές περιοχές)
            cleaned_text = re.sub(r'\s+', ' ', full_text).strip()
            
            return cleaned_text
        else:
            print(f"Failed to retrieve {url}")
            return ""
    except Exception as e:
        print(f"Error while crawling {url}: {e}")
        return ""

# Δημιουργία λεξικού για αποθήκευση του πλήρους κειμένου ανά URL
text_dict = {}

# Κάνουμε crawl τις 10 σελίδες
for url in urls:
    page_text = crawl_page(url)
    text_dict[url] = page_text

# Αποθήκευση των δεδομένων σε αρχείο JSON
with open('programming_languages_text.json', 'w') as file:
    json.dump(text_dict, file, indent=4)

print("Data saved to programming_languages_text.json")
