import os
import google.generativeai as genai


genai.configure(api_key=os.environ['API_KEY'])

model = genai.GenerativeModel('gemini-1.5-flash')
chat = model.start_chat(history=[])

response = chat.send_message(
    input("Ask something to Gemini AI: "))

print(response.text)
