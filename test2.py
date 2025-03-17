import requests
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk

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
        
        weather_info.set(
            f"Погода в {city}, {country}:\n"
            f"Температура: {temp}°C\n"
            f"Влажность: {humidity}%\n"
            f"Атмосферное давление: {pressure} hPa\n"
            f"Описание: {weather_desc.capitalize()}"
        )
        
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка при получении данных: {e}")
    except KeyError as e:
        messagebox.showerror("Ошибка", f"Ошибка в данных: {e}")

def on_city_select():
    selected_city = city_var.get()
    if selected_city:
        get_weather(selected_city, api_key)

root = Tk()
root.title("Погодное приложение")
root.geometry("400x600")

try:
    bg_image = Image.open("background.jpg")
    bg_image = bg_image.resize((400, 600), Image.ANTIALIAS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = Label(root, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)
except FileNotFoundError:
    print("Файл изображения не найден. Продолжение без фонового изображения.")

api_key = "b67c58f69b9b4084d425b4935230a194"

cities = ["Moscow", "Saint Petersburg", "Novosibirsk", "Yekaterinburg", "Kazan"]

city_var = StringVar(root)
city_var.set(cities[0])

weather_info = StringVar()
weather_info.set("Выберите город, чтобы узнать погоду.")

try:
    logo_image = Image.open("logo.png")
    logo_image = logo_image.resize((100, 100), Image.ANTIALIAS)
    logo_photo = ImageTk.PhotoImage(logo_image)
    logo_label = Label(root, image=logo_photo, bg="white")
    logo_label.pack(pady=10)
except FileNotFoundError:
    print("Файл логотипа не найден. Продолжение без логотипа.")

city_label = Label(root, text="Выберите город:", bg="white", font=("Arial", 12))
city_label.pack(pady=10)

city_dropdown = OptionMenu(root, city_var, *cities)
city_dropdown.config(font=("Arial", 12))
city_dropdown.pack(pady=10)

get_weather_button = Button(root, text="Получить погоду", command=on_city_select, font=("Arial", 12))
get_weather_button.pack(pady=20)

weather_label = Label(root, textvariable=weather_info, bg="white", font=("Arial", 12), justify=LEFT)
weather_label.pack(pady=20)

root.mainloop()