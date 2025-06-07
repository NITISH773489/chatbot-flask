from flask import Flask, request, jsonify
import nltk
from nltk.stem import WordNetLemmatizer

# Ensure required NLTK data
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
    "naam": "Naam me kya rakha hai",
    "default": "I'm sorry, I don't understand. Can you please rephrase that?"
}

def preprocess_input(text):
    text = text.lower()
    tokens = nltk.word_tokenize(text)
    return [lemmatizer.lemmatize(word) for word in tokens]

def get_response(user_input):
    processed_input = preprocess_input(user_input)
    for pattern, response in patterns_responses.items():
        pattern_words = preprocess_input(pattern)
        if all(word in processed_input for word in pattern_words):
            return response
    return patterns_responses["default"]

# Flask app
app = Flask(__name__)

@app.route("/")
def index():
    return "Chatbot is running!"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")
    response = get_response(user_message)
    return jsonify({"response": response})

if __name__ == "__main__":
    import os
port = int(os.environ.get("PORT", 5000))
app.run(debug=False, host="0.0.0.0", port=port)
