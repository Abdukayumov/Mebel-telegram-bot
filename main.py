import telebot
from telebot import types

# ================= SOZLAMALAR =================
TOKEN = "7971999489:AAG7GFdexQAUeyb13sTRLVczL-dH4f8aHRI"
ADMIN_ID = 5938434244

bot = telebot.TeleBot(TOKEN)

# ================= KATALOG =================
PRODUCT = {
    "id": "sharner_autsite",
    "name": "Sharner Autsite",
    "price": 7000,
    "photo": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTtSm6VPb1AtXVFEv7ttL9kffuxe0QkuK3D3FaBkfHDYg&s=10"
}

user_state = {}  # chat_id -> step
orders = {}

# ================= START =================
@bot.message_handler(commands=["start"])
def start(message):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(
        text="🛒 Buyurtma berish",
        callback_data="order"
    ))
    bot.send_message(
        message.chat.id,
        "Assalomu alaykum!\nMahsulot buyurtma berish uchun tugmani bosing 👇",
        reply_markup=kb
    )

# ================= BUYURTMA BOSHLASH =================
@bot.callback_query_handler(func=lambda call: call.data == "order")
def order(call):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(
        text=f"{PRODUCT['name']} — {PRODUCT['price']} so'm",
        callback_data="product"
    ))
    bot.send_message(
        call.message.chat.id,
        "Mahsulotni tanlang:",
        reply_markup=kb
    )

# ================= MAHSULOT =================
@bot.callback_query_handler(func=lambda call: call.data == "product")
def product(call):
    bot.send_photo(
        call.message.chat.id,
        PRODUCT["photo"],
        caption=f"📦 {PRODUCT['name']}\n💰 Narxi: {PRODUCT['price']} so'm"
    )

    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.add(types.KeyboardButton("📞 Telefon raqamni yuborish", request_contact=True))

    user_state[call.message.chat.id] = "contact"
    bot.send_message(
        call.message.chat.id,
        "Buyurtmani davom ettirish uchun telefon raqamingizni yuboring:",
        reply_markup=kb
    )

# ================= CONTACT =================
@bot.message_handler(content_types=["contact"])
def contact(message):
    if user_state.get(message.chat.id) != "contact":
        return

    orders[message.chat.id] = {
        "phone": message.contact.phone_number,
        "name": message.contact.first_name
    }

    kb = types.ReplyKeyboardRemove()
    user_state[message.chat.id] = "name"

    bot.send_message(
        message.chat.id,
        "Ismingizni kiriting:",
        reply_markup=kb
    )

# ================= ISM =================
@bot.message_handler(func=lambda message: user_state.get(message.chat.id) == "name")
def get_name(message):
    orders[message.chat.id]["client_name"] = message.text

    text = (
        "🆕 Yangi buyurtma!\n\n"
        f"👤 Ism: {orders[message.chat.id]['client_name']}\n"
        f"📞 Tel: {orders[message.chat.id]['phone']}\n"
        f"📦 Mahsulot: {PRODUCT['name']}\n"
        f"💰 Narxi: {PRODUCT['price']} so'm"
    )

    bot.send_message(ADMIN_ID, text)
    bot.send_message(message.chat.id, "✅ Buyurtmangiz qabul qilindi. Rahmat!")

    user_state.pop(message.chat.id, None)
    orders.pop(message.chat.id, None)

# ================= RUN =================
print("Bot ishga tushdi...")
bot.infinity_polling()