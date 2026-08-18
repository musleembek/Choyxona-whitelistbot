import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

BOT_TOKEN = os.getenv("BOT_TOKEN", "8138358819:AAGpKlT7btsq8pve7xKdNqeWqTy13GlU_M4")
ADMIN_ID = os.getenv("ADMIN_ID", "1860260857")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

class Registration(StatesGroup):
    rules_agree = State()
    phone = State()
    nickname = State()

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

@dp.message(CommandStart())
async def start_cmd(message: types.Message, state: FSMContext):
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="✅ Qoidalarga rozilik bildiraman")]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer(RULES_TEXT, reply_markup=kb, parse_mode="Markdown")
    await state.set_state(Registration.rules_agree)

@dp.message(Registration.rules_agree, F.text == "✅ Qoidalarga rozilik bildiraman")
async def process_rules(message: types.Message, state: FSMContext):
    phone_kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📱 Telefon raqamni yuborish", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer(
        "Ro'yxatdan o'tishni davom ettirish uchun telefon raqamingizni tasdiqlang.\n"
        "Pastdagi '📱 Telefon raqamni yuborish' tugmasini bosing:",
        reply_markup=phone_kb
    )
    await state.set_state(Registration.phone)

@dp.message(Registration.phone, F.contact)
async def process_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.contact.phone_number)
    await message.answer(
        "Telefon raqamingiz tasdiqlandi! ✅\n\nEndi Minecraft'dagi taxallusingizni (Nickname) yozib yuboring:",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(Registration.nickname)

@dp.message(Registration.phone)
async def invalid_phone(message: types.Message):
    await message.answer("❌ Ro'yxatdan o'tish uchun telefon raqamingizni pastdagi tugma orqali tasdiqlashingiz shart!")

@dp.message(Registration.nickname)
async def process_nickname(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    nickname = message.text.strip()
    phone = user_data.get("phone")
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
            await bot.send_message(chat_id=int(ADMIN_ID), text=admin_text, parse_mode="Markdown")
        except Exception as e:
            print(f"Adminga xabar yuborishda xato: {e}")

    await message.answer(
        "🎉 **Tabriklaymiz!** Siz ro'yxatdan muvaffaqiyatli o'tdingiz.\n"
        "Sizning so'rovingiz adminlarga yuborildi. Tezada sizni Whitelist'ga qo'shishadi!"
    )
    await state.clear()

async def main():
    print("Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
