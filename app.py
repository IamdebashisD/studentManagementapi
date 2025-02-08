from flask import Flask, request, jsonify, Response
import requests
import datetime as dt
from typing import Any, Optional, NoReturn, Tuple


app = Flask(__name__)

@app.route('/current_weather', methods = ['POST'])
def get_weather():
    API_KEY:str = '91f939e70741477979cbd4df2994e7e9'
    data:dict[str, str] = request.get_json()
    
    if not data or not data.keys():
        return jsonify({'error': 'Please provide a city Name IN JSON format!'}), 400
    
    CITY_NAME = data['city']
    if not CITY_NAME or 'city' not in data:
        return jsonify({'error': 'City name is required and cannot be empty.'}), 400

    try:
        BASE_URL:str = f'''https://api.openweathermap.org/data/2.5/weather?q={CITY_NAME},In&appid={API_KEY}&units=metric'''
        response = requests.get(BASE_URL)
        data: dict[str,int,float, Any] = response.json()
        
        if data and data.get('coord') and data.get('weather') and data.get('main') and data.get('cod') == 200:
            longitude = data['coord']['lon']
            latitude = data['coord']['lat']
            main = data['weather'][0].get('main', 'No haze availbale')
            description = data['weather'][0].get('description', 'No description available')
            if data['base'] and len(data['base']) > 0:
                base = data.get('base', 'No base available')

            if len(data['main']) > 0:
                temperature = data['main']['temp']   
                feels_like = data['main']['feels_like']   
                temp_min = data['main']['temp_min']   
                temp_max = data['main']['temp_max']   
                pressure = data['main']['pressure']   
                humidity = data['main']['humidity']   
                sea_level = data['main']['sea_level']   
                ground_level = data['main']['grnd_level']
            if data.get('visibility'):
                visibility = data['visibility']

            if data.get('wind') and len(data['wind']) > 0:
                wind_speed = data['wind']['speed']
                wind_direction = data['wind']['deg']

            if data.get('clouds'):
                cloudiness = data['clouds']['all']

            if data.get('sys', {}) and data.get('timezone') is not None:
                type_info = data['sys']['type']
                location_id = data['sys']['id']
                country_code = data['sys']['country']
                sunrise_time = dt.datetime.fromtimestamp(data['sys']['sunrise'] + data['timezone'])
                sunset_time = dt.datetime.fromtimestamp(data['sys']['sunset'] + data['timezone'])

            if data.get('name') and data.get('timezone'):
                timezone = data['timezone']
                city_name = data.get('name')
                location_id = data['id']

            response = {
                "City name": city_name, "Country code": country_code, "Longitude": longitude, "Latitude": latitude, 
                "main": main, "description": description, "Base": base, "temperature": f'{temperature}\u00B0C', 
                "feels_like": feels_like, "Maximun temperature": temp_max, "Minimun temperature": temp_min, 
                "type_info": type_info, "pressure": pressure, "humidity": humidity, "sunrise time": sunrise_time, 
                "sunset time": sunset_time, "timezone": timezone, "wind speed": wind_speed, "wind direction": wind_direction,
                "country code": country_code, "cloudiness": cloudiness, "location id": location_id, 
                "ground level": ground_level,"see level": sea_level, "visibility": visibility
            }
            return jsonify({'result': response}), 200
        else:
            return jsonify({'message': 'Failed to fetch'}), 404

    except requests.exceptions.HTTPError as http_err:
        if http_err.response is not None:
            if http_err.response.status_code == 404:
                return jsonify({'error': 'City not found'}), 404
            else:
                return jsonify({'error': f'HTTP error occured {http_err}'}), http_err.response.status_code    
        else:
            return jsonify({'error': f'An HTTP error occured {http_err}'}), 500                    

    except Exception as err:
        return jsonify({'error': f'An error occured {str(err)}'}) # Default to 500 if no response

if __name__  == "__main__":
    app.run(debug = True)




