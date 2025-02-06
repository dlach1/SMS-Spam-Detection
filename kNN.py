import math
import thecounter
import re
import matplotlib.pyplot as plt

# Define the constants for the kNN model 
# These include the training set ratio, the stop words (words to not be looked at), and the currency characters
TRAINING_SET_RATIO = 0.7
STOP_WORDS = thecounter.get_most_common_words(50)
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

#Beginning of tokenization

#Replace all of the digits in the words with the number 1
def replace_digits(word):
    return re.sub(r'\d{4,}', lambda x: '1' * len(x.group()), word)
words = [[replace_digits(word) for word in word_list] for word_list in words]

#Replace all of the currency characters with the dollar sign
def replace_currency(word):
    for char in CURRENCY_CHARACTERS:
        word = word.replace(char, '$')
    return word
words = [[replace_currency(word) for word in word_list] for word_list in words]

#Convert all of the words to lowercase
def lowercase(word):
    return word.lower()
words = [[lowercase(word) for word in word_list] for word_list in words]

#Remove all of the common words from the list of words
def remove_common(word):
    return word if word not in STOP_WORDS else ""
words = [[remove_common(word) for word in word_list] for word_list in words]



# Split the data into training and test sets
train = words[:int(len(words)*TRAINING_SET_RATIO)]
test = words[int(len(words)*TRAINING_SET_RATIO):]

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

# Calculate the Euclidean distance between two vectors
def euclidean_distance(vec1, vec2): 
    total = 0
    for term in vec1:
        if term in vec2:
            total += (vec1[term] - vec2[term]) ** 2
    return math.sqrt(total)

# Calculate the Manhattan distance between two vectors
def manhattan_distance(vec1, vec2):
    total = 0
    for term in vec1:
        if term in vec2:
            total += abs(vec1[term] - vec2[term])
    return total

# Calculate the Minkowski distance between two vectors
def minkowski_distance(vec1, vec2):
    total = 0
    for term in vec1:
        if term in vec2:
            total += abs(vec1[term] - vec2[term]) ** 3
    return total ** (1 / 3)

# Find the k nearest neighbors of a test set in the training set
def find_knn(k, test_set, train_tfidf, distance_function=euclidean_distance):
    distances = dict()
    for i in range(len(train_tfidf)):
        distances.update({i: distance_function(test_set, train_tfidf[i])})
    sorted_distances = sorted(distances.items(), key=lambda item: item[1], reverse=True)
    return sorted_distances[:k]

TEST_START_INDEX = int(len(words)*TRAINING_SET_RATIO)

# Categorize a test set using kNN
def categorize_knn(k, test_index, train_tfidf, distance_function=euclidean_distance):
    knn = find_knn(k, test_tf[test_index], train_tfidf, distance_function)
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

# Evaluate the kNN model using the test set
def evaluate(k, print_results=True, distance_function=euclidean_distance):
    correct_spam = 0
    correct_ham = 0
    total_spam = 0
    total_ham = 0
    for i in range(0, len(lines)-TEST_START_INDEX):
        indexed_label = categorize_knn(k, i, train_tfidf, distance_function)

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

    F1_Score = 2 * (correct_spam / total_spam) * (correct_spam / (correct_spam + total_ham - correct_ham)) / ((correct_spam / total_spam) + (correct_spam / (correct_spam + total_ham - correct_ham)))
    if print_results:
        print("True Positives:", correct_spam)
        print("False Positives:", total_ham - correct_ham)
        print("True Negatives:", correct_ham)
        print("False Negatives:", total_spam - correct_spam)

        print("Accuracy:", (correct_spam + correct_ham) / (total_spam + total_ham))
        print("Precision:", correct_spam / total_spam)
        print("Recall:", correct_spam / (correct_spam + total_ham - correct_ham))
        print("F1 Score:", F1_Score)
    return F1_Score

# print("Euclidean Distance")
# evaluate(5, True, euclidean_distance)
# print("\nManhattan Distance")
# evaluate(5, True, manhattan_distance)
# print("\nMinkowski Distance")
# evaluate(5, True, minkowski_distance)

manhattan_results = []
euclidean_results = []
minkowski_results = []

for i in range(1, 16, 2):
    manhattan_results.append(evaluate(i, False, manhattan_distance))
    euclidean_results.append(evaluate(i, False, euclidean_distance))
    minkowski_results.append(evaluate(i, False, minkowski_distance))
    print("k =", i, "done")

# Plot the results using matplotlib
k_values = [i for i in range(1, 16, 2)]

plt.plot(k_values, manhattan_results, label='Manhattan Distance', marker='o')
plt.plot(k_values, euclidean_results, label='Euclidean Distance', marker='x')
plt.plot(k_values, minkowski_results, label='Minkowski Distance', marker='^')
plt.ylim(0.1, 1)
plt.xlabel('k')
plt.ylabel('F1 Score')
plt.title('F1 Score vs k for Manhattan, Euclidean, and Minkowski (p=3) Distances')
plt.legend()
plt.grid(True)
plt.show()