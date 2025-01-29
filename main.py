import string
import email
import math
from collections import defaultdict

TRAINING_SET_RATIO = 0.7

# Read all the lines in SMSSpamCollection to a list
file_path = 'SMSSpamCollection'

with open(file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()

words = []
label = []
# Print the lines to verify
for line in lines:
    label.append(line.strip().split()[0])
    words.append(line.strip().split()[1:])

# Remove punctuation and words that are only punctuation
cleaned_words = []
for tokens in words:
    cleaned_tokens = [word.strip(string.punctuation) for word in tokens if word.strip(string.punctuation)]
    cleaned_words.append(cleaned_tokens)

words = cleaned_words

# Split the data into training and test sets
train = words[:int(len(words)*TRAINING_SET_RATIO)]
test = words[int(len(words)*TRAINING_SET_RATIO):]

# Identify the list of unique terms in the train set
unique_terms = set()
for tokens in train:
    unique_terms.update(tokens)

# print("Unique terms in the training set:", unique_terms)

# Calculate the inverse document frequency (IDF) for each term in the train set
def calculate_idf(term, train_set):
    num_docs_with_term = sum(1 for doc in train_set if term in doc)
    return math.log(len(train_set) / (1 + num_docs_with_term))

idf = {term: calculate_idf(term, train) for term in unique_terms}

# print("Inverse Document Frequency (IDF) for each term:", idf)

# Calculate the term frequency (TF) for each term in a document
def calculate_tf(term, document):
    return document.count(term) / len(document)

# Calculate the term frequency for each term in the train set
train_tf = []
for doc in train:
    doc_tf = {term: calculate_tf(term, doc) for term in doc}
    train_tf.append(doc_tf)

# Calculate the term frequency for each term in the test set
test_tf = []
for doc in test:
    doc_tf = {term: calculate_tf(term, doc) for term in doc}
    test_tf.append(doc_tf)

# print("Term Frequency (TF) for each term in the training set:", train_tf)
# print("Term Frequency (TF) for each term in the test set:", test_tf)

# Calculate the TF-IDF for each term in the train set
train_tfidf = []
for doc_tf in train_tf:
    doc_tfidf = {term: tf * idf[term] for term, tf in doc_tf.items()}
    train_tfidf.append(doc_tfidf)

print("TF-IDF for each term in the training set:", train_tfidf)

