# Dan Lechance, Garrett Thompson , Hal Williams 
# AI Usage Statement
# Tools Used: None
# Prohibited Use Compliance: Confirmed
import math
import re

# Define constants including the ratio for training set and currency characters
TRAINING_SET_RATIO = 0.7
CURRENCY_CHARACTERS = ['$', '€', '£', '¥', '₹', '₩', '₽', '₺', '฿', '₫', '₴', '₦', '₲', '₵', '₡', '₱', '₭', '₮', '₦', '₳', '₣', '₤', '₧', '₯']

# Read all the lines in SMSSpamCollection to a list
file_path = 'SMSSpamCollection'
with open(file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()

words = []
label = []
# Splits lines into set of word and label
for line in lines:
    label.append(line.strip().split()[0])
    words.append(line.strip().split()[1:])

# Define a function to remove punctuation from a word
def replace_digits(word):
    return re.sub(r'\d{4,}', lambda x: '1' * len(x.group()), word)
words = [[replace_digits(word) for word in word_list] for word_list in words]

# Define a function to remove punctuation from a word
def replace_currency(word):
    for char in CURRENCY_CHARACTERS:
        word = word.replace(char, '$')
    return word
words = [[replace_currency(word) for word in word_list] for word_list in words]

# Define a function to remove punctuation from a word
def lowercase(word):
    return word.lower()
words = [[lowercase(word) for word in word_list] for word_list in words]

# Split the data into training and test sets
train = words[:int(len(words)*TRAINING_SET_RATIO)]
test = words[int(len(words)*TRAINING_SET_RATIO):]

# Identify the list of unique terms in the train set
unique_terms = set()
for tokens in train:
    unique_terms.update(tokens)

# Create dictionaries to count occurrences in spam and ham
spam_counts = {term: 0 for term in unique_terms}
ham_counts = {term: 0 for term in unique_terms}
total_counts = {term: 0 for term in unique_terms}

# Count the occurrences of each term in spam and ham
for i, tokens in enumerate(train):
    if label[i] == 'spam':
        for token in tokens:
            spam_counts[token] += 1
            total_counts[token] += 1
    else:
        for token in tokens:
            ham_counts[token] += 1
            total_counts[token] += 1

# Calculate the probability of each term in spam and ham
prob_spam = {term: 0 for term in unique_terms}
prob_ham = {term: 0 for term in unique_terms}
for term in unique_terms:
    prob_spam[term] = spam_counts[term] / total_counts[term]
    prob_ham[term] = ham_counts[term] / total_counts[term]

TEST_START_INDEX = int(len(words)*TRAINING_SET_RATIO)

# Define a function to classify a set of tokens as spam or ham using naive bayes classification
def classify(tokens, prob_spam, prob_ham):
    spam_probability = 1.0
    ham_probability = 1.0
    for word in tokens:
        if word in unique_terms:
            ham_probability *= prob_ham[word]
            spam_probability *= prob_spam[word]

    if spam_probability > ham_probability:
        return 'spam'
    else:
        return 'ham'
    
# Test the classifier on the test set
correct_spam = 0
correct_ham = 0
total_spam = 0
total_ham = 0
for i in range(0, len(lines)-TEST_START_INDEX):
    indexed_label = classify(test[i], prob_spam, prob_ham)

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
