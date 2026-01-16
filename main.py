import telebot
from telebot import types

# ================== SOZLAMALAR ==================
TOKEN = "7971999489:AAG7GFdexQAUeyb13sTRLVczL-dH4f8aHRI"
ADMIN_ID = 5938434244

bot = telebot.TeleBot(TOKEN)

# ================== MAHSULOTLAR KATALOGI ==================
CATALOG = {
    "🔩 Sharnerlar": [
        {
            "id": "sharner_autsite",
            "name": "Sharner Autsite",
            "price": 7000,
            "photo": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTtSm6VPb1AtXVFEv7ttL9kffuxe0QkuK3D3FaBkfHDYg&s=10"
        },
        {
            "id": "Autsite Garbat",
            "name": "Autsite Garbat",
            "price": 7000,
            "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Hinge.jpg/640px-Hinge.jpg"
        }
    ],
    "🧲 Magnitlar": [
        {
            "id": "magnit_kichik",
            "name": "Magnit kichik",
            "price": 2000,
            "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7c/Magnet.jpg/640px-Magnet.jpg"
        }
    ]
}

# ================== FOYDALANUVCHI HOLATI ==================
user_state = {}     # chat_id -> state
orders = {}         # chat_id -> product

# ================== START ==================
@bot.message_handler(commands=["start"])
def start(message):
    kb = types.InlineKeyboardMarkup()
    for category in CATALOG:
        kb.add(types.InlineKeyboardButton(
            text=category,
            callback_data=f"cat|{category}"
        ))
    bot.send_message(
        message.chat.id,
        "Assalomu alaykum 👋\nKategoriya tanlang:",
        reply_markup=kb
    )

# ================== KATEGORIYA TANLANDI ==================
@bot.callback_query_handler(func=lambda call: call.data.startswith("cat|"))
def show_products(call):
    category = call.data.split("|")[1]
    kb = types.InlineKeyboardMarkup()

    for p in CATALOG[category]:
        kb.add(types.InlineKeyboardButton(
            text=f"{p['name']} – {p['price']} so'm",
            callback_data=f"prod|{p['id']}"
        ))

    bot.send_message(
        call.message.chat.id,
        "Mahsulotni tanlang:",
        reply_markup=kb
    )

# ================== MAHSULOT TANLANDI ==================
@bot.callback_query_handler(func=lambda call: call.data.startswith("prod|"))
def show_product(call):
    pid = call.data.split("|")[1]
    chat_id = call.message.chat.id

    for products in CATALOG.values():
        for p in products:
            if p["id"] == pid:
                orders[chat_id] = p

                bot.send_photo(
                    chat_id,
                    p["photo"],
                    caption=f"📦 <b>{p['name']}</b>\n💰 Narxi: <b>{p['price']} so'm</b>",
                    parse_mode="HTML"
                )

                kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                kb.add(types.KeyboardButton(
                    "📞 Telefon raqamni yuborish",
                    request_contact=True
                ))

                user_state[chat_id] = "contact"
                bot.send_message(
                    chat_id,
                    "Buyurtmani davom ettirish uchun telefon raqamingizni yuboring:",
                    reply_markup=kb
                )
                return

# ================== CONTACT QABUL QILISH ==================
@bot.message_handler(content_types=["contact"])
def get_contact(message):
    chat_id = message.chat.id

    if user_state.get(chat_id) != "contact":
        return

    product = orders.get(chat_id)

    admin_text = (
        "🆕 <b>YANGI BUYURTMA</b>\n\n"
        f"👤 Ism: {message.contact.first_name}\n"
        f"📞 Tel: {message.contact.phone_number}\n\n"
        f"📦 Mahsulot: {product['name']}\n"
        f"💰 Narxi: {product['price']} so'm"
    )

    bot.send_message(
        ADMIN_ID,
        admin_text,
        parse_mode="HTML"
    )

    bot.send_message(
        chat_id,
        "✅ Buyurtmangiz qabul qilindi!\nTez orada siz bilan bog‘lanamiz.",
        reply_markup=types.ReplyKeyboardRemove()
    )

    user_state.pop(chat_id, None)
    orders.pop(chat_id, None)

# ================== RUN ==================
print("Bot ishga tushdi...")
bot.infinity_polling()