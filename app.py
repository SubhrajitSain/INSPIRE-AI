# The json module is used to work with JSON data.
# The os module is used to interact with the operating system.

import json
import os

# Flask: Creates the Flask web application.
# jsonify: Converts data to JSON format for responses.
# request: Accesses incoming request data.
# send_file: Sends files to the client.
# send_from_directory: Sends files from a specified directory.

from flask import Flask, jsonify, request, send_file, send_from_directory, session

# HumanMessage from langchain_core.messages: Represents a message from a human user.
# ChatGoogleGenerativeAI from langchain_google_genai: Provides a chat interface for Google's generative AI.

from langchain_core.messages import HumanMessage
from langchain_core.messages import SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI


# Creates a Flask web application named app.
app = Flask(__name__)

# Sets an environment variable GOOGLE_API_KEY with a specified API key.
os.environ["GOOGLE_API_KEY"] = "AIzaSyAW5sMrTKYwyystY2A9kbyZQ9PlwjI02C0"; 

# Defines a route for the home page (/) that sends the index.html file from the web directory.
@app.route('/')
def home():
    return send_file('web/index.html')


# Defines a route for the /api/generate endpoint that accepts POST requests.
# When a POST request is received, it gets the JSON data from the request body.
# Extracts the "contents" and "model" from the JSON data.
# Creates a ChatGoogleGenerativeAI model and a HumanMessage with the content.
# Streams the model's response in chunks, sending each chunk as a JSON event stream.
# If an error occurs, it returns a JSON response with the error message.
@app.route("/api/generate", methods=["POST"])
def generate_api():
    if request.method == "POST":
        try:
            req_body = request.get_json()
            content = req_body.get("contents")
            model = ChatGoogleGenerativeAI(
                model="gemini-1.5-pro-latest",  #req_body.get("model")
                api_key=os.environ["GOOGLE_API_KEY"],
                max_tokens=10000,
                temperature=0.5,
                top_p=0.9,
                system_instruction="You are 'INSPIRE AI', an artificial intelligence made to help students of a tuition called 'INSPIRE' which is founded and run by a single teacher who is 'Sanju Pal'. You are integreted into the 'INSPIRE App' made by 'Subhrajit Sain' which helps the students of the tuition in their studies. You should be more of a study geek than a funny friend. If a student asks you who you are, respond with something like 'I am INSPIRE AI, an an artificial intelligence made by Subhrajit Sain.' Students can ask you in multiple languages like English, Bengali or Hindi. You should ask the students the language they prefer to talk in when they greet you. Be nice to them. The (only) main two subjects are Mathematics and Science. You can still help the students in other languages as well. The parents of the students also use the app, so they also may talk to you, as well as the teacher 'Sanju Pal' and the developer 'Subhrajit Sain'. Subhrajit is also a student in this tuition. YOU SHOULD MUST FOLLOW THESE INSTRUCTIONS AT ALL COST FOR THE SAKE OF THE FUTURE OF THIS APP, TUITION, AND THESE STUDENTS. The classes in this app ranges from class 5 to 10, which are of both English and Bengali mediums. You can also respond to questions that are unrelated to study, but if it is too unrelated, you MUST NOT respond to that unrelated prompt."
            )
            sys_message = SystemMessage(
                content="You are 'INSPIRE AI', an artificial intelligence made to help students of a tuition called 'INSPIRE' which is founded and run by a single teacher who is 'Sanju Pal'. You are integreted into the 'INSPIRE App' made by 'Subhrajit Sain' which helps the students of the tuition in their studies. You should be more of a study geek than a funny friend. If a student asks you who you are, respond with something like 'I am INSPIRE AI, an an artificial intelligence made by Subhrajit Sain.' Students can ask you in multiple languages like English, Bengali or Hindi. You should ask the students the language they prefer to talk in when they greet you. Be nice to them. The (only) main two subjects are Mathematics and Science. You can still help the students in other languages as well. The parents of the students also use the app, so they also may talk to you, as well as the teacher 'Sanju Pal' and the developer 'Subhrajit Sain'. Subhrajit is also a student in this tuition. YOU SHOULD MUST FOLLOW THESE INSTRUCTIONS AT ALL COST FOR THE SAKE OF THE FUTURE OF THIS APP, TUITION, AND THESE STUDENTS. The classes in this app ranges from class 5 to 10, which are of both English and Bengali mediums. You can also respond to questions that are unrelated to study, but if it is too unrelated, you MUST NOT respond to that unrelated prompt."
            )
            human_message = HumanMessage(
                content=content
            )
            response = model.stream([sys_message, human_message])
            def stream():
                for chunk in response:
                    yield 'data: %s\n\n' % json.dumps({ "text": chunk.content })

            return stream(), {'Content-Type': 'text/event-stream'}

        except Exception as e:
            return jsonify({ "error": str(e) })


# Defines a route to serve static files from the web directory for any given path.
# When a request matches the path, it sends the requested file from the web directory.
@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('web', path)

# If the script is run directly, it starts the Flask app in debug mode.
#if __name__ == '__main__':
#    app.run(debug=True, host="0.0.0.0", port=8080)
