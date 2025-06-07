import nltk
import tkinter as tk
from tkinter import scrolledtext
from nltk.stem import WordNetLemmatizer
import datetime

# --- Ensure Required NLTK Data is Available ---
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

try:
    nltk.data.find('corpora/omw-1.4')
except LookupError:
    nltk.download('omw-1.4')

# --- Chatbot Core Setup ---
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
    "colending": "It’s a joint lending arrangement among REs typically in the ratio of 80:20",
    "co lending": "It’s a joint lending arrangement among REs typically in the ratio of 80:20",
    "naam": "Naam me kya rakha hai"
}

def preprocess_input(text):
    text = text.lower()
    tokens = nltk.word_tokenize(text)
    return [lemmatizer.lemmatize(word) for word in tokens]

def get_response(user_input):
    processed_input_str = user_input.lower()

    # Handle "search for ..." queries
    if "search for" in processed_input_str:
        try:
            query = processed_input_str.split("search for", 1)[1].strip()
            if query:
                return f"Searching for '{query}'... (Simulated result: Found some interesting facts about '{query}'.)"
            else:
                return "What specifically would you like me to search for?"
        except Exception:
            return "What specifically would you like me to search for?"

    # Handle "what is ..." queries
    if "what is" in processed_input_str:
        try:
            query = processed_input_str.split("what is", 1)[1].strip()
            if query:
                return f"Searching for '{query}'... (Simulated result: The definition of '{query}' is [insert definition].)"
        except Exception:
            pass

    # Match predefined patterns
    for pattern, response in patterns_responses.items():
        if pattern in processed_input_str:
            return response

    # Default fallback response
    return patterns_responses["default"]

LOG_FILE = "chatbot_interactions.log"

def log_interaction(user_question, bot_response):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] User: {user_question}\n")
            f.write(f"[{timestamp}] Bot: {bot_response}\n")
            f.write("-" * 50 + "\n")
    except IOError as e:
        print(f"Error writing to log file: {e}")

def send_message():
    user_message = entry_field.get()
    print(f"User message received: '{user_message}'")  # Debug print

    if user_message.strip() == "":
        print("Empty input. No response generated.")  # Debug print
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
        print(f"Bot response: '{bot_response}'")  # Debug print

    chat_history.insert(tk.END, f"Chatbot: {bot_response}\n")
    chat_history.config(state=tk.DISABLED)
    entry_field.delete(0, tk.END)
    chat_history.see(tk.END)
    log_interaction(user_message, bot_response)

# --- GUI Setup ---
root = tk.Tk()
root.title("Simple Python Chatbot")
root.geometry("500x450")
root.resizable(False, False)

chat_frame = tk.Frame(root, bd=2, relief=tk.GROOVE)
chat_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

chat_history = scrolledtext.ScrolledText(
    chat_frame,
    wrap=tk.WORD,
    state=tk.DISABLED,
    font=("Arial", 10),
    bg="#f0f0f0",
    fg="#333"
)
chat_history.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

input_frame = tk.Frame(root)
input_frame.pack(padx=10, pady=(0, 10), fill=tk.X)

entry_field = tk.Entry(input_frame, font=("Arial", 11), bd=2, relief=tk.RIDGE)
entry_field.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=5)
entry_field.bind("<Return>", lambda event=None: send_message())

send_button = tk.Button(
    input_frame,
    text="Send",
    command=send_message,
    font=("Arial", 12, "bold"),
    bg="#4CAF50",
    fg="white",
    activebackground="#45a049",
    activeforeground="white",
    relief=tk.RAISED,
    bd=2
)
send_button.pack(side=tk.RIGHT, padx=(5, 0), ipadx=10, ipady=5)

chat_history.config(state=tk.NORMAL)
chat_history.insert(tk.END, "Chatbot: Hi! How can I help you today?\n")
chat_history.config(state=tk.DISABLED)

root.mainloop()
