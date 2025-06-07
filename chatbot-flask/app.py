from flask import Flask, request, render_template
import nltk
from nltk.stem import WordNetLemmatizer

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
    "bye": "Goodbye! Have a great day!",
    "thank you": "You're welcome!",
    "help": "I can answer basic questions about myself.",
    "colending": "It’s a joint lending arrangement among REs typically in the ratio of 80:20",
    "default": "I'm sorry, I don't understand. Can you please rephrase that?"
}

def get_response(user_input):
    user_input = user_input.lower()
    for pattern, response in patterns_responses.items():
        if pattern in user_input and pattern != "default":
            return response
    return patterns_responses["default"]

@app.route("/", methods=["GET", "POST"])
def index():
    response = ""
    if request.method == "POST":
        message = request.form["message"]
        response = get_response(message)
    return render_template("chat.html", response=response)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
