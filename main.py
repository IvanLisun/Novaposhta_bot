import telebot
from telebot import types
from datetime import datetime

bot = telebot.TeleBot('7243990700:AAFLRhd5ZPQQX8G9gc7ISAUB6FbhK-XWy8o')

# === Кнопки ===
button_hi = types.KeyboardButton('Привіт! 👋')
button_commands = types.KeyboardButton('Доступні команди бота 📋')  # нова кнопка
greet_kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
greet_kb.add(button_hi)

main_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
main_kb.add(
    types.KeyboardButton("Знайти відділення 🏤"),
    types.KeyboardButton("Графік роботи 🕒"),
)
main_kb.add(
    types.KeyboardButton("Розташування 📍"),
    types.KeyboardButton("Доступні послуги 📦"),
    types.KeyboardButton("📅 Забронювати час"),
    button_commands  # додана кнопка
)

inline_kb = types.InlineKeyboardMarkup()
inline_button = types.InlineKeyboardButton("🌍 Перейти на сайт Нової Пошти", url="https://novaposhta.ua/")
inline_kb.add(inline_button)

# === Словник відділень ===
branches = {
    "київ": ["вул. Хрещатик, 10", "вул. Саксаганського, 45"],
    "харків": ["вул. Сумська, 35", "просп. Науки, 21"],
    "одеса": ["вул. Дерибасівська, 12", "просп. Шевченка, 4"],
    "дніпро": ["вул. Центральна, 15", "просп. Гагаріна, 20"],
    "львів": ["вул. Городоцька, 85", "просп. Чорновола, 67"],
    "запоріжжя": ["вул. Перемоги, 36", "просп. Соборний, 77"],
    "вінниця": ["вул. Соборна, 15", "вул. Келецька, 78"],
    "миколаїв": ["вул. Адміральська, 10", "просп. Центральний, 56"],
    "чернігів": ["вул. Шевченка, 23", "вул. Рокоссовського, 12"],
    "черкаси": ["вул. Смілянська, 43", "бул. Шевченка, 145"],
    "суми": ["вул. Харківська, 22", "вул. Козацький Вал, 3"],
    "полтава": ["вул. Європейська, 12", "вул. Шевченка, 77"],
    "івано-франківськ": ["вул. Незалежності, 24", "вул. Галицька, 125"],
    "ужгород": ["вул. Корзо, 13", "вул. Минайська, 23"],
    "тернопіль": ["вул. Руська, 18", "вул. Живова, 7"],
    "рівне": ["вул. Соборна, 110", "вул. Київська, 36"],
    "луцьк": ["просп. Волі, 15", "вул. Конякіна, 18"],
    "хмельницький": ["вул. Кам’янецька, 40", "вул. Зарічанська, 3"],
    "чернівці": ["вул. Головна, 123", "вул. Руська, 56"],
    "кропивницький": ["вул. Велика Перспективна, 89", "вул. Полтавська, 33"],
    "житомир": ["вул. Київська, 25", "вул. Перемоги, 10"]
}

# === Команда /start ===
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "👋 Вітаю у єдиному офіційному боті Нової Пошти у Telegram!",
        reply_markup=greet_kb
    )

@bot.message_handler(commands=['book_time'])
def book_time(message):
    msg = bot.send_message(message.chat.id, "📅 Введіть бажану дату відправлення (у форматі ДД.ММ.РРРР):")
    bot.register_next_step_handler(msg, ask_time)

def ask_time(message):
    date = message.text.strip()
    if not validate_date(date):
        msg = bot.send_message(message.chat.id, "❗️ Невірний формат дати. Спробуйте ще раз (ДД.ММ.РРРР):")
        bot.register_next_step_handler(msg, ask_time)
        return
    message.chat.booking_date = date
    msg = bot.send_message(message.chat.id, "⏰ Введіть бажаний час (у форматі ГГ:ХХ):")
    bot.register_next_step_handler(msg, confirm_booking, date)

def confirm_booking(message, date):
    time = message.text.strip()
    if not validate_time(time):
        msg = bot.send_message(message.chat.id, "❗️ Невірний формат часу. Спробуйте ще раз (ГГ:ХХ):")
        bot.register_next_step_handler(msg, confirm_booking, date)
        return
    bot.send_message(
        message.chat.id,
        f"✅ Ваше бронювання підтверджено!\n📦 Дата: {date}\n⏰ Час: {time}\nДякуємо, що обрали Нову Пошту!"
    )

@bot.message_handler(func=lambda message: message.text == "📅 Забронювати час")
def book_time_button(message):
    book_time(message)
# === Команда /help ===
@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(
        message.chat.id,
        "🛠 Доступні команди:\n"
        "/start — запуск бота\n"
        "/help — допомога\n"
        "/news — останні новини\n"
        "/track — відстежити посилку\n"
        "/feedback — залишити відгук\n"
        "/contact — контактна інформація\n"
        "/site — сайт Нової Пошти\n\n"
        "/find_by_index = Пошук відділенння за індексом чи адресою"
        "Або просто скористайтесь кнопками нижче.",
        reply_markup=main_kb
    )

# === Команда /commands ===
@bot.message_handler(commands=['commands'])
def commands(message):
    bot.send_message(
        message.chat.id,
        "📋 Доступні команди бота:\n"
        "/start — запуск бота\n"
        "/help — допомога\n"
        "/news — останні новини\n"
        "/track — відстежити посилку\n"
        "/feedback — залишити відгук\n"
        "/contact — контактна інформація\n"
        "/site — сайт Нової Пошти\n"
        "/find_by_index = Пошук відділенння за індексом чи адресою\n"
    )

# === Вітання ===
@bot.message_handler(func=lambda message: message.text == "Привіт! 👋")
def reply_hello(message):
    bot.send_message(
        message.chat.id,
        "Як я можу допомогти? Оберіть опцію нижче ⬇️",
        reply_markup=main_kb
    )

# === Знайти відділення ===
@bot.message_handler(func=lambda message: message.text == "Знайти відділення 🏤")
def ask_city(message):
    msg = bot.send_message(message.chat.id, "🏙 Введіть назву міста українською:")
    bot.register_next_step_handler(msg, find_branch)

def find_branch(message):
    city = message.text.strip().lower()
    if city in branches:
        reply = f"📍 Відділення у місті {city.capitalize()}:\n" + "\n".join(
            [f"{i+1}. {addr}" for i, addr in enumerate(branches[city])])
    else:
        reply = "🚫 На жаль, немає інформації про відділення в цьому місті. Спробуйте інше місто."
    bot.send_message(message.chat.id, reply)

# === Графік роботи ===
@bot.message_handler(func=lambda message: message.text == "Графік роботи 🕒")
def schedule(message):
    bot.send_message(
        message.chat.id,
        "🕒 Звичайний графік роботи:\nПн-Пт: 08:00 - 20:00\nСб: 09:00 - 18:00\nНд: 10:00 - 16:00"
    )

# === Розташування ===
@bot.message_handler(func=lambda message: message.text == "Розташування 📍")
def location(message):
    bot.send_message(
        message.chat.id,
        "📌 Приклад розташування відділення у Києві:"
    )
    bot.send_location(message.chat.id, latitude=50.4501, longitude=30.5234)
    bot.send_message(message.chat.id, "🔗 Додатково:", reply_markup=inline_kb)

# === Послуги ===
@bot.message_handler(func=lambda message: message.text == "Доступні послуги 📦")
def services(message):
    services_kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    services_kb.add(
        "📬 Відправлення та отримання", "💰 Післяплата",
        "🚚 Кур’єрська доставка", "📦 Зберігання посилок",
        "🔁 Переадресація", "⬅️ Назад"
    )
    bot.send_message(
        message.chat.id,
        "📦 Оберіть послугу для детальнішої інформації:",
        reply_markup=services_kb
    )

@bot.message_handler(func=lambda message: message.text in [
    "📬 Відправлення та отримання",
    "💰 Післяплата",
    "🚚 Кур’єрська доставка",
    "📦 Зберігання посилок",
    "🔁 Переадресація",
    "⬅️ Назад"
])
def service_detail(message):
    details = {
        "📬 Відправлення та отримання": "📬 Ви можете швидко надіслати або отримати посилку у будь-якому відділенні. Оформлення доступне і через мобільний додаток.",
        "💰 Післяплата": "💰 Отримувач може оплатити замовлення при видачі — готівкою або карткою.",
        "🚚 Кур’єрська доставка": "🚚 Замовте кур’єра для доставки/збору посилки з дому або офісу.",
        "📦 Зберігання посилок": "📦 Безкоштовне зберігання — 5 днів. Потім — за тарифами.",
        "🔁 Переадресація": "🔁 Змініть адресу доставки через додаток або за допомогою оператора.",
    }
    if message.text == "⬅️ Назад":
        bot.send_message(
            message.chat.id,
            "🔙 Повертаємось до головного меню:",
            reply_markup=main_kb
        )
    else:
        bot.send_message(message.chat.id, details[message.text])

# === Команда /news ===
@bot.message_handler(commands=['news'])
def news(message):
    bot.send_message(
        message.chat.id,
        "📰 Останні новини Нової Пошти:\n"
        "1. Нове відділення у Бучі!\n"
        "2. Кур’єри тепер працюють до 22:00.\n"
        "3. Знижки до -20% на доставку до кінця місяця."
    )

@bot.message_handler(commands=['find_by_index'])
def find_by_index(message):
    msg = bot.send_message(message.chat.id, "🔎 Введіть поштовий індекс або частину адреси:")
    bot.register_next_step_handler(msg, search_by_index)

def search_by_index(message):
    query = message.text.strip().lower()
    results = []
    for city, addresses in branches.items():
        for addr in addresses:
            if query in addr.lower():
                results.append(f"{city.capitalize()}: {addr}")
    if results:
        bot.send_message(message.chat.id, "📍 Знайдено:\n" + "\n".join(results))
    else:
        bot.send_message(message.chat.id, "🚫 Нічого не знайдено за запитом.")

# === Команда /track ===
@bot.message_handler(commands=['track'])
def track(message):
    msg = bot.send_message(message.chat.id, "📦 Введіть номер ТТН для відстеження:")
    bot.register_next_step_handler(msg, process_tracking)

def process_tracking(message):
    ttn = message.text.strip()
    bot.send_message(
        message.chat.id,
        f"🔍 Статус посилки {ttn}:\n✅ Посилка прямує до відділення у вашому місті."
    )

# === Команда /feedback ===
@bot.message_handler(commands=['feedback'])
def feedback(message):
    msg = bot.send_message(message.chat.id, "✍️ Напишіть ваш відгук або побажання:")
    bot.register_next_step_handler(msg, save_feedback)

def save_feedback(message):
    feedback_text = message.text.strip()
    bot.send_message(message.chat.id, "✅ Дякуємо за ваш відгук!")

def validate_date(date_str):
    try:
        datetime.strptime(date_str, "%d.%m.%Y")
        return True
    except ValueError:
        return False

def validate_time(time_str):
    try:
        datetime.strptime(time_str, "%H:%M")
        return True
    except ValueError:
        return False

# === Команда /contact ===
@bot.message_handler(commands=['contact'])
def contact(message):
    bot.send_message(
        message.chat.id,
        "📞 Служба підтримки:\n"
        "Телефон: 0 800 500 609\n"
        "Email: info@novaposhta.ua"
    )

# === Команда /site ===
@bot.message_handler(commands=['site'])
def site(message):
    bot.send_message(
        message.chat.id,
        "🌐 Вебсайт Нової Пошти:",
        reply_markup=inline_kb
    )

# === Запуск бота ===
bot.polling()
