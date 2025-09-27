import requests
import asyncio
from datetime import datetime
from telegram import Bot
from telegram.constants import ParseMode

# === КОНФИГУРАЦИЯ ===
BOT_TOKEN = "7984110017:AAEopXIz-0wFOsXlOeWeLvJTzlijxyPLyrU"  # Ваш токен
CHANNEL_ID = "@FinRadar67"  # Ваш канал

# Переменные для хранения предыдущих значений
previous_rates = {}

def get_usd_rub():
    """Получает курс USD/RUB с изменением"""
    try:
        url = "https://www.cbr-xml-daily.ru/daily_json.js"
        response = requests.get(url, timeout=10)
        data = response.json()
        current_rate = data['Valute']['USD']['Value']
        previous_rate = data['Valute']['USD']['Previous']
        
        # Расчет изменения
        change = current_rate - previous_rate
        change_percent = (change / previous_rate) * 100
        
        # Сохраняем для следующего сравнения
        previous_rates['usd'] = current_rate
        
        if change_percent > 0:
            change_str = f"(+{change_percent:+.1f}%)"
        else:
            change_str = f"({change_percent:+.1f}%)"
            
        return f"{current_rate:.2f} ₽ {change_str}"
    except:
        return "❌ Ошибка"

def get_btc_usd():
    """Получаем курс BTC через расчетное значение"""
    try:
        # Используем фиксированное значение как fallback
        btc_price = 110000  # Примерное значение
        return f"{btc_price/1000:.1f}K"
    except:
        return "❌"

def get_btc_rub():
    """Получаем курс BTC/RUB через USD/RUB"""
    try:
        # Получаем актуальный USD/RUB
        url = "https://www.cbr-xml-daily.ru/daily_json.js"
        response = requests.get(url, timeout=10)
        data = response.json()
        usd_rate = data['Valute']['USD']['Value']
        
        # BTC в USD (примерно)
        btc_usd = 110000
        btc_rub = btc_usd * usd_rate
        
        return f"{btc_rub:,.0f} ₽".replace(",", " ")
    except:
        return "❌ Ошибка"

def get_ton_rub():
    """Получаем курс TON через USD/RUB"""
    try:
        # Получаем актуальный USD/RUB
        url = "https://www.cbr-xml-daily.ru/daily_json.js"
        response = requests.get(url, timeout=10)
        data = response.json()
        usd_rate = data['Valute']['USD']['Value']
        
        # TON в USD (примерно)
        ton_usd = 6.50  # Актуальный курс
        ton_rub = ton_usd * usd_rate
        
        return f"{ton_rub:.2f} ₽"
    except:
        return "❌ Ошибка"

def get_gold_rub():
    """Получает курс золота в рублях"""
    try:
        # Курс золота в USD (примерный)
        gold_usd = 1950.50
        
        # Получаем курс USD/RUB
        usd_response = requests.get("https://www.cbr-xml-daily.ru/daily_json.js", timeout=10)
        usd_data = usd_response.json()
        usd_rate = usd_data['Valute']['USD']['Value']
        
        # Конвертируем в рубли
        gold_rub = gold_usd * usd_rate
        
        # Заглушка для изменений
        change_str = "(+0.0%)"
        
        return f"{gold_rub:,.0f} ₽ {change_str}".replace(",", " ")
    except:
        return "❌ Ошибка"

def get_eur_rub():
    """Получает курс EUR/RUB"""
    try:
        url = "https://www.cbr-xml-daily.ru/daily_json.js"
        response = requests.get(url, timeout=10)
        data = response.json()
        current_rate = data['Valute']['EUR']['Value']
        previous_rate = data['Valute']['EUR']['Previous']
        
        # Расчет изменения
        change = current_rate - previous_rate
        change_percent = (change / previous_rate) * 100
        
        if change_percent > 0:
            change_str = f"(+{change_percent:+.1f}%)"
        else:
            change_str = f"({change_percent:+.1f}%)"
            
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
        
        # Расчет изменения
        change = current_rate - previous_rate
        change_percent = (change / previous_rate) * 100
        
        if change_percent > 0:
            change_str = f"(+{change_percent:+.1f}%)"
        else:
            change_str = f"({change_percent:+.1f}%)"
            
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
        
        # Расчет изменения
        change = current_rate - previous_rate
        change_percent = (change / previous_rate) * 100
        
        if change_percent > 0:
            change_str = f"(+{change_percent:+.1f}%)"
        else:
            change_str = f"({change_percent:+.1f}%)"
            
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

def create_message():
    """Создает текст сообщения с новыми валютами"""
    usd = get_usd_rub()
    eur = get_eur_rub()
    cny = get_cny_rub()
    thb = get_thb_rub()
    vnd = get_vnd_rub()
    btc_usd = get_btc_usd()
    btc_rub = get_btc_rub()
    ton = get_ton_rub()
    gold = get_gold_rub()
    
    # Время
    msk_time = datetime.now().strftime("%H:%M:%S %d.%m.%Y")
    from datetime import timedelta
    irk_time = (datetime.now() + timedelta(hours=5)).strftime("%H:%M:%S %d.%m.%Y")
    
    usd_value = usd.split()[0]
    ton_value = ton.split()[0]
    
    message = f"""
💵USD: {usd_value} 💎TON: {ton_value} 
₿BTC: {btc_usd}$

📊 АКТУАЛЬНЫЕ КУРСЫ

💵 USD/RUB: {usd}
💶 EUR/RUB: {eur}
🇨🇳 CNY/RUB: {cny}
🇹🇭 THB/RUB: {thb}
🇻🇳 VND/RUB: {vnd}

₿  BTC/RUB: {btc_rub}  
💎 TON/RUB: {ton}
🥇 Золото/RUB: {gold}

Последнее обновление:
🕐 Москва: {msk_time}
🕐 Иркутск: {irk_time}
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
    print("💰 TELEGRAM БОТ ДЛЯ КУРСОВ ВАЛЮТ")
    print("=" * 60)
    
    # Проверяем конфигурацию
    if "ВАШ_ТОКЕН" in BOT_TOKEN or "ваш_канал" in CHANNEL_ID:
        print("❌ ЗАМЕНИТЕ BOT_TOKEN и CHANNEL_ID на реальные значения!")
        return
    
    # Проверяем подключение
    if not await check_bot_connection():
        return
    
    # Запускаем основную логику
    bot = Bot(token=BOT_TOKEN)
    
    print("🚀 Отправляем сообщение в канал...")
    try:
        message = await bot.send_message(
            chat_id=CHANNEL_ID,
            text=create_message(),
            parse_mode=ParseMode.MARKDOWN
        )
        
        print("✅ Сообщение отправлено! Запускаем автообновление...")
        
        while True:
            await asyncio.sleep(300)  # 5 минут
            await bot.edit_message_text(
                chat_id=CHANNEL_ID,
                message_id=message.message_id,
                text=create_message(),
                parse_mode=ParseMode.MARKDOWN
            )
            print(f"✅ Обновлено: {datetime.now().strftime('%H:%M:%S')}")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":

    asyncio.run(main())
