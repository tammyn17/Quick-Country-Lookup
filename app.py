from flask import Flask, render_template, request
import requests
import os 
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    country = request.form['country']
    print("Country entered:", country)
    
    country_url = (f"https://restcountries.com/v3.1/name/{country}?fields=name,capital,population,currencies,languages,flags")
    print("Fetching country data from:", country_url)
    try:
        country_res = requests.get(country_url)
        country_res.raise_for_status()
        country_data = country_res.json()[0]
        print("Country data returned:", country_data)

        name = country_data['name']['common']
        capital = country_data.get('capital', ['N/A'])[0]
        population = country_data.get('population', 'N/A')
        currencies = ', '.join(
            [currencies['name'] for currencies in country_data.get('currencies', {}).values()]
        )
        languages = ', '.join(
            [lang for lang in country_data.get('languages', {}).values()]
        )
        flag_url = country_data['flags']['png'] 

        print(f"Capital: {capital}")

        weather_url = (f"http://api.openweathermap.org/data/2.5/weather?q={capital}&appid={WEATHER_API_KEY}&units=metric")
        print("Fetching weather data from:", weather_url)

        weather_res = requests.get(weather_url)
        weather_res.raise_for_status()
        weather_data = weather_res.json()
        print("Weather data returned:", weather_data)

        temp = weather_data['main']['temp']
        condition = weather_data['weather'][0]['description']
        icon = weather_data['weather'][0]['icon']
       
        return render_template('results.html', name=name, capital=capital, population=population,
                               currencies=currencies, languages=languages, flag_url=flag_url, temp=temp, condition=condition, icon=icon)
    
    except Exception as e:
        print("Error:", e)
        return render_template('index.html', error="Please enter a valid country.")

if __name__ == '__main__':
    app.run(debug=True)