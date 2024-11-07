from flask import Flask, request, jsonify
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

nltk.download('stopwords')

# Initialize global variables and configurations for chatbot context
menu_context = None
stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

@app.route("/")
def home():
    return render_template("./index.html")

# Define the chatbot functions and logic provided
def preprocess_input(text):
    words = nltk.word_tokenize(text.lower())
    filtered_words = [lemmatizer.lemmatize(w) for w in words if w.isalnum() and w not in stop_words]
    return " ".join(filtered_words)

def handle_main_menu(user_input):
    global menu_context
    user_input = preprocess_input(user_input)

    if "1" in user_input or "products" in user_input:
        menu_context = "products"
        return "You are now in the products section. Here are some options: \n1. View all products\n2. Search for a product\n3. Go back to the main menu."
    elif "2" in user_input or "order" in user_input:
        menu_context = "orders"
        return "You are now in the orders section. What would you like to do?\n1. Track an order\n2. Cancel an order\n3. Go back to the main menu."
    elif "3" in user_input or "customer service" in user_input:
        menu_context = "customer_service"
        return "Welcome to customer service! How can we help you today?\n1. Speak to a representative\n2. Return to the main menu."
    elif "4" in user_input or "contact us" in user_input:
        return "You can contact us at contact@yourshop.com or call us at +1234567890."
    elif "5" in user_input or "time" in user_input:
        current_time = datetime.datetime.now().strftime("%H:%M")
        return f"The current time is {current_time}."
    elif "6" in user_input or "date" in user_input:
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        return f"Today's date is {current_date}."
    else:
        return "Invalid choice. Please select a valid option:\n1. Products\n2. Orders\n3. Customer Service\n4. Contact Us\n5. Current Time\n6. Current Date"

def handle_sub_menu(user_input):
    global menu_context
    user_input = preprocess_input(user_input)

    if menu_context == "products":
        if "1" in user_input or "view" in user_input:
            return "Here are all available products."
        elif "2" in user_input or "search" in user_input:
            return "Please enter the product name to search for."
        elif "3" in user_input or "back" in user_input:
            menu_context = None
            return "Returning to the main menu."
        else:
            return "Invalid choice in products section. Please select a valid option."
    
    elif menu_context == "orders":
        if "1" in user_input or "track" in user_input:
            return "Please provide your order number to track."
        elif "2" in user_input or "cancel" in user_input:
            return "Please provide your order number to cancel."
        elif "3" in user_input or "back" in user_input:
            menu_context = None
            return "Returning to the main menu."
        else:
            return "Invalid choice in orders section. Please select a valid option."

    elif menu_context == "customer_service":
        if "1" in user_input or "speak" in user_input:
            return "Connecting you to a customer service representative."
        elif "2" in user_input or "back" in user_input:
            menu_context = None
            return "Returning to the main menu."
        else:
            return "Invalid choice in customer service. Please select a valid option."
    
    else:
        menu_context = None
        return "Returning to the main menu."

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    print("User Input:", user_input)  # Check if this prints the user's input
    global menu_context

    if menu_context is None:
        response = handle_main_menu(user_input)
    else:
        response = handle_sub_menu(user_input)
    
    return jsonify({"response": response})


if __name__ == "__main__":
    app.run(debug=True)
