import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

API_TOKEN = '8537969027:AAHn-0DbGMgkf2g0PdeDZZtmf6uq7-3d0dM'
ADMIN_ID = 5714788187

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# --- KANALLAR VA TUGMALAR ---
CHANNELS = [
    {"name": "MERCYRE 2025", "url": "https://t.me/MERCYRE2025", "id": "@MERCYRE2025"},
    {"name": "GAMING PRO 2025", "url": "https://t.me/GAMINGPRO2025", "id": "@GAMINGPRO2025"},
    {"name": "LOGO MARKET", "url": "https://t.me/LOGOMARKET90", "id": "@LOGOMARKET90"},
]
SOCIAL_LINKS = [
    {"name": "Cyber Games IG", "url": "https://www.instagram.com/cybergames2024/"},
    {"name": "XON BRAND IG", "url": "https://www.instagram.com/xonbrand/"},
    {"name": "XON BRAND YT", "url": "https://www.youtube.com/@XONBRAND"},
    {"name": "Cyber Games YT", "url": "https://www.youtube.com/@CYBERGAMES2024"},
]


def get_sub_keyboard():
    buttons = [[InlineKeyboardButton(text=f"➕ {ch['name']}", url=ch['url'])] for ch in CHANNELS]
    for link in SOCIAL_LINKS:
        buttons.append([InlineKeyboardButton(text=f"🔗 {link['name']}", url=link['url'])])
    buttons.append([InlineKeyboardButton(text="✅ Obunani tekshirish", callback_data="check_subs")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def check_user_subs(user_id):
    for ch in CHANNELS:
        try:
            member = await bot.get_chat_member(chat_id=ch['id'], user_id=user_id)
            if member.status in ["left", "kicked"]: return False
        except:
            return False
    return True


@dp.message(CommandStart())
async def start_command(message: types.Message):
    if await check_user_subs(message.from_user.id):
        await message.answer("✅ Xush kelibsiz! Savol va fayllaringizni yuboring.")
    else:
        await message.answer("⚠️ Botdan foydalanish uchun obuna bo'ling:", reply_markup=get_sub_keyboard())


# --- ADMIN JAVOBINI FOYDALANUVCHIGA YUBORISH ---
@dp.message(F.reply_to_message & (F.from_user.id == ADMIN_ID))
async def reply_to_user(message: types.Message):
    try:
        # Reply qilingan xabar matnidan ID raqamini ajratib olamiz
        reply_text = message.reply_to_message.text or message.reply_to_message.caption
        user_id = int(reply_text.split("ID: ")[1].split("\n")[0])

        await bot.copy_message(chat_id=user_id, from_chat_id=ADMIN_ID, message_id=message.message_id)
        await message.answer("✅ Javobingiz yuborildi.")
    except Exception as e:
        await message.answer(f"❌ Xatolik: Javob yuborib bo'lmadi. ID topilmadi.")


# --- FOYDALANUVCHI XABARINI ADMINGA YUBORISH ---
@dp.message()
async def handle_all_messages(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        # Foydalanuvchiga tasdiq
        await message.answer("Qabul qilindi! Adminga yetkazildi.")

        # Adminga xabarni ma'lumotlari bilan yuborish
        info = f"📩 Yangi xabar!\n👤 Kimdan: {message.from_user.full_name}\n🆔 ID: {message.from_user.id}\n\n"

        if message.text:
            await bot.send_message(ADMIN_ID, info + f"📝 Matn: {message.text}")
        else:
            # Agar fayl (rasm, video va h.k.) bo'lsa
            await bot.send_message(ADMIN_ID, info + "📎 Fayl quyida:")
            await message.copy_to(chat_id=ADMIN_ID)
    else:
        if not message.reply_to_message:
            await message.answer("Xabarga javob yozish uchun 'Reply' qiling.")


@dp.callback_query(lambda c: c.data == "check_subs")
async def check_callback(callback: CallbackQuery):
    if await check_user_subs(callback.from_user.id):
        await callback.message.delete()
        await callback.message.answer("🎉 Obuna tasdiqlandi!")
    else:
        await callback.answer("❌ Obuna bo'lmagansiz!", show_alert=True)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    InlineKeyboardButton(text="➡️ Kirish", url=ch['url'])


if __name__ == '__main__':
    asyncio.run(main())