from flask import Flask,render_template, request
app = Flask(__name__)

@app.route('/a')
def hello_world():
    return 'Hello World'

from app1 import GetResponse
@app.route('/',methods=['GET','POST']) 
def index():
    if request.method == 'POST':
        query = request.form['userInput2']
        result = GetResponse(query)
        print("🤖 AI Response from main :\n", result)
        # GetResponse(query)
        print(result)
        result = "🤖 AI Response :\n" + result
        return (render_template('index.html', result=result))
    return (render_template('index.html'))

if __name__ == '__main__':
    app.debug = True
    app.run()
