""" 
    
    Written as a little "test drive" of the two cool Python features, 
       Requests, for dealing with APIs
       NLTK, for natural language processing

    Author: KEN
    Date:   2023.04.27

 """

import requests
from bs4 import BeautifulSoup, Comment
from io import BytesIO
from nltk import word_tokenize, pos_tag, ne_chunk
import nltk
from nltk.probability import FreqDist


# Needed to fix a certificate issue on MacOS
import os
import certifi
os.environ['SSL_CERT_FILE'] = certifi.where()

# The fun starts here
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

def extract_text_from_page(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Remove script and style elements
        for element in soup(['script', 'style']):
            element.decompose()

        # Remove comments
        for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
            comment.extract()

        # Extract text from the remaining elements
        text = soup.get_text(separator=' ')

        # Replace consecutive whitespace characters with a single space
        clean_text = ' '.join(text.split())

        return clean_text
    else:
        print(f"Error: Unable to fetch data from the website. Status code: {response.status_code}")
        return None

def analyze_text(text):
    # Tokenization
    tokens = word_tokenize(text)
    # print(f"Tokens: {tokens}\n")

    # Part-of-speech tagging
    pos_tags = pos_tag(tokens)
    # print(f"Part-of-speech tags: {pos_tags}\n")

    # Named entity recognition
    named_entities = ne_chunk(pos_tags)
    #print(f"Named entities: {named_entities}")

 # Convert tokens to lowercase and filter out non-alphabetic tokens
    words = [token.lower() for token in tokens if token.isalpha()]

    # Calculate word frequency
    freq_dist = FreqDist(words)
    print(f"Word frequency: {freq_dist}\n")

    # Display the top 10 most frequent words
    print("Top 10 most frequent words:")
    for word, count in freq_dist.most_common(10):
        print(f"{word}: {count}")

url = 'https://cnn.com/blog'
text_content = extract_text_from_page(url)

if text_content:
    print( "\n\n *** THIS IS THE TEXT CONTENT ***\n")
    print(text_content)
    print( "\n\n *** THIS IS THE ANALYSIS ***\n")
    analyze_text(text_content)




   
