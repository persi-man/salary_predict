import os
import openai
import replicate
import anthropic
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()

# Dictionnaire pour stocker les clés API
api_keys = {
    'ChatGPT': os.getenv('CHATGPT_API_KEY'),
    'LLaMA': os.getenv('LLAMA_API_KEY'),
    'Claude': os.getenv('ANTHROPIC_API_KEY'),
    'Replicate': os.getenv('REPLICATE_API_KEY')
}

def get_response(model_selection, user_input):
    if model_selection == 'ChatGPT':
        openai.api_key = api_keys['ChatGPT']
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": user_input}]
        )
        return response.choices[0].message.content

    elif model_selection == 'LLaMA':
        # Utilisation de l'API Replicate pour LLaMA
        replicate_client = replicate.Client(api_token=api_keys['Replicate'])
        response = replicate_client.run(
            "meta/meta-llama-3.1-405b-instruct",
            input={"prompt": user_input, "max_length": 100}
        )
        return response

    elif model_selection == 'Claude':
        ant_client = anthropic.Anthropic()
        anthropic.api_key = api_keys['Claude']
        response = ant_client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=150,
            temperature=0.5,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text",
                         "text": user_input
                         }
                    ]
                }
            ]
        )
        return response.completion

    return "Modèle non reconnu."
