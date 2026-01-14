import telebot
from telebot import types

TOKEN = "BOTFATHER_TOKENING"
ADMIN_ID = 5938434244

bot = telebot.TeleBot(TOKEN)

# ===== MAHSULOT =====
PRODUCT = {
    "name": "Sharner Autsite",
    "price": "7 000 so‘m",
    "photo": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTtSm6VPb1AtXVFEv7ttL9kffuxe0QkuK3D3FaBkfHDYg&s=10"
}

# ===== START =====
@bot.message_handler(commands=['start'])
def start(message):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("🛒 Buyurtma berish", callback_data="order"))

    bot.send_photo(
        message.chat.id,
        PRODUCT["photo"],
        caption=(
            f"📦 <b>{PRODUCT['name']}</b>\n"
            f"💰 Narxi: <b>{PRODUCT['price']}</b>\n\n"
            "Buyurtma berish uchun tugmani bosing 👇"
        ),
        parse_mode="HTML",
        reply_markup=kb
    )

# ===== BUYURTMA BOSILDI =====
@bot.callback_query_handler(func=lambda call: call.data == "order")
def order(call):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.add(types.KeyboardButton("📞 Telefon raqamni yuborish", request_contact=True))

    bot.send_message(
        call.message.chat.id,
        "📞 Iltimos, telefon raqamingizni yuboring:",
        reply_markup=kb
    )

# ===== CONTACT QABUL QILISH =====
@bot.message_handler(content_types=['contact'])
def get_contact(message):
    name = message.from_user.first_name
    phone = message.contact.phone_number

    # foydalanuvchiga javob
    bot.send_message(
        message.chat.id,
        "✅ Buyurtma qabul qilindi!\nTez orada siz bilan bog‘lanamiz.",
        reply_markup=types.ReplyKeyboardRemove()
    )

    # adminga yuborish
    bot.send_message(
        ADMIN_ID,
        f"📥 <b>YANGI BUYURTMA</b>\n\n"
        f"👤 Ism: {name}\n"
        f"📞 Tel: {phone}\n"
        f"📦 Mahsulot: {PRODUCT['name']}\n"
        f"💰 Narx: {PRODUCT['price']}",
        parse_mode="HTML"
    )

bot.polling()
