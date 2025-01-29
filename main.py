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

#Removes punctuation
for tokens in words:
    tokens = [i.strip("".join(string.punctuation)) for i in tokens if i not in string.punctuation]
    # print(tokens)

# Split the data into training and test sets
train = words[:int(len(words)*TRAINING_SET_RATIO)]
test = words[int(len(words)*TRAINING_SET_RATIO):]

# Calculate term frequency for each document
def term_frequency(document):
    tf = defaultdict(int)
    for word in document:
        tf[word] += 1
    return tf

# Calculate document frequency for each term
def document_frequency(docs):
    df = defaultdict(int)
    for doc in docs:
        unique_terms = set(doc)
        for term in unique_terms:
            df[term] += 1
    return df

# Calculate inverse document frequency for each term
def inverse_document_frequency(docs):
    N = len(docs)
    df = document_frequency(docs)
    idf = {}
    for term, freq in df.items():
        idf[term] = math.log(N / (1 + freq))
    return idf

# Calculate IDF for the training set
idf = inverse_document_frequency(train)
print(idf)

# Calculate TF for the training set
tf = term_frequency(train)

# Calculate TF-IDF for the training set
tf_idf = td * idf

