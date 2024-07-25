from flask import Flask, render_template, request, jsonify
import os
import google.generativeai as genai
from flask_cors import CORS
import sqlite3

genai.configure(api_key=os.environ['API_KEY'])

model = genai.GenerativeModel('gemini-1.5-flash')
app = Flask(__name__)
CORS(app)
chat = model.start_chat(history=[])

# Global variable for counter

def init_db():
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                name TEXT NOT NULL, 
                email TEXT UNIQUE NOT NULL
            )
            '''
        )
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS resources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                eligibility TEXT NOT NULL,
                application_deadline_process TEXT NOT NULL,
                contact TEXT NOT NULL,
                website TEXT NOT NULL
            )
            '''
        )
        conn.commit()
# Call init_db() once at the start of the application
init_db()

@app.route('/api/resources', methods=['GET'])
def get_resources():
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM resources')
        rows = cursor.fetchall()
        resources = [
            {
                "name": row[1],
                "desc": row[2],
                "elig": row[3],
                "app_deadline_process": row[4],
                "contact": row[5],
                "website": row[6]
            }
            for row in rows
        ]
    return jsonify(resources)


@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/api/resources_page')
def resources_page():
    return render_template('infodatabase.html')


@app.route('/involve')
def involve():
    return render_template('involve.html')

@app.route('/api/chat', methods=['POST'])
def chat_api():
    data = request.get_json()
    user_message = data["message"]
    response = chat.send_message(user_message)
    return jsonify({"reply": response.text})

if __name__ == '__main__':
    app.run(debug=True)
