# Используем базовый образ Python
FROM python:3.9

# Устанавливаем рабочую директорию в контейнере
WORKDIR /weatherapp

# Копируем файл зависимостей в рабочую директорию
COPY requirements.txt requirements.txt

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все содержимое текущей директории в рабочую директорию контейнера
COPY weatherapp/ .

# Копируем файл .env
COPY env.txt .env

# Экспонируем порт 5000
EXPOSE 5000

# Указываем команду для запуска приложения
CMD ["python", "app/main.py"]
