import requests
import datetime


# Функция для получения времени от API
def get_time_from_api():
    try:
        # Отправляем GET-запрос к API
        request_start = datetime.datetime.now(datetime.timezone.utc)
        response = requests.get(
            'https://yandex.com/time/sync.json?geo=213',
            timeout=5
        )
        response.raise_for_status()   # Проверяем наличие ошибок

        # Фиксируем время получения ответа
        request_end = datetime.datetime.now(datetime.timezone.utc)

        # Парсим JSON-ответ
        data = response.json()
        return data, request_start, request_end
    except requests.RequestException as e:
        print(f"Ошибка при получении времени: {e}")
        return None, None, None


# Функция для форматирования временной метки
def format_timestamp(timestamp_ms, offset_ms):
    # Преобразуем миллисекунды в секунды
    timestamp_seconds = timestamp_ms / 1000
    offset_seconds = offset_ms / 1000

    # Создаем временную зону
    tzinfo = datetime.timezone(datetime.timedelta(seconds=offset_seconds))

    # Создаем объект datetime с учетом временной зоны
    dt = datetime.datetime.fromtimestamp(timestamp_seconds, tz=tzinfo)
    return dt

#Вычисляем задержку
def calculate_time_delay(request_start, request_end):
    time_delay = (request_end - request_start) / 2
    return time_delay


# Основная функция
def main():
    data, request_start, request_end = get_time_from_api()

    if data:
        # Получаем данные из API
        timestamp_ms = data['time']
        offset_ms = data['clocks']['213']['offset']
        timezone_str = data['clocks']['213']['offsetString']

        # Форматируем время с учетом часового пояса
        api_time = format_timestamp(timestamp_ms, offset_ms)
        formatted_time = api_time.strftime('%d.%m.%Y %H:%M:%S %Z')

        # Вычисляем задержку
        time_delay = calculate_time_delay(request_start, request_end)
        network_delay_ms = time_delay.total_seconds() * 1000
        request_time_ms = (request_end - request_start).total_seconds() * 1000

        # Выводим результаты
        print(f"Текущее время: {formatted_time}")
        print(f"Сетевая задержка: {network_delay_ms:.3f} мс")
        print(f"Время выполнения запроса: {request_time_ms:.3f} мс")

        # Дополнительная информация
        print("\nДополнительная информация:")
        print(f"Метка времени API: {timestamp_ms} мс")
        print(f"Часовой пояс: {timezone_str}")
    else:
        print("Не удалось получить данные о времени")

if __name__ == "__main__":
    main()