import requests
import json


def get_time_data():

    try:
        # Выполняем GET-запрос с таймаутом 5 секунд
        response = requests.get(
            "https://yandex.com/time/sync.json?geo=213",
            timeout=5
        )
        response.raise_for_status()  # Проверяем на ошибки HTTP

        # Парсим JSON ответ
        json_data = response.json()

        # Выводим  отформатированный JSON
        print(json.dumps(json_data, indent=2, ensure_ascii=False))

        return json_data

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при выполнении запроса: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Ошибка при разборе JSON: {e}")
        return None

if __name__ == "__main__":
    time_data = get_time_data()
