from pyrogram import Client, filters
import openai

# OpenAI API Key
openai.api_key = "YOUR_OPENAI_API_KEY"

# Function to get AI response from OpenAI
def get_ai_response(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",  # Use the appropriate model
        prompt=prompt,
        max_tokens=150,
    )
    return response.choices[0].text.strip()

# Pyrogram message handler for the AI chatbot
@Client.on_message(filters.text & filters.group)
def ai_chatbot(client, message):
    user_input = message.text
    ai_reply = get_ai_response(user_input)
    message.reply(ai_reply)