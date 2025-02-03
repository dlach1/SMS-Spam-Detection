import string
import email
import math
import numpy as np
from collections import defaultdict
import re

TRAINING_SET_RATIO = 0.73
TOTAL_SET = 1
STOP_WORDS = {'to', 'i', 'you', 'a', 'the', 'u', 'and', 'is', 'in', 'my', 'for', 'your', 'of', 'me', 'have', 'call', 'on', 'are', 'that', 'it', '2', 'so', 'but', 'or', 'not', 'at', 'ur', 'can', 'if', 'with', 'will', "i'm", 'be', 'get', 'just', 'do', 'we', 'this', 'when', 'from', '&lt;#&gt;', 'go', 'up', 'all', 'no', '4', 'how', 'what', 'now', '.', 'like', 'got', 'know', 'was', 'free', 'out', 'come', 'am', 'its', 'then', 'good', 'send', '?', 'only', 'want', 'he', 'as', 'text', 'time', "i'll", 'by', 'love', '...', 'going', 'ok', 'ü', 'need', 'about', 'r', 'still', 'one', 'txt', 'n', 'see', 'our', 'dont', "don't", 'new', 'there', 'tell', 'she', 'been', 'any', 'think', 'reply', 'they', 'mobile', 'take', 'back', 'stop', 'some', 'please', 'has', 'did', 'home', 'an', '&', 'day', 'who', 'claim', 'her', 'hope', 'hi', 'had', 'make', 'give', 'pls', 'more', 'where', 'me.', 'd', 'phone', "it's", 'should', 'later', 'now.', 'much', 'him', 'happy', '-', 'great', 'sorry', 'after', 'ask', '&amp;', 'dear', 'you.', 'hey', 'da', 'say', 'well', 'e', 'really', 'im', 'here', 'last', 'way', 'very', 'meet', 'why', 'now!', 'night', 'miss', 'would', 'cos', 'c', 'too', 'today', 'oh', 'every', 'find', 'week', 'let', 'pick', 'them', 'number', 'win', 'work', 'contact', 'lor.', 'doing', 'nokia', 'said', 'right', "i've", 'cash', 'sent', 'keep', 'won', '1', 'cant', 'even', 'b', 'yeah', 'wat', 'thanks', 'also', 'message', 'were', 'went', 'next', 'his', 'anything', 'could', 'which', 'lol', 'feel', 'buy', 'gud', 'many'}
CURRENCY_CHARACTERS = ['$', '€', '£', '¥', '₹', '₩', '₽', '₺', '฿', '₫', '₴', '₦', '₲', '₵', '₡', '₱', '₭', '₮', '₦', '₳', '₣', '₤', '₧', '₯']

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

def replace_digits(word):
    return re.sub(r'\d{4,}', lambda x: '1' * len(x.group()), word)
words = [[replace_digits(word) for word in word_list] for word_list in words]

def replace_currency(word):
    for char in CURRENCY_CHARACTERS:
        word = word.replace(char, '$')
    return word
words = [[replace_currency(word) for word in word_list] for word_list in words]

def lowercase(word):
    return word.lower()
words = [[lowercase(word) for word in word_list] for word_list in words]

def remove_common(word):
    return word if word not in STOP_WORDS else ""
words = [[remove_common(word) for word in word_list] for word_list in words]



# Split the data into training and test sets
train = words[:int(len(words)*TRAINING_SET_RATIO*TOTAL_SET)]
test = words[int(len(words)*TRAINING_SET_RATIO*TOTAL_SET):int(len(words)*TOTAL_SET)]

# Identify the list of unique terms in the train set
unique_terms = set()
for tokens in train:
    unique_terms.update(tokens)

# Calculate the inverse document frequency (IDF) for each term in the train set
def calculate_idf(term, train_set):
    num_docs_with_term = sum(1 for doc in train_set if term in doc)
    return math.log(len(train_set) / (1 + num_docs_with_term))

idf = {term: calculate_idf(term, train) for term in unique_terms}

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
    knn = find_knn(k, test_tf[test_index], train_tfidf)
    total_spam = 0
    total_ham = 0
    for i in range(len(knn)):
        if (label[knn[i][0]] == 'spam' and knn[i][1] != 0):
            total_spam += 1
        elif (label[knn[i][0]] == 'ham' and knn[i][1] != 0):
            total_ham += 1 
    if (total_ham > total_spam):
        return "ham"
    return "spam"

k = 5

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
    else:
        "ERROR: Neither spam nor ham"

print("True Positives:", correct_spam)
print("False Positives:", total_ham - correct_ham)
print("True Negatives:", correct_ham)
print("False Negatives:", total_spam - correct_spam)

print("Accuracy:", (correct_spam + correct_ham) / (total_spam + total_ham))
print("Precision:", correct_spam / total_spam)
print("Recall:", correct_spam / (correct_spam + total_ham - correct_ham))
print("F1 Score:", 2 * (correct_spam / total_spam) * (correct_spam / (correct_spam + total_ham - correct_ham)) / ((correct_spam / total_spam) + (correct_spam / (correct_spam + total_ham - correct_ham))))
