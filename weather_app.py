import os
import sys
import requests
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_weather(city: str) -> dict:
   
    if not API_KEY:
        raise ValueError("API-ключ не найден. Проверьте файл .env")

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric", 
        "lang": "ru"        
    }

 
    response = requests.get(BASE_URL, params=params, timeout=5)


    if response.status_code == 401:
        raise PermissionError("Неверный API-ключ (код 401)")
    if response.status_code == 404:
        raise FileNotFoundError(f"Город '{city}' не найден (код 404)")


    try:
        response.raise_for_status()
    except requests.exceptions.Timeout:
        raise TimeoutError("Превышено время ожидания ответа (таймаут 5 сек)")
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Сетевая ошибка: {e}")


    data = response.json()

    return {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "description": data["weather"][0]["description"],
        "humidity": data["main"]["humidity"],
        "wind": data["wind"]["speed"]
    }


if __name__ == "__main__":

    if len(sys.argv) > 1:
        city = " ".join(sys.argv[1:])
    else:
        city = input("Введите название города: ").strip()

    if not city:
        print("Ошибка: название города не может быть пустым.")
        sys.exit(1)

    try:
        weather = get_weather(city)


        print("\n Погода ")
        print(f"Город:        {weather['city']}")
        print(f"Температура:  {weather['temperature']}°C")
        print(f"Описание:     {weather['description']}")
        print(f"Влажность:    {weather['humidity']}%")
        print(f"Ветер:        {weather['wind']} м/с")


    except (PermissionError, FileNotFoundError, TimeoutError, ConnectionError, ValueError) as e:
        print(f"\n Ошибка: {e}\n")
        sys.exit(1)
