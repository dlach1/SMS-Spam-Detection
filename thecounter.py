import threading
from collections import Counter
import queue
import json

# Number of threads to use
NUM_THREADS = 4

# Thread-safe queue to store lines
line_queue = queue.Queue()

# Dictionary to store word counts (thread-safe)
word_counts = Counter()

# Define stop words to ignore
# STOP_WORDS = {"and", "the", "but", "or", "if", "so", "it"}

def process_lines():
    local_counter = Counter()
    while True:
        try:
            line = line_queue.get(timeout=3)  # Get a line from the queue
        except queue.Empty:
            break  # Exit if the queue is empty

        words = line.strip().split()[1:]  # Skip the first word (ham/spam)
        words = [word.lower() for word in words]  # Convert to lowercase & filter

        local_counter.update(words)  # Count words locally

    # Merge local counter into global counter
    global word_counts
    with threading.Lock():
        word_counts.update(local_counter)

def main(file_path, output_json):
    # Read file and add lines to the queue
    with open(file_path, "r", encoding="utf-8") as f:
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

    # Get the 100 most common words
    most_common_words = dict(word_counts.most_common(100))

    # Save to JSON file
    with open(output_json, "w", encoding="utf-8") as json_file:
        json.dump(most_common_words, json_file, indent=4)

    print(f"Saved the 100 most common words to {output_json}")

if __name__ == "__main__":
    file_path = r"SMSSpamCollection.txt"
    output_json = r"C:\Users\Garrett\Documents\Class - School\Machine-Learning\ML_Assignment1\word_counts.json"
    main(file_path, output_json)
