from flask import Flask, request, jsonify, render_template
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# Download required NLTK resources only if they're not already downloaded
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('wordnet', quiet=True)

# Initialize global variables and configurations for chatbot context
menu_context = None
stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()
greetings = [
    "hi",
    "hello",
    "hey",
    "good morning",
    "good afternoon",
    "good evening",
    "what's up?",
    "howdy",
    "greetings",
    "hi there",
    "hey there",
    "hi and hello",
    "how’s it going?",
    "what’s new?",
    "nice to meet you",
    "long time no see",
    "sup?",
    "yo",
    "how are you?",
    "how are things?"
]

product_list = [
    "Smartphone - Model X", "Laptop - PowerPro 15", "Headphones - SoundMax Pro",
    "Camera - SnapIt 12MP", "Smartwatch - TimeTrack Ultra", "Tablet - TabPlus 10.1",
    "Gaming Console - GameBox 360", "Wireless Earbuds - EarSync Duo", "Monitor - ViewMaster 27",
    "External Hard Drive - StoragePro 1TB"
]



@app.route("/")
def home():
    return render_template("index.html")

# Define the chatbot functions and logic
def preprocess_input(text):
    words = nltk.word_tokenize(text.lower())
    filtered_words = [lemmatizer.lemmatize(w) for w in words if w.isalnum() and w not in stop_words]
    return " ".join(filtered_words)

def greet_user():
    current_hour = datetime.datetime.now().hour
    options = "Please choose a valid option:\n1. Products\n2. Orders\n3. Customer Service\n4. Contact Us\n5. Current Time\n6. Current Date"
    if current_hour > 4 and current_hour < 12:
        return f"Good morning! Welcome to Customer Service Chatbot. How can I assist you today? {options}"
    elif 12 <= current_hour < 16:
        return f"Good afternoon! Welcome to Customer Service Chatbot. How can I assist you today? {options}"
    else:
        return f"Good evening! Welcome to Customer Service Chatbot. How can I assist you today? {options}"

def handle_main_menu(user_input):
    global menu_context
    user_input = preprocess_input(user_input)

    if "1" in user_input or "products" in user_input:
        menu_context = "products"
        return "You're now in the products section. Here are some options:\n1. View all products\n2. Search for a product\n3. Go back to the main menu."
    elif "2" in user_input or "order" in user_input:
        menu_context = "orders"
        return "You're now in the orders section. What would you like to do?\n1. Track an order\n2. Cancel an order\n3. Go back to the main menu."
    elif "3" in user_input or "customer service" in user_input:
        menu_context = "customer_service"
        return "Welcome to customer service! How can we help you today?\n1. Speak to a representative\n2. Return to the main menu."
    elif "4" in user_input or "contact us" in user_input:
        return "You can contact us at contact@yourshop.com or call us at +1234567890. We're happy to help!"
    elif "5" in user_input or "time" in user_input:
        current_time = datetime.datetime.now().strftime("%H:%M")
        return f"The current time is {current_time}. Anything else I can assist you with?"
    elif "6" in user_input or "date" in user_input:
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        return f"Today's date is {current_date}. Is there anything else I can help you with?"
    else:
        return "I'm sorry, I didn't quite catch that. Please choose a valid option:\n1. Products\n2. Orders\n3. Customer Service\n4. Contact Us\n5. Current Time\n6. Current Date"

def handle_sub_menu(user_input):
    global menu_context
    user_input = preprocess_input(user_input)

    if menu_context == "products":
        if "1" in user_input or "view" in user_input:
            return f"Here are all available products. Let me know if you'd like details on any specific product :{product_list}" 
        elif "2" in user_input or "search" in user_input:
            return "Please enter the product name you'd like to search for."
        elif "3" in user_input or "back" in user_input:
            menu_context = None
            return "Returning to the main menu. How else may I assist you?"
        else:
            return "Sorry, I didn't understand that. Please select a valid option in the products section."

    elif menu_context == "orders":
        if "1" in user_input or "track" in user_input:
            return "Please provide your order number to track it."
        elif "2" in user_input or "cancel" in user_input:
            return "Please provide your order number to cancel."
        elif "3" in user_input or "back" in user_input:
            menu_context = None
            return "Returning to the main menu. How else may I assist you?"
        else:
            return "Sorry, I didn't understand that. Please select a valid option in the orders section."

    elif menu_context == "customer_service":
        if "1" in user_input or "speak" in user_input:
            return "Connecting you to a customer service representative. Please hold on a moment."
        elif "2" in user_input or "back" in user_input:
            menu_context = None
            return "Returning to the main menu. How else may I assist you?"
        else:
            return "Sorry, I didn't understand that. Please select a valid option in customer service."

    else:
        menu_context = None
        return "Returning to the main menu."

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_input = request.json.get("message")
        global menu_context
        # Initial greeting when no menu context is set and no input is provided
        if user_input.lower() in greetings:
            response = greet_user()
        elif menu_context is None:
            response = handle_main_menu(user_input.lower())
        else:
            response = handle_sub_menu(user_input.lower())
        return jsonify({"response": response})
    except Exception as e:
        print("Error in /chat route:", e)
        return jsonify({"response": "Oops! Something went wrong on our end. Please try again."}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)
