import requests
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk

def get_weather(city_name, api_key):
    # رابط OpenWeatherMap API
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    
    # المعاملات التي سيتم إرسالها مع الطلب
    params = {
        "q": city_name,        # اسم المدينة
        "appid": api_key,      # مفتاح API
        "units": "metric",     # الوحدة المستخدمة (درجة الحرارة بـ مئوي)
        "lang": "ru"           # اللغة الروسية
    }
    
    try:
        # إرسال الطلب إلى API
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # التحقق من الأخطاء في الاستجابة
        
        # تحويل الاستجابة إلى JSON
        data = response.json()
        
        # استخراج البيانات
        city = data.get("name", "Неизвестно")  # اسم المدينة
        country = data.get("sys", {}).get("country", "Неизвестно")  # الدولة
        temp = data.get("main", {}).get("temp", "Недоступно")  # درجة الحرارة
        humidity = data.get("main", {}).get("humidity", "Недоступно")  # الرطوبة
        pressure = data.get("main", {}).get("pressure", "Недоступно")  # الضغط الجوي
        weather_desc = data.get("weather", [{}])[0].get("description", "Недоступно")  # وصف الطقس
        
        # عرض البيانات في الواجهة
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
    # الحصول على المدينة المختارة
    selected_city = city_var.get()
    if selected_city:
        get_weather(selected_city, api_key)

# إنشاء النافذة الرئيسية
root = Tk()
root.title("Погодное приложение")
root.geometry("400x600")  # حجم النافذة

# تحميل صورة الخلفية
try:
    bg_image = Image.open("background.jpg")  # استبدل بمسار الصورة الخاصة بك
    bg_image = bg_image.resize((400, 600), Image.ANTIALIAS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = Label(root, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)
except FileNotFoundError:
    print("Файл изображения не найден. Продолжение без фонового изображения.")

# مفتاح API
api_key = "b67c58f69b9b4084d425b4935230a194"  # استبدل بمفتاح API الخاص بك إذا لزم الأمر

# قائمة المدن
cities = ["Moscow", "Saint Petersburg", "Novosibirsk", "Yekaterinburg", "Kazan"]

# متغير لتخزين المدينة المختارة
city_var = StringVar(root)
city_var.set(cities[0])  # القيمة الافتراضية

# متغير لعرض معلومات الطقس
weather_info = StringVar()
weather_info.set("Выберите город, чтобы узнать погоду.")

# إضافة صورة إلى الواجهة
try:
    logo_image = Image.open("logo.png")  # استبدل بمسار الصورة الخاصة بك
    logo_image = logo_image.resize((100, 100), Image.ANTIALIAS)
    logo_photo = ImageTk.PhotoImage(logo_image)
    logo_label = Label(root, image=logo_photo, bg="white")
    logo_label.pack(pady=10)
except FileNotFoundError:
    print("Файл логотипа не найден. Продолжение без логотипа.")

# إنشاء القائمة المنسدلة (Dropdown)
city_label = Label(root, text="Выберите город:", bg="white", font=("Arial", 12))
city_label.pack(pady=10)

city_dropdown = OptionMenu(root, city_var, *cities)
city_dropdown.config(font=("Arial", 12))
city_dropdown.pack(pady=10)

# زر للحصول على الطقس
get_weather_button = Button(root, text="Получить погоду", command=on_city_select, font=("Arial", 12))
get_weather_button.pack(pady=20)

# عرض معلومات الطقس
weather_label = Label(root, textvariable=weather_info, bg="white", font=("Arial", 12), justify=LEFT)
weather_label.pack(pady=20)

# تشغيل النافذة
root.mainloop()