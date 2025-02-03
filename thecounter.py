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
STOP_WORDS={}
# STOP_WORDS = {
#     "and", "the", "but", "or", "if", "so", "it", "a", "to", "of", "in", "for", "on", 
#     "with", "as", "this", "that", "at", "by", "from", "was", "is", "are", "be", "an", 
#     "we", "he", "she", "they", "you", "i", "me", "my", "mine", "our", "ours", "your", 
#     "yours", "their", "theirs", "his", "her", "hers", "its"
# }

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

def main(file_path, output_file):
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

    # Get the 50 most common words
    most_common_words = [word for word, _ in word_counts.most_common(200)]

    # Save to file in Python list syntax
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(str(most_common_words))

    print(f"Saved the 50 most common words to {output_file}")

if __name__ == "__main__":
    file_path = r"C:\Users\Garrett\Documents\Class - School\Machine-Learning\ML_Assignment1\SMSSpamCollection"
    output_file = r"C:\Users\Garrett\Documents\Class - School\Machine-Learning\ML_Assignment1\top_words.py"
    main(file_path, output_file)
