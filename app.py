import os
from dotenv import load_dotenv
from flask import Flask, render_template, jsonify, request
from ecommbot.ingest import ingestdata
from ecommbot.retrieval_generation import generation

app= Flask(__name__)

load_dotenv()
vectorstore= ingestdata('done')
chain= generation(vectorstore)

@app.route('/')
def index():
    return render_template('chat.html')


@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    result= chain.invoke(input)
    print(f'Response: {result}')
    return str(result)
    
    
if __name__ == '__main__':
    app.run(debug= True)
    