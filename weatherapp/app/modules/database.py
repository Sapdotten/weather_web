import sqlite3


class WeatherRequestsManager:
    DATABASE_FILE = "data/weather_requests.db"

    @classmethod
    def create_table(cls):
        conn = sqlite3.connect(cls.DATABASE_FILE)
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS weather_requests
                     (city TEXT, count INTEGER)""")
        conn.commit()
        conn.close()

    @classmethod
    def increase_request_counter(cls, city):
        conn = sqlite3.connect(cls.DATABASE_FILE)
        c = conn.cursor()

        c.execute("SELECT count FROM weather_requests WHERE city = ?", (city,))
        result = c.fetchone()
        if result:
            count = result[0] + 1
        else:
            count = 1

        c.execute(
            "INSERT OR REPLACE INTO weather_requests (city, count) VALUES (?, ?)", (city, count))
        conn.commit()
        conn.close()

    @classmethod
    def decrease_request_count(cls, city):
        conn = sqlite3.connect(cls.DATABASE_FILE)
        c = conn.cursor()

        # Поиск города в базе данных
        c.execute("SELECT count FROM weather_requests WHERE city = ?", (city,))
        result = c.fetchone()
        if result:
            # Уменьшение счетчика, но не меньше 0
            count = max(result[0] - 1, 0)

            # Обновление данных в базе
            c.execute(
                "UPDATE weather_requests SET count = ? WHERE city = ?", (count, city))
            conn.commit()

        conn.close()

    @classmethod
    def get_request_count(cls, city):
        conn = sqlite3.connect(cls.DATABASE_FILE)
        c = conn.cursor()

        c.execute("SELECT count FROM weather_requests WHERE city = ?", (city,))
        result = c.fetchone()
        conn.close()
        if result:
            return result[0]
        else:
            return 0


WeatherRequestsManager.create_table()
