import threading
from collections import Counter
import queue

# Number of threads to use
NUM_THREADS = 4

# Thread-safe queue to store lines
line_queue = queue.Queue()

# Dictionary to store word counts (thread-safe)
word_counts = Counter()

# List of stop words to remove
STOP_WORDS = {}

def process_lines():
    local_counter = Counter()
    while True:
        try:
            line = line_queue.get(timeout=3)  # Get a line from the queue
        except queue.Empty:
            break  # Exit if the queue is empty

        words = line.strip().split()[1:]  # Skip the first word (ham/spam)
        words = [word.lower() for word in words if word.lower() not in STOP_WORDS]  # Convert to lowercase & filter

        local_counter.update(words)  # Count words locally

    # Merge local counter into global counter
    global word_counts
    with threading.Lock():
        word_counts.update(local_counter)

def get_most_common_words(number_words):
    # Read file and add lines to the queue
    with open(f'SMSSpamCollection', "r", encoding="utf-8") as f:
        for line in f:
            line_queue.put(line)

    # Create and start worker threads
    threads = []
    for _ in range(NUM_THREADS):
        t = threading.Thread(target=process_lines)
        t.start()
        threads.append(t)

    # Wait for all threads to complete
    for t in threads:
        t.join()

    # Return the 1750 most common words as a set
    return set(word for word, _ in word_counts.most_common(number_words))

if __name__ == "__main__":
    file_path = r"C:\Users\Garrett\Documents\Class - School\Machine-Learning\ML_Assignment1\SMSSpamCollection"
    top_words_set = get_most_common_words(file_path)
    print(top_words_set)  # Print or use the set as needed
