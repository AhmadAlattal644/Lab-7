import requests

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
        
        # عرض البيانات بشكل منسق
        print(f"Погода в {city}, {country}:")
        print(f"Температура: {temp}°C")
        print(f"Влажность: {humidity}%")
        print(f"Атмосферное давление: {pressure} hPa")
        print(f"Описание: {weather_desc.capitalize()}")
        print("-" * 30)  # فاصل بين المدن
        
    except requests.exceptions.RequestException as e:
        print(f"Произошла ошибка при получении данных для города {city_name}: {e}")
    except KeyError as e:
        print(f"Ошибка в данных для города {city_name}: {e}")

def choose_city():
    # قائمة المدن
    cities = {
        1: "Moscow",
        2: "Saint Petersburg",
        3: "Novosibirsk",
        4: "Yekaterinburg",
        5: "Kazan"
    }
    
    while True:
        # عرض القائمة للمستخدم
        print("Выберите город:")
        for key, city in cities.items():
            print(f"{key}. {city}")
        
        # طلب إدخال من المستخدم
        try:
            choice = int(input("Введите номер города: "))
            if choice in cities:
                selected_city = cities[choice]
                get_weather(selected_city, api_key)  # جلب بيانات الطقس للمدينة المختارة
            else:
                print("Неверный выбор. Пожалуйста, выберите номер из списка.")
        except ValueError:
            print("Неверный ввод. Пожалуйста, введите число.")

if __name__ == "__main__":
    # مفتاح API
    api_key = "b67c58f69b9b4084d425b4935230a194"  # استبدل بمفتاح API الخاص بك إذا لزم الأمر
    
    # تشغيل الدالة لاختيار المدينة
    choose_city()