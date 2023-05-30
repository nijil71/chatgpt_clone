from flask import Flask, render_template, request, redirect, url_for, session,jsonify
from flask_pymongo import PyMongo
import openai

openai.api_key = ""

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://nmnijilkhan:Khannijil%40123@cluster0.q4yvzzk.mongodb.net/chatgpt"
mongo = PyMongo(app)

@app.route('/')
def home():
    chats = mongo.db.chats.find({})
    mychats=[chat for chat in chats] 
    return render_template('index.html',mychats=mychats)

@app.route('/api', methods=['GET', 'POST'])
def qa():
    if request.method == 'POST':
        print(request.json)
        question = request.json.get('question')
        chat = mongo.db.chats.find_one({"question":question})
        print(chat)
        if chat:
            data = {"result": f"{chat['answer']}"}
            return jsonify(data)
        else:
            response = openai.Completion.create(
            model="text-davinci-003",
            prompt=question,
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
            )
            data = {"question":question,"answer":response.choices[0].text}
            mongo.db.chats.insert_one({"question":question,"answer":response.choices[0].text})
            return jsonify(data)
    data={"result": "This version includes custom styles for the form elements, such as colors, borders, and padding, to give it an insane look. Feel free to adjust the styles further to your liking!"}
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)