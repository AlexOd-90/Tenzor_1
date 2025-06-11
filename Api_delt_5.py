import requests
import datetime
from statistics import mean  # mean для вычисления среднего значения

# Функция для получения времени от API
def get_time_from_api():

    try:
        # Отправляем GET-запрос к API
        request_start = datetime.datetime.now(datetime.timezone.utc)
        response = requests.get(
            'https://yandex.com/time/sync.json?geo=213',
            timeout=5
        )
        response.raise_for_status()  # Проверяем наличие ошибок

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
    # Переводим миллисекунды в секунды
    timestamp_seconds = timestamp_ms / 1000
    offset_seconds = offset_ms / 1000

    # Создаем временную зону
    tzinfo = datetime.timezone(datetime.timedelta(seconds=offset_seconds))

    # Создаем datetime с учетом временной зоны
    dt = datetime.datetime.fromtimestamp(timestamp_seconds, tz=tzinfo)
    return dt

#Вычисляем задержку
def calculate_time_delay(request_start, request_end):
    time_delay = (request_end - request_start) / 2
    return time_delay


def perform_multiple_requests():

    delays = []
    request_times = []
    all_results = []

    for i in range(5):
        print(f"\n--- Запрос #{i + 1} ---")
        data, request_start, request_end = get_time_from_api()

        if data:
            # Извлекаем данные из ответа API
            timestamp_ms = data['time']
            offset_ms = data['clocks']['213']['offset']
            timezone_str = data['clocks']['213']['offsetString']

            # Форматируем время для вывода
            api_time = format_timestamp(timestamp_ms, offset_ms)
            formatted_time = api_time.strftime('%d.%m.%Y %H:%M:%S %Z')

            # Рассчитываем дельту в миллисекундах
            time_delay = calculate_time_delay(request_start, request_end)
            network_delay_ms = time_delay.total_seconds() * 1000
            request_time_ms = (request_end - request_start).total_seconds() * 1000

            # Сохраняем результаты
            delays.append(network_delay_ms)
            request_times.append(request_time_ms)
            all_results.append({
                'request_num': i + 1,
                'time': formatted_time,
                'network_delay_ms': network_delay_ms,
                'request_time_ms': request_time_ms,
                'timestamp': timestamp_ms,
                'timezone': timezone_str
            })

            # Выводим информацию о текущем запросе
            print(f"Текущее время: {formatted_time}")
            print(f"Сетевая задержка: {network_delay_ms:.3f} мс")
            print(f"Время выполнения запроса: {request_time_ms:.3f} мс")

        else:
            print("Не удалось получить данные о времени")
            all_results.append({
                'request_num': i + 1,
                'error': True
            })

    # Рассчитываем средние значения
    avg_delay = mean(delays) if delays else 0
    avg_request_time = mean(request_times) if request_times else 0

    return avg_delay, avg_request_time, all_results


def main():

    avg_delay, avg_request_time, all_results = perform_multiple_requests()

    # Выводим сводную статистику
    print("\n=== Итоговая статистика ===")
    print(f"Средняя сетевая задержка: {avg_delay:.3f} мс")
    print(f"Среднее время запроса: {avg_request_time:.3f} мс")

    # Дополнительно можно сохранить all_results в файл или БД


if __name__ == "__main__":
    main()