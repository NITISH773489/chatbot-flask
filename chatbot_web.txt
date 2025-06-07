from flask import Flask, request, jsonify
import nltk
from nltk.stem import WordNetLemmatizer
import datetime
import os

# Initialize Flask app
app = Flask(__name__)

# --- NLTK Setup ---
lemmatizer = WordNetLemmatizer()

# Download required NLTK data if not already present
try: nltk.data.find('tokenizers/punkt')
except: nltk.download('punkt')
try: nltk.data.find('corpora/wordnet')
except: nltk.download('wordnet')
try: nltk.data.find('corpora/omw-1.4')
except: nltk.download('omw-1.4')

# --- Bot Logic ---
patterns_responses = {
    "hello": "Hi there! How can I help you today?",
    "hi": "Hello! Nice to chat with you.",
    "how are you": "I'm a bot, so I don't have feelings, but I'm functioning well!",
    "what is your name": "I am a simple chatbot created to assist you.",
    "age": "I don't have an age. I was just programmed.",
    "bye": "Goodbye! Have a great day!",
    "thank you": "You're welcome!",
    "help": "You can ask me basic questions or say 'search for' something.",
    "python": "Python is a powerful programming language. Want to learn it?",
    "learn": "Learning is fun! What do you want to learn?",
    "colending": "It’s a joint lending arrangement among REs typically in the ratio of 80:20.",
    "co lending": "It’s a joint lending arrangement among REs typically in the ratio of 80:20.",
    "naam": "Naam me kya rakha hai",
    "default": "I'm sorry, I don't understand. Can you please rephrase that?"
}

def preprocess_input(text):
    tokens = nltk.word_tokenize(text.lower())
    return [lemmatizer.lemmatize(word) for word in tokens]

def get_response(user_input):
    processed_input = preprocess_input(user_input)

    # Simulated search-like behavior
    if "search" in processed_input and "for" in processed_input:
        try:
            query = " ".join(processed_input[processed_input.index("for") + 1:])
            return f"Searching for '{query}'... (Simulated result: found info on '{query}')"
        except:
            return "What exactly should I search for?"

    # Rule-based matching
    for pattern, response in patterns_responses.items():
        pattern_words = preprocess_input(pattern)
        if all(word in processed_input for word in pattern_words):
            return response

    return patterns_responses["default"]

def log_interaction(user_input, bot_response):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("chat_log.txt", "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] User: {user_input}\n")
        f.write(f"[{timestamp}] Bot: {bot_response}\n")
        f.write("-" * 50 + "\n")

# --- API Endpoint ---
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_msg = data.get('message', '')
    if not user_msg:
        return jsonify({"response": "Please send a valid message."}), 400

    bot_reply = get_response(user_msg)
    log_interaction(user_msg, bot_reply)
    return jsonify({"response": bot_reply})

if __name__ == '__main__':
    app.run(debug=True)
