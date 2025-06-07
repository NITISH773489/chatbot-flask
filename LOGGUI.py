import nltk
nltk.download('punkt')
print("NLTK is working!")
import tkinter as tk
from tkinter import scrolledtext
import nltk
from nltk.stem import WordNetLemmatizer
import re
import datetime # For logging timestamps
import os # To manage the log file directory

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
"""
def get_response(user_input):
    
    Determines the chatbot's response based on predefined patterns and simulated search.
    
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
        if pattern in processed_input: # Direct keyword match
            return response
        
        pattern_words = preprocess_input(pattern) # For multi-word patterns
        # Checks if all words in a multi-word pattern are present in the user's input
        if all(word in processed_input for word in pattern_words) and len(pattern_words) > 1:
            return response

    return patterns_responses["default"] # Default response if no match is found
"""


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

# --- GUI Logic (Tkinter) ---




def send_message():
    user_message = entry_field.get()
    print("User input:", user_message)  # Debug print
    if user_message.strip() == "":
        return

    chat_history.config(state=tk.NORMAL)
    chat_history.insert(tk.END, f"You: {user_message}\n")

    if user_message.lower() == 'bye':
        bot_response = "Goodbye! Have a great day!"
        chat_history.insert(tk.END, f"Chatbot: {bot_response}\n")
        log_interaction(user_message, bot_response)
        root.after(750, root.destroy)
        return
    else:
        bot_response = get_response(user_message)
        print("Bot response:", bot_response)  # Debug print

    chat_history.insert(tk.END, f"Chatbot: {bot_response}\n")
    chat_history.config(state=tk.DISABLED)
    entry_field.delete(0, tk.END)
    chat_history.see(tk.END)
    log_interaction(user_message, bot_response)







def send_message():
    """
    This function is called when the user sends a message (Enter key or Send button).
    It processes the user's input, gets the bot's response, updates the GUI,
    and logs the interaction.
    """
    user_message = entry_field.get() # Get text from the input field
    if user_message.strip() == "": # Ignore empty messages
        return

    # 1. Display User Message in Chat History
    chat_history.config(state=tk.NORMAL) # Temporarily enable to insert text
    chat_history.insert(tk.END, f"You: {user_message}\n")
    
    # 2. Get Bot Response
    if user_message.lower() == 'bye':
        bot_response = "Goodbye! Have a great day!"
        chat_history.insert(tk.END, f"Chatbot: {bot_response}\n") # Display bye message immediately
        log_interaction(user_message, bot_response) # Log the exit interaction
        root.after(750, root.destroy) # Close window after a short delay (0.75 seconds)
        return # Exit the function
    else:
        bot_response = get_response(user_message)
    
    # 3. Display Bot Response in Chat History
    chat_history.insert(tk.END, f"Chatbot: {bot_response}\n")
    chat_history.config(state=tk.DISABLED) # Disable editing again
    
    # 4. Clear Input Field
    entry_field.delete(0, tk.END) # Clear the text in the entry field
    
    # 5. Scroll to the End of Chat History
    chat_history.see(tk.END) # Auto-scrolls to show the latest message

    # 6. Log the Interaction
    log_interaction(user_message, bot_response)

# --- Main Tkinter Window Setup ---
root = tk.Tk()
root.title("Simple Python Chatbot")
root.geometry("500x450") # Set initial window size (width x height)
root.resizable(False, False) # Prevents the window from being resized by the user

# Frame for the chat history display area
chat_frame = tk.Frame(root, bd=2, relief=tk.GROOVE) # Adds a border and groove effect
chat_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# ScrolledText widget for displaying chat history
chat_history = scrolledtext.ScrolledText(
    chat_frame, 
    wrap=tk.WORD, # Wrap lines at word boundaries
    state=tk.DISABLED, # Initially disabled so users can't type here
    font=("Arial", 10), 
    bg="#f0f0f0", # Light grey background
    fg="#333" # Dark grey text
)
chat_history.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

# Frame for the user input field and send button
input_frame = tk.Frame(root)
input_frame.pack(padx=10, pady=(0, 10), fill=tk.X) # Puts it at the bottom, some padding

# Entry widget for user input
entry_field = tk.Entry(
    input_frame, 
    font=("Arial", 11), 
    bd=2, 
    relief=tk.RIDGE # Adds a ridged border effect
)
entry_field.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=5) # Left aligned, expands horizontally
entry_field.bind("<Return>", lambda event=None: send_message()) # Binds the Enter key to the send_message function

# Send button
send_button = tk.Button(
    input_frame, 
    text="Send", 
    command=send_message, # Calls send_message when clicked
    font=("Arial", 12, "bold"), 
    bg="#4CAF50", # Green background
    fg="white", # White text
    activebackground="#45a049", # Darker green when pressed
    activeforeground="white",
    relief=tk.RAISED, # Raised button effect
    bd=2
)
send_button.pack(side=tk.RIGHT, padx=(5, 0), ipadx=10, ipady=5) # Right aligned, some padding

# Initial welcome message in the chat history
chat_history.config(state=tk.NORMAL)
chat_history.insert(tk.END, "Chatbot: Hi! How can I help you today?\n")
chat_history.config(state=tk.DISABLED)

# --- Start the Tkinter Event Loop ---
# This line must be at the very end. It keeps the GUI window open and responsive.
root.mainloop()