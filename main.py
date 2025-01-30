import string
import email
import math
import numpy as np
from collections import defaultdict

TRAINING_SET_RATIO = 0.7
TOTAL_SET = 1

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
train = words[:int(len(words)*TRAINING_SET_RATIO*TOTAL_SET)]
test = words[int(len(words)*TRAINING_SET_RATIO*TOTAL_SET):int(len(words)*TOTAL_SET)]

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

# Calculate the TF-IDF for each term in the
train_tfidf = []
for doc_tf in train_tf:
    doc_tfidf = {term: tf * idf[term] for term, tf in doc_tf.items()}
    train_tfidf.append(doc_tfidf)


def euclidean_distance(vec1, vec2): 
    total = 0
    for term in vec1:
        if term in vec2:
            total += (vec1[term] - vec2[term]) ** 2
    return math.sqrt(total)

def find_knn(k, test_set, train_tfidf):
    distances = dict()
    for i in range(len(train_tfidf)):
        distances.update({i: euclidean_distance(test_set, train_tfidf[i])})
    sorted_distances = sorted(distances.items(), key=lambda item: item[1], reverse=True)
    return sorted_distances[:k]

TEST_START_INDEX = int(len(words)*TRAINING_SET_RATIO*TOTAL_SET)
def categorize(k, test_index, train_tfidf):
    knn = find_knn(5, test_tf[test_index], train_tfidf)
    total_spam = 0
    total_ham = 0
    for i in range(len(knn)):
        if (label[knn[i][0]] == 'spam'):
            total_spam += 1
        elif (label[knn[i][0]] == 'ham'):
            total_ham += 1 
    if (total_spam > total_ham):
        return "spam"
    return "ham"

k = 10

correct_spam = 0
correct_ham = 0
total_spam = 0
total_ham = 0
for i in range(0, len(lines)-TEST_START_INDEX):
    indexed_label = categorize(k, i, train_tfidf)

    if (label[i+TEST_START_INDEX] == "spam"):
        if (indexed_label == "spam"):
            correct_spam += 1
        total_spam += 1
    elif (label[i+TEST_START_INDEX] == "ham"):
        if (indexed_label == "ham"):
            correct_ham += 1
        total_ham += 1

print("True Positives:", correct_spam)
print("False Positives:", total_ham - correct_ham)
print("True Negatives:", correct_ham)
print("False Negatives:", total_spam - correct_spam)

print("Accuracy:", (correct_spam + correct_ham) / (total_spam + total_ham))
print("Precision:", correct_spam / total_spam)
print("Recall:", correct_spam / (correct_spam + total_ham - correct_ham))
print("F1 Score:", 2 * (correct_spam / total_spam) * (correct_spam / (correct_spam + total_ham - correct_ham)) / ((correct_spam / total_spam) + (correct_spam / (correct_spam + total_ham - correct_ham))))