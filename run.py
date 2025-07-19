#!/usr/bin/env python3
"""
Gift Tinder - Main Runner
Запуск всех компонентов приложения
"""

import os
import sys
import subprocess
import time
import signal
import threading
from pathlib import Path

def check_dependencies():
    """Проверка наличия необходимых зависимостей"""
    try:
        import fastapi
        import uvicorn
        import pyrogram
        import telegram
        print("✅ Все зависимости установлены")
        return True
    except ImportError as e:
        print(f"❌ Ошибка импорта: {e}")
        print("Установите зависимости: pip install -r requirements.txt")
        return False

def check_config():
    """Проверка конфигурации"""
    required_vars = [
        'BOT_TOKEN',
        'API_ID', 
        'API_HASH',
        'WEBAPP_URL'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Отсутствуют переменные окружения: {', '.join(missing_vars)}")
        print("Создайте файл .env с необходимыми переменными")
        return False
    
    print("✅ Конфигурация проверена")
    return True

def run_backend():
    """Запуск backend API"""
    print("🚀 Запуск Backend API...")
    try:
        os.chdir("backend")
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--reload", 
            "--host", "0.0.0.0", 
            "--port", "8000"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка запуска backend: {e}")
    except KeyboardInterrupt:
        print("⏹️ Backend остановлен")

def run_userbot():
    """Запуск userbot"""
    print("🤖 Запуск Userbot...")
    try:
        os.chdir("userbot")
        subprocess.run([
            sys.executable, "run.py"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка запуска userbot: {e}")
    except KeyboardInterrupt:
        print("⏹️ Userbot остановлен")

def run_bot():
    """Запуск Telegram бота"""
    print("📱 Запуск Telegram Bot...")
    try:
        os.chdir("..")
        subprocess.run([
            sys.executable, "bot.py"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка запуска bot: {e}")
    except KeyboardInterrupt:
        print("⏹️ Bot остановлен")

def main():
    """Главная функция"""
    print("🎁 Gift Tinder - Запуск приложения")
    print("=" * 50)
    
    # Проверки
    if not check_dependencies():
        return
    
    if not check_config():
        return
    
    print("\n📋 Доступные команды:")
    print("1. backend  - Запустить только Backend API")
    print("2. userbot  - Запустить только Userbot")
    print("3. bot      - Запустить только Telegram Bot")
    print("4. all      - Запустить все компоненты")
    print("5. dev      - Запустить в режиме разработки")
    print("6. exit     - Выход")
    
    while True:
        try:
            choice = input("\nВыберите команду: ").strip().lower()
            
            if choice == "exit":
                print("👋 До свидания!")
                break
                
            elif choice == "backend":
                run_backend()
                
            elif choice == "userbot":
                run_userbot()
                
            elif choice == "bot":
                run_bot()
                
            elif choice == "all":
                print("🚀 Запуск всех компонентов...")
                
                # Запуск в отдельных потоках
                backend_thread = threading.Thread(target=run_backend, daemon=True)
                userbot_thread = threading.Thread(target=run_userbot, daemon=True)
                bot_thread = threading.Thread(target=run_bot, daemon=True)
                
                backend_thread.start()
                time.sleep(2)
                
                userbot_thread.start()
                time.sleep(2)
                
                bot_thread.start()
                
                print("✅ Все компоненты запущены")
                print("Нажмите Ctrl+C для остановки")
                
                try:
                    while True:
                        time.sleep(1)
                except KeyboardInterrupt:
                    print("\n⏹️ Остановка всех компонентов...")
                    break
                    
            elif choice == "dev":
                print("🔧 Запуск в режиме разработки...")
                print("Backend будет доступен на http://localhost:8000")
                print("Frontend откройте frontend/index.html в браузере")
                
                run_backend()
                
            else:
                print("❌ Неизвестная команда")
                
        except KeyboardInterrupt:
            print("\n⏹️ Остановка...")
            break
        except Exception as e:
            print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    main() 