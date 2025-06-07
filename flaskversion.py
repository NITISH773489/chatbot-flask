# app.py
from flask import Flask, request, render_template
import nltk
from nltk.stem import WordNetLemmatizer
import datetime

# Download required NLTK data
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')

app = Flask(__name__)
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

def get_response(user_input):
    user_input = user_input.lower()

    if "search for" in user_input:
        query = user_input.split("search for", 1)[1].strip()
        return f"Searching for '{query}'... (Simulated result: Found some interesting facts about '{query}')."

    if "what is" in user_input:
        query = user_input.split("what is", 1)[1].strip()
        return f"Searching for '{query}'... (Simulated result: The definition of '{query}' is [insert definition])."

    for pattern, response in patterns_responses.items():
        if pattern in user_input and pattern != "default":
            return response

    return patterns_responses["default"]

@app.route("/", methods=["GET", "POST"])
def index():
    response = ""
    if request.method == "POST":
        user_message = request.form["message"]
        response = get_response(user_message)
    return render_template("chat.html", response=response)

