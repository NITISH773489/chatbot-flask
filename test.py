import python
import nltk
from nltk.stem import WordNetLemmatizer
import re
import datetime # For logging timestamps
import os # To manage the log file directory
# Removed Tkinter imports as the GUI part is being removed

# --- NLTK Data Downloads (Corrected Error Handling) ---
# These try-except blocks will attempt to download necessary NLTK data
# if it's not found on your system.
try:
    nltk.data.find('tokenizers/punkt')
except Exception: # Changed from nltk.downloader.DownloadError
    print("Downloading NLTK 'punkt' tokenizer (for tokenization)...")
    nltk.download('punkt')
try:
    nltk.data.find('corpora/wordnet')
except Exception: # Changed from nltk.downloader.DownloadError
    print("Downloading NLTK 'wordnet' corpus (for lemmatization)...")
    nltk.download('wordnet')
try:
    nltk.data.find('corpora/omw-1.4')
except Exception: # Changed from nltk.downloader.DownloadError
    print("Downloading NLTK 'omw-1.4' corpus (Open Multilingual WordNet)...")
    nltk.download('omw-1.4')

# --- Chatbot Core Logic ---
lemmatizer = WordNetLemmatizer()

patterns_responses = {
    "hello": "Hi there! How can I help you today?",
    "hi": "Hello! Nice to chat with you.",
    "how are you": "I'm a bot, so I don't have feelings, but I'm functioning well!",
    "what is your name": "I am a simple chatbot created to assist you.",
    "age": "I don't have an age. I was just programmed.",
    "bye": "Goodbye! Have a great day!",
    "thank you": "You're welcome!",
    "help": "I can answer basic questions about myself. You can also ask me to 'search for' something.",
    "python": "Python is a popular programming language. Are you learning Python?",
    "learn": "Learning is fun! What do you want to learn?",
    "default": "I'm sorry, I don't understand. Can you please rephrase that?",
    "colending": "Its a joint lending arrangement among REs typically in the ratio of 80:20",
    "co lending": "Its a joint lending arrangement among REs typically in the ratio of 80:20",
    "Naam": "Naam me kya rakha hai"
}

def preprocess_input(text):
    """
    Tokenizes, lowercases, and lemmatizes the input text using NLTK.
    """
    text = text.lower() # Convert to lowercase
    tokens = nltk.word_tokenize(text) # Tokenize the text into words
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in tokens] # Lemmatize each word
    return lemmatized_tokens

def get_response(user_input):
    """
    Determines the chatbot's response based on predefined patterns and simulated search.
    """
    processed_input = preprocess_input(user_input)

    # Simulated Google Search Integration Logic
    # Checks for phrases like "search for..." or "what is..."
    if "search" in processed_input and "for" in processed_input:
        search_query_parts = []
        try:
            for_index = processed_input.index("for")
            search_query_parts = processed_input[for_index + 1:]
        except ValueError:
            pass # "for" not found after "search"

        if search_query_parts:
            query = " ".join(search_query_parts)
            # In a real-world scenario, you would integrate with a Google Search API here.
            # For this example, we provide a simulated response.
            return f"Searching for '{query}'... (Simulated result: Found some interesting facts about '{query}'.)"
        else:
            return "What specifically would you like me to search for?"

    if "what" in processed_input and "is" in processed_input and len(processed_input) > 2:
        try:
            what_index = processed_input.index("what")
            is_index = processed_input.index("is")
            if is_index == what_index + 1: # Ensures "what is" are consecutive words
                query_parts = processed_input[is_index + 1:]
                if query_parts:
                    query = " ".join(query_parts)
                    return f"Searching for '{query}'... (Simulated result: The definition of '{query}' is [insert brief definition here].)"
        except ValueError:
            pass # "what" or "is" not found sequentially

    # Rule-Based Response Logic
    # Iterates through predefined patterns to find a match
    for pattern, response in patterns_responses.items():
        # Preprocess the pattern for comparison
        pattern_words = preprocess_input(pattern)

        # Check if the exact multi-word pattern is present as a substring in the original user input
        # This is often a more robust way to match phrases than checking for individual words
        if pattern.lower() in user_input.lower():
             return response

        # Fallback to checking if all words in a multi-word pattern are present
        # This might match incorrectly if the words appear out of order or far apart,
        # but is included based on the original code's logic.
        if all(word in processed_input for word in pattern_words) and len(pattern_words) > 1:
            return response
            
        # Direct keyword match (for single-word patterns or if the above fails)
        if pattern in processed_input:
             return response


    return patterns_responses["default"] # Default response if no match is found

# --- Interaction Logging Function ---
LOG_FILE = "chatbot_interactions.log"

def log_interaction(user_question, bot_response):
    """
    Logs the user's question and the chatbot's response to a text file.
    Each interaction is timestamped for analysis.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        # 'a' mode appends to the file if it exists, creates it if it doesn't
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] User: {user_question}\n")
            f.write(f"[{timestamp}] Bot: {bot_response}\n")
            f.write("-" * 50 + "\n") # Add a separator for readability
    except IOError as e:
        print(f"Error writing to log file {LOG_FILE}: {e}")

# Removed the entire Tkinter GUI setup and mainloop
# You can now interact with the chatbot functions directly from notebook cells

# Example of how to interact with the chatbot from the notebook:
# user_input = "hello"
# bot_response = get_response(user_input)
# print(f"You: {user_input}")
# print(f"Chatbot: {bot_response}")
# log_interaction(user_input, bot_response)

# user_input = "what is colending"
# bot_response = get_response(user_input)
# print(f"You: {user_input}")
# print(f"Chatbot: {bot_response}")
# log_interaction(user_input, bot_response)