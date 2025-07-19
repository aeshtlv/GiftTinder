# 🎁 Gift Tinder

**Gift Tinder** — это свайп-приложение внутри Telegram (Mini App), позволяющее пользователям оценивать Telegram Gifts друг друга. Если два пользователя лайкнули подарки друг друга — происходит мэтч, и открывается возможность чата.

## 🚀 Быстрый старт

### 1. Установка зависимостей

```bash
# Создание виртуального окружения
python -m venv venv

# Активация окружения
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt
```

### 2. Настройка конфигурации

Создайте файл `.env` в корне проекта:

```env
# Telegram Bot
BOT_TOKEN=your_bot_token_here
BOT_USERNAME=your_bot_username

# Telegram API (получите на https://my.telegram.org)
API_ID=1234567
API_HASH=your_api_hash_here

# База данных
DB_URL=sqlite:///./gift_tinder.db

# Безопасность
SECRET_KEY=your-secret-key-change-this
WEBAPP_URL=https://your-domain.com

# Отладка
DEBUG=True
```

### 3. Создание Telegram Bot

1. Напишите [@BotFather](https://t.me/BotFather) в Telegram
2. Создайте нового бота командой `/newbot`
3. Получите токен бота и добавьте в `.env`

### 4. Получение Telegram API

1. Перейдите на [my.telegram.org](https://my.telegram.org)
2. Войдите в свой аккаунт
3. Создайте новое приложение
4. Получите `API_ID` и `API_HASH`
5. Добавьте в `.env`

### 5. Запуск компонентов

#### Backend API
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Userbot (для синхронизации подарков)
```bash
cd userbot
python run.py
```

#### Telegram Bot
```bash
python bot.py
```

#### Frontend (Mini App)
Загрузите папку `frontend/` на любой статический хостинг:
- Vercel
- Netlify
- GitHub Pages
- Render

## 📁 Структура проекта

```
gift_tinder/
├── bot.py                 # Telegram бот
├── backend/
│   ├── main.py           # FastAPI сервер
│   ├── database.py       # Настройки БД
│   ├── models.py         # Модели данных
│   └── utils.py          # Утилиты
├── userbot/
│   ├── run.py            # Запуск userbot
│   └── tasks.py          # Задачи userbot
├── frontend/
│   ├── index.html        # Главная страница
│   ├── style.css         # Стили
│   └── app.js           # JavaScript логика
├── config.py             # Конфигурация
├── requirements.txt      # Зависимости
└── README.md            # Документация
```

## 🔗 API Endpoints

### Пользователи
- `GET /api/user/{telegram_id}` - Получить пользователя
- `POST /api/user` - Создать/обновить пользователя

### Подарки
- `GET /api/gifts/{telegram_id}` - Получить подарки пользователя
- `POST /api/sync_gifts/{telegram_id}` - Синхронизировать подарки
- `GET /api/next_gift/{telegram_id}` - Следующий подарок для свайпа

### Свайпы и мэтчи
- `POST /api/swipe` - Записать свайп
- `GET /api/matches/{telegram_id}` - Получить мэтчи пользователя

## 🎯 Основные функции

### ✅ Реализовано
- [x] Регистрация пользователей через Telegram WebApp
- [x] Автоматическая синхронизация подарков через Pyrogram
- [x] Свайп-интерфейс для оценки подарков
- [x] Система мэтчей при взаимных лайках
- [x] Профиль пользователя со статистикой
- [x] Просмотр мэтчей
- [x] Современный адаптивный дизайн
- [x] Безопасность через Telegram WebApp API

### 🔄 В разработке
- [ ] Чат между мэтчами
- [ ] Уведомления о новых мэтчах
- [ ] Фильтры по типам подарков
- [ ] Статистика и аналитика
- [ ] Модерация контента

## 🛠 Технологии

- **Frontend**: HTML5, CSS3, JavaScript, Telegram WebApp API
- **Backend**: Python, FastAPI, SQLAlchemy
- **Database**: SQLite (можно PostgreSQL)
- **Userbot**: Pyrogram
- **Bot**: python-telegram-bot
- **Hosting**: Vercel/Netlify для frontend, любой VPS для backend

## 🔐 Безопасность

- Валидация данных через Telegram WebApp API
- Проверка подписи initData
- Лимиты на действия пользователей
- Userbot работает только с видимыми пользователями
- Защита от спама и злоупотреблений

## 📱 Использование

1. Пользователь открывает бота в Telegram
2. Нажимает кнопку "Gift Tinder" для запуска Mini App
3. Авторизуется через Telegram WebApp API
4. Свайпает подарки других пользователей
5. При взаимном лайке происходит мэтч
6. Просматривает мэтчи в профиле

## 🚀 Деплой

### Backend (VPS)
```bash
# Установка на сервере
git clone <repository>
cd gift_tinder
pip install -r requirements.txt

# Настройка systemd сервиса
sudo nano /etc/systemd/system/gift-tinder-api.service
```

### Frontend (Vercel)
1. Создайте аккаунт на [vercel.com](https://vercel.com)
2. Подключите GitHub репозиторий
3. Настройте деплой папки `frontend/`
4. Обновите `WEBAPP_URL` в конфигурации

## 🤝 Разработка

### Добавление новых функций
1. Создайте ветку: `git checkout -b feature/new-feature`
2. Внесите изменения
3. Протестируйте локально
4. Создайте Pull Request

### Тестирование
```bash
# Запуск тестов
python -m pytest tests/

# Линтинг
flake8 backend/
```

## 📞 Поддержка

- **Автор**: [@aeshtlv](https://t.me/aeshtlv)
- **Лицензия**: MIT
- **Версия**: 1.0.0

## 📄 Лицензия

MIT License - см. файл [LICENSE](LICENSE) для деталей.

---

**Gift Tinder** - находите людей по подаркам! 🎁💕 