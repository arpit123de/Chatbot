# from flask import Flask,render_template, request
# app = Flask(__name__)

# @app.route('/a')
# def hello_world():
#     return 'Hello World'

# from app1 import GetResponse
# @app.route('/',methods=['GET','POST']) 
# def index():
#     if request.method == 'POST':
#         query = request.form['userInput2']
#         result = GetResponse(query)
#         print("🤖 AI Response from main :\n", result)
#         # GetResponse(query)
#         # print(query)
#         result = "🤖 AI Response :\n" + result
#         return (render_template('index.html', result=result))
#     return (render_template('index.html'))

# if __name__ == '__main__':
#     app.debug = True
#     a

from flask import Flask, render_template, request
import requests
from waitress import serve

app = Flask(__name__)

# === AI RESPONSE HANDLER ===
API_TOKEN = "wAuzeTQbBowf6RJYgqMJ3RIS2sd2r8wL"
API_URL = "https://api.deepinfra.com/v1/inference/meta-llama/Meta-Llama-3-8B-Instruct"
headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

def GetResponse(qry):    
    data = {
        "input": "<|begin_of_text|><|start_header_id|>user<|end_header_id|>\n\n" + qry + "<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n",
        "stop": ["<|eot_id|>"],
        "stream": False
    }
    response = requests.post(API_URL, headers=headers, json=data)
    
    if response.status_code == 200:
        response_json = response.json()
        generated_text = response_json["results"][0]["generated_text"]
    else:
        generated_text = f"❌ Error: {response.status_code} - {response.text}"
    return generated_text

# === WEATHER + AQI ===
def GetPollution(lon, lat):
    API_Key = "65dab33592af356944a01e1f66db4a8f"
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_Key}"
    return requests.get(url)

def GetWeather(city_name):
    API_Key = "65dab33592af356944a01e1f66db4a8f"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_Key}"
    return requests.get(url)

# === ROUTES ===
@app.route('/a')
def hello_world():
    return 'Hello World'

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ''
    if request.method == 'POST':
        user_input = request.form['userInput2']
        weather_only = 'weatherOnly' in request.form  # True if checkbox is checked

        if weather_only:
            # Handle weather and AQI only
            weather_response = GetWeather(user_input)
            if weather_response.status_code == 200:
                api_data = weather_response.json()
                lon = api_data['coord']['lon']
                lat = api_data['coord']['lat']
                temp_city = api_data['main']['temp'] - 273.15
                weather_desc = api_data['weather'][0]['description']

                pollution_response = GetPollution(lon, lat)
                if pollution_response.status_code == 200:
                    pollution_data = pollution_response.json()
                    aqi = pollution_data['list'][0]['main']['aqi']
                    aqi_description = {
                        1: "Good",
                        2: "Fair",
                        3: "Moderate",
                        4: "Poor",
                        5: "Very Poor"
                    }.get(aqi, "Unknown")

                    result = f"""🌦️ Weather Report for {user_input}:
Temperature: {temp_city:.2f}°C
Description: {weather_desc}
AQI: {aqi} - {aqi_description}"""
                else:
                    result = "Weather found but AQI lookup failed."
            else:
                result = "❌ Could not fetch weather for the given city."
        else:
            # Handle AI Chat only
            ai_response = GetResponse(user_input)
            result = f"🤖 AI Response:\n{ai_response}"

    return render_template('index.html', result=result)
if __name__ == '__main__':
    # app.debug = True
    # app.run()
    serve(app, host="0.0.0.0", port=8000, threads=8)
