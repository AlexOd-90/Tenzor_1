import requests
import datetime
import json


# Функция для получения времени от API
def get_time_from_api():
    try:
        # Отправляем GET-запрос к API
        response = requests.get(
            'https://yandex.com/time/sync.json?geo=213',
            timeout=5
        )
        response.raise_for_status()  # Проверяем наличие ошибок

        # Парсим JSON-ответ
        data = response.json()
        return data
    except requests.RequestException as e:
        print(f"Ошибка при получении времени: {e}")
        return None


# Функция для форматирования временной метки
def format_timestamp(timestamp):
    # Преобразуем миллисекунды в секунды
    timestamp_seconds = timestamp / 1000

    # Создаем объект datetime
    dt = datetime.datetime.fromtimestamp(timestamp_seconds)

    # Форматируем дату в читаемый вид
    formatted_date = dt.strftime('%d.%m.%Y %H:%M:%S')
    return formatted_date


# Основная функция
def main():
    # Получаем данные от API
    data = get_time_from_api()

    if data:
        # Извлекаем временную метку
        timestamp = data['time']

        # Форматируем и выводим результат
        formatted_time = format_timestamp(timestamp)
        print(f"Текущее время: {formatted_time}")

        # Выводим дополнительную информацию
        city_info = data['clocks']['213']
        #print(f"Город: {city_info['name']}")
        print(f"Часовой пояс: {city_info['offsetString']}")
        #print(f"Восход солнца: {city_info['sunrise']}")
        #print(f"Закат солнца: {city_info['sunset']}")
        #print(f"Текущая температура: {city_info['weather']['temp']}°C")
    else:
        print("Не удалось получить данные о времени")


if __name__ == "__main__":
    main()
