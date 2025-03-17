import requests

def get_weather(city_name, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    
    params = {
        "q": city_name,
        "appid": api_key,
        "units": "metric",
        "lang": "ru"
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        city = data.get("name", "Неизвестно")
        country = data.get("sys", {}).get("country", "Неизвестно")
        temp = data.get("main", {}).get("temp", "Недоступно")
        humidity = data.get("main", {}).get("humidity", "Недоступно")
        pressure = data.get("main", {}).get("pressure", "Недоступно")
        weather_desc = data.get("weather", [{}])[0].get("description", "Недоступно")
        
        print(f"Погода в {city}, {country}:")
        print(f"Температура: {temp}°C")
        print(f"Влажность: {humidity}%")
        print(f"Атмосферное давление: {pressure} hPa")
        print(f"Описание: {weather_desc.capitalize()}")
        print("-" * 30)
        
    except requests.exceptions.RequestException as e:
        print(f"Произошла ошибка при получении данных для города {city_name}: {e}")
    except KeyError as e:
        print(f"Ошибка в данных для города {city_name}: {e}")

def choose_city():
    cities = {
        1: "Moscow",
        2: "Saint Petersburg",
        3: "Novosibirsk",
        4: "Yekaterinburg",
        5: "Kazan"
    }
    
    while True:
        print("Выберите город:")
        for key, city in cities.items():
            print(f"{key}. {city}")
        
        try:
            choice = int(input("Введите номер города: "))
            if choice in cities:
                selected_city = cities[choice]
                get_weather(selected_city, api_key)
            else:
                print("Неверный выбор. Пожалуйста, выберите номер из списка.")
        except ValueError:
            print("Неверный ввод. Пожалуйста, введите число.")

if __name__ == "__main__":
    api_key = "b67c58f69b9b4084d425b4935230a194"
    
    choose_city()