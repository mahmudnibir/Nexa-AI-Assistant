import random
import json

def load_conversations():
    """Load conversation patterns from a JSON file."""
    try:
        with open('conversations.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_conversations(conversations):
    """Save conversation patterns to a JSON file."""
    with open('conversations.json', 'w') as file:
        json.dump(conversations, file, indent=4)

def get_response(intent, conversation_data, **kwargs):
    """Retrieve a response based on the intent."""
    responses = conversation_data.get(intent, [])
    if responses:
        response = random.choice(responses)
        # Replace placeholders in the response
        for key, value in kwargs.items():
            response = response.replace(f"{{{{{key}}}}}", str(value))
        return response
    else:
        return "Sorry, I don't have a response for that."

def add_conversation(intent, response):
    """Add a new conversation pattern."""
    conversations = load_conversations()
    if intent in conversations:
        conversations[intent].append(response)
    else:
        conversations[intent] = [response]
    save_conversations(conversations)
