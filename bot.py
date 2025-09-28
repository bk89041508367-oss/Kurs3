import os
import requests
import asyncio
from datetime import datetime, timedelta
from telegram import Bot
from telegram.constants import ParseMode

# === ОБХОД ДЛЯ RENDER WEB SERVICES ===
if "RENDER" in os.environ:
    import http.server
    import socketserver
    from threading import Thread
    
    def run_dummy_server():
        PORT = 8000
        with socketserver.TCPServer(("", PORT), http.server.SimpleHTTPRequestHandler) as httpd:
            print(f"✅ HTTP server running on port {PORT}")
            httpd.serve_forever()
    
    server_thread = Thread(target=run_dummy_server, daemon=True)
    server_thread.start()

# === КОНФИГУРАЦИЯ ===
BOT_TOKEN = os.environ.get('BOT_TOKEN', '7984110017:AAEopXIz-0wFOsXlOeWeLvJTzlijxyPLyrU')
CHANNEL_ID = os.environ.get('CHANNEL_ID', '@FinRadar67')

# ПРОВЕРКА ПЕРЕМЕННЫХ
if not BOT_TOKEN or BOT_TOKEN == 'BOT_TOKEN':
    print("❌ Ошибка: Не установлен BOT_TOKEN")
    exit(1)

if not CHANNEL_ID or CHANNEL_ID == '@FinRadar67':
    print("❌ Ошибка: Не установлен CHANNEL_ID")
    exit(1)

# === ФУНКЦИИ ДЛЯ КУРСОВ ===
def get_usd_rub():
    """Получает курс USD/RUB"""
    try:
        url = "https://www.cbr-xml-daily.ru/daily_json.js"
        response = requests.get(url, timeout=10)
        data = response.json()
        current_rate = data['Valute']['USD']['Value']
        previous_rate = data['Valute']['USD']['Previous']
        change = ((current_rate - previous_rate) / previous_rate) * 100
        change_str = f"({change:+.1f}%)"
        return f"{current_rate:.2f} ₽ {change_str}"
    except:
        return "❌ Ошибка"

# ... ОСТАЛЬНЫЕ ВАШИ ФУНКЦИИ ОСТАЮТСЯ БЕЗ ИЗМЕНЕНИЙ ...

def get_eur_rub():
    """Получает курс EUR/RUB"""
    try:
        url = "https://www.cbr-xml-daily.ru/daily_json.js"
        response = requests.get(url, timeout=10)
        data = response.json()
        current_rate = data['Valute']['EUR']['Value']
        previous_rate = data['Valute']['EUR']['Previous']
        change = ((current_rate - previous_rate) / previous_rate) * 100
        change_str = f"({change:+.1f}%)"
        return f"{current_rate:.2f} ₽ {change_str}"
    except:
        return "❌ Ошибка"

def get_cny_rub():
    """Получает курс CNY/RUB"""
    try:
        url = "https://www.cbr-xml-daily.ru/daily_json.js"
        response = requests.get(url, timeout=10)
        data = response.json()
        current_rate = data['Valute']['CNY']['Value']
        previous_rate = data['Valute']['CNY']['Previous']
        change = ((current_rate - previous_rate) / previous_rate) * 100
        change_str = f"({change:+.1f}%)"
        return f"{current_rate:.2f} ₽ {change_str}"
    except:
        return "❌ Ошибка"

def get_thb_rub():
    """Получает курс THB/RUB"""
    try:
        url = "https://www.cbr-xml-daily.ru/daily_json.js"
        response = requests.get(url, timeout=10)
        data = response.json()
        current_rate = data['Valute']['THB']['Value']
        previous_rate = data['Valute']['THB']['Previous']
        change = ((current_rate - previous_rate) / previous_rate) * 100
        change_str = f"({change:+.1f}%)"
        return f"{current_rate:.4f} ₽ {change_str}"
    except:
        return "❌ Ошибка"

def get_vnd_rub():
    """Получает курс 1000 VND к RUB"""
    try:
        url = "https://www.cbr-xml-daily.ru/daily_json.js"
        response = requests.get(url, timeout=10)
        data = response.json()
        usd_rate = data['Valute']['USD']['Value']
        rub_per_1000vnd = (usd_rate / 23000) * 1000
        return f"1000₫ = {rub_per_1000vnd:.2f} ₽"
    except:
        return "❌ Ошибка"

def get_gold_rub():
    """Получает курс золота в рублях"""
    try:
        # Курс золота в USD
        gold_usd = 1950.50
        
        # Получаем курс USD/RUB
        url = "https://www.cbr-xml-daily.ru/daily_json.js"
        response = requests.get(url, timeout=10)
        data = response.json()
        usd_rate = data['Valute']['USD']['Value']
        
        # Конвертируем в рубли
        gold_rub = gold_usd * usd_rate
        return f"{gold_rub:,.0f} ₽".replace(",", " ")
    except:
        return "❌ Ошибка"

def create_message():
    """Создает текст сообщения только с валютами"""
    usd = get_usd_rub()
    eur = get_eur_rub()
    cny = get_cny_rub()
    thb = get_thb_rub()
    vnd = get_vnd_rub()
    gold = get_gold_rub()
    
    # Время
    msk_time = datetime.now().strftime("%H:%M:%S %d.%m.%Y")
    irk_time = (datetime.now() + timedelta(hours=5)).strftime("%H:%M:%S %d.%m.%Y")
    
    # Извлекаем числовые значения для первой строки
    usd_value = usd.split()[0] if '❌' not in usd else '❌'
    eur_value = eur.split()[0] if '❌' not in eur else '❌'
    
    message = f"""
💵USD: {usd_value} 💶EUR: {eur_value}

📊 АКТУАЛЬНЫЕ КУРСЫ (ЦБ РФ)

💵 USD/RUB: {usd}
💶 EUR/RUB: {eur}
🇨🇳 CNY/RUB: {cny}
🇹🇭 THB/RUB: {thb}
🇻🇳 VND/RUB: {vnd}
🥇 Золото: {gold}

Последнее обновление:
🕐 Москва: {msk_time}
🕐 Иркутск: {irk_time}

*Криптовалюты временно отключены*
"""
    return message

# === ПРОВЕРКА ПОДКЛЮЧЕНИЯ ===
async def check_bot_connection():
    """Проверяет подключение бота"""
    print("🔍 Проверяем подключение к Telegram...")
    
    try:
        bot = Bot(token=BOT_TOKEN)
        me = await bot.get_me()
        print(f"✅ Бот подключен: @{me.username} ({me.first_name})")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        return False

# === ОСНОВНАЯ ЛОГИКА ===
async def main():
    print("=" * 60)
    print("💰 TELEGRAM БОТ ДЛЯ КУРСОВ ВАЛЮТ (УПРОЩЕННАЯ ВЕРСИЯ)")
    print("=" * 60)
    
    # Проверяем подключение
    if not await check_bot_connection():
        return
    
    # Запускаем основную логику
    bot = Bot(token=BOT_TOKEN)
    
    print("🚀 Отправляем сообщение в канал...")
    
    retry_count = 0
    max_retries = 3
    
    while True:
        try:
            if retry_count == 0:
                # Первая отправка сообщения
                message = await bot.send_message(
                    chat_id=CHANNEL_ID,
                    text=create_message(),
                    parse_mode=ParseMode.MARKDOWN
                )
                print("✅ Сообщение отправлено! Запускаем автообновление...")
            else:
                # Повторная отправка после ошибки
                message = await bot.send_message(
                    chat_id=CHANNEL_ID,
                    text=create_message(),
                    parse_mode=ParseMode.MARKDOWN
                )
                print("✅ Переподключение успешно! Сообщение отправлено зановo.")
                retry_count = 0
            
            # Основной цикл обновления
            while retry_count < max_retries:
                try:
                    await asyncio.sleep(300)  # 5 минут
                    await bot.edit_message_text(
                        chat_id=CHANNEL_ID,
                        message_id=message.message_id,
                        text=create_message(),
                        parse_mode=ParseMode.MARKDOWN
                    )
                    print(f"✅ Обновлено: {datetime.now().strftime('%H:%M:%S')}")
                    retry_count = 0
                    
                except Exception as e:
                    print(f"❌ Ошибка при обновлении: {e}")
                    retry_count += 1
                    if retry_count >= max_retries:
                        print("🔄 Превышено количество попыток, перезапускаем соединение...")
                        break
                    else:
                        print(f"🔄 Повторная попытка {retry_count}/{max_retries} через 30 секунд...")
                        await asyncio.sleep(30)
            
        except Exception as e:
            print(f"❌ Критическая ошибка: {e}")
            print("🔄 Перезапуск через 60 секунд...")
            await asyncio.sleep(60)
            retry_count = 0 if retry_count >= max_retries else retry_count + 1

if __name__ == "__main__":
    asyncio.run(main())



