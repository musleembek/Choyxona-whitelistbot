import os
import telebot
from telebot import types

# Token va Admin ID
BOT_TOKEN = os.getenv("BOT_TOKEN", "8138358819:AAGpKlT7btsq8pve7xKdNqeWqTy13GlU_M4")
ADMIN_ID = os.getenv("ADMIN_ID", "1860260857")

bot = telebot.TeleBot(BOT_TOKEN)

# Vaqtinchalik ma'lumotlarni saqlash uchun
user_data = {}

RULES_TEXT = """📜 **Minecraft Server Qoidalari:**

1. Har qanday, kichikmi u yoki katta qoidabuzarlikni jazosi - BAN (butun umrlik)
2. Har qanday so'kish va haqarotli so'zlar minecraft va discord serverlarda taqiqlanadi.
3. Serverdagi o'yinchilarga bo'lgan har qanday haqarotomus murojat, xurmatsiz so'zlar va laqablar taqiqlanadi. [Istisno: Har ikki o'yinchi roziligi bilan].
4. Serverdagi sehrli kitob, instrument va kamyob buyumlarni haqiqiy pulga sotish taqiqlanadi.
5. O'yindan tashqaridagi konfliktlarni o'yinga kiritish taqiqlanadi.
6. O'yinchilar gohi-gohi bilan discord serverga kirib tanishib chiqishi kerak, yangiliklardan boxabar bo'lish uchun. [Majburiy emas]
7. Agar biror qoida shu qatorda eslab o'tilmagan bo'lsa, ammo u o'yindan olinadigan tajribani buzsa yoki noqulaylik uchun xizmat qiluvchi hatti-xarakat bo'lsa, ma'muriyat bu ishni ko'rib chiqadi.
8. Server adminstratori xohlagan payt o'yinchini tekshiruv uchun discordga/telegram suhbatga chaqirishi mumkin. [Norkulov_play, D0odlebug_]
9. Har qanday turdagi cheating software'lar, xRAY va shunga o'xshash o'yinni buzadigan dasturlar ishlatish taqiqlanadi.
10. Discord /telegram serverda so'kinish taqiqlanadi.
11. Telegram va Discord chatlarida flood qilish (bitta yoki bir mazmunga ega so'zlarni ko'p marta jo'natish).
12. Qoidalar har doim ham aniq yozilgandek ishlamasligi mumkin, u moral nuqtai nazarlardan kelib chiqib ham ko'rib chiqiladi.
13. Server Adminlari va Egasi chatda o'yinchilar tomonidan yozilgan so'zlarga javob berishga majbur emas. Har qanday siyosiy va qonuniy muammo o'zingizniki!
14. Qoidalar har doim o'zgarib turishi mumkin va bu haqida faqatgina https://t.me/choyxona_world telegram guruhida bilib olasiz.
15. Qoidalarni bilmaslik sizni javobgarlikdan qutqarmaydi.
16. Har qanday millat, irq va din prinsplari yoki belgilari orasidagi farqni tilga olish, u bo'yicha bir inson qadriga putr yetkazish va obrosizlantirish taqiqlanadi.
17. Ban olgan o'yinchi qurgan har bir narsa ortga qaytariladi yoki o'chirib tashlanadi [istisno: admin ko'rib chiqadi].
18. PVP unda qatanshuvchilarni har biri roziligida o'tkazilishi lozim. [PVP qilish uchun chatda opponentdan ruxsat so'rang].

💡 Yangi g'oyalar va muammolarga yechimlarni @musleembek ga telegramdan yozing!"""

@bot.message_handler(commands=['start'])
def start_cmd(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn = types.KeyboardButton("✅ Qoidalarga rozilik bildiraman")
    markup.add(btn)
    bot.send_message(message.chat.id, RULES_TEXT, reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "✅ Qoidalarga rozilik bildiraman")
def agree_rules(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn = types.KeyboardButton("📱 Telefon raqamni yuborish", request_contact=True)
    markup.add(btn)
    bot.send_message(
        message.chat.id, 
        "Ro'yxatdan o'tishni davom ettirish uchun telefon raqamingizni tasdiqlang.\n"
        "Pastdagi '📱 Telefon raqamni yuborish' tugmasini bosing:", 
        reply_markup=markup
    )

@bot.message_handler(content_types=['contact'])
def get_contact(message):
    user_data[message.from_user.id] = {'phone': message.contact.phone_number}
    msg = bot.send_message(
        message.chat.id, 
        "Telefon raqamingiz tasdiqlandi! ✅\n\nEndi Minecraft'dagi taxallusingizni (Nickname) yozib yuboring:",
        reply_markup=types.ReplyKeyboardRemove()
    )
    bot.register_next_step_handler(msg, get_nickname)

def get_nickname(message):
    chat_id = message.chat.id
    nickname = message.text.strip()
    phone = user_data.get(chat_id, {}).get('phone', 'Noma\'lum')
    username = f"@{message.from_user.username}" if message.from_user.username else "Mavjud emas"

    admin_text = (
        "📥 **Yangi o'yinchi ro'yxatdan o'tdi!**\n\n"
        f"👤 **User:** {message.from_user.full_name} ({username})\n"
        f"🆔 **ID:** `{message.from_user.id}`\n"
        f"📞 **Tel:** `{phone}`\n"
        f"🎮 **Minecraft Nickname:** `{nickname}`"
    )

    if ADMIN_ID:
        try:
            bot.send_message(ADMIN_ID, admin_text, parse_mode="Markdown")
        except Exception as e:
            print(f"Adminga yuborishda xato: {e}")

    bot.send_message(
        chat_id, 
        "🎉 **Tabriklaymiz!** Siz ro'yxatdan muvaffaqiyatli o'tdingiz.\n"
        "Sizning so'rovingiz adminlarga yuborildi. Tezada sizni Whitelist'ga qo'shishadi!"
    )

if __name__ == "__main__":
    print("Bot ishga tushdi...")
    bot.infinity_polling()
