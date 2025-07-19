# 🚀 Настройка Gift Tinder

## Шаг 1: Подготовка окружения

### Установка Python
Убедитесь, что у вас установлен Python 3.8+:
```bash
python --version
```

### Создание виртуального окружения
```bash
# Создание окружения
python -m venv venv

# Активация (Windows)
venv\Scripts\activate

# Активация (macOS/Linux)
source venv/bin/activate
```

### Установка зависимостей
```bash
pip install -r requirements.txt
```

## Шаг 2: Настройка Telegram

### Создание бота
1. Откройте Telegram
2. Найдите [@BotFather](https://t.me/BotFather)
3. Отправьте команду `/newbot`
4. Следуйте инструкциям для создания бота
5. Сохраните полученный токен

### Получение API ключей
1. Перейдите на [my.telegram.org](https://my.telegram.org)
2. Войдите в свой аккаунт
3. Создайте новое приложение
4. Запишите `api_id` и `api_hash`

## Шаг 3: Создание конфигурации

Создайте файл `.env` в корне проекта:

```env
# Telegram Bot
BOT_TOKEN=ваш_токен_бота
BOT_USERNAME=ваш_username_бота

# Telegram API
API_ID=ваш_api_id
API_HASH=ваш_api_hash

# База данных
DB_URL=sqlite:///./gift_tinder.db

# Безопасность
SECRET_KEY=измените_этот_ключ_в_продакшене
WEBAPP_URL=https://ваш-домен.com

# Отладка
DEBUG=True
```

## Шаг 4: Настройка базы данных

База данных создастся автоматически при первом запуске backend.

## Шаг 5: Запуск компонентов

### Backend API
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Userbot (в отдельном терминале)
```bash
cd userbot
python run.py
```

### Telegram Bot (в отдельном терминале)
```bash
python bot.py
```

## Шаг 6: Настройка Frontend

### Локальная разработка
1. Откройте `frontend/index.html` в браузере
2. Или используйте локальный сервер:
```bash
cd frontend
python -m http.server 8080
```

### Продакшн деплой
1. Загрузите папку `frontend/` на Vercel/Netlify
2. Обновите `WEBAPP_URL` в `.env`

## Шаг 7: Тестирование

1. Откройте бота в Telegram
2. Отправьте `/start`
3. Нажмите кнопку "Gift Tinder"
4. Протестируйте функционал

## Возможные проблемы

### Ошибка импорта модулей
```bash
pip install -r requirements.txt
```

### Ошибка подключения к API
Проверьте правильность `API_ID` и `API_HASH`

### Ошибка токена бота
Проверьте правильность `BOT_TOKEN`

### Ошибка CORS
Добавьте домен в настройки бота через @BotFather

## Полезные команды

### Просмотр логов
```bash
# Backend
tail -f backend.log

# Userbot
tail -f userbot.log

# Bot
tail -f bot.log
```

### Очистка базы данных
```bash
rm gift_tinder.db
```

### Обновление зависимостей
```bash
pip install --upgrade -r requirements.txt
```

## Следующие шаги

1. Настройте домен для frontend
2. Настройте SSL сертификат
3. Настройте мониторинг
4. Добавьте логирование
5. Настройте резервное копирование БД 