from flask import Flask, render_template, request, jsonify
from modules.city import CityHelper
from modules.weather import WeatherHelper
from modules.database import WeatherRequestsManager
import datetime
import logging
app = Flask(__name__)

# Список возможных подсказок


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/suggestions')
def get_suggestions():
    query = request.args.get('query')
    if query:
        suggestions = CityHelper.get_list_of_cities(query.lower())
        return jsonify(suggestions)
    return ''


# @app.route('/weather')
# def get_city():
#     city_name = request.args.get('city')
#     coords = CityHelper.get_city_coords(city_name)
#     forecast = WeatherHelper.get_weather_week(coords)
#     return render_template('weather.html', city={'name': city_name}, forecast=forecast)

@app.route('/request_count')
def request_count():
    city_name = request.args.get('city')
    count = WeatherRequestsManager.get_request_count(city_name)
    return jsonify({"city": city_name,
                    "count": count})


@app.route('/weather')
def test_page():
    city_name = request.args.get('city')
    WeatherRequestsManager.increase_request_counter(city_name)
    coords = CityHelper.get_city_coords(city_name)
    forecast = WeatherHelper.get_weather_week(coords)
    return render_template("test.html", forecast=forecast, city={"name": city_name}, date={"date": datetime.datetime.today().strftime("%d.%m.%Y")})


if __name__ == '__main__':
    WeatherRequestsManager.create_table()
    app.run(host='0.0.0.0', port=5000, debug=True)
