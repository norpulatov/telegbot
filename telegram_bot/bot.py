import logging
from aiogram import Bot, Dispatcher, executor, types
from database import Database
import keyboards as kb
import config
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot)
db = Database()

# Start komandasi
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_id = message.from_user.id
    if not db.user_exists(user_id):
        db.add_user(user_id)
        await message.answer("👋 Salom! Sizga 1 kunlik tekin foydalanish berildi.")
    expire_date = db.get_sub_expire(user_id)
    if expire_date and expire_date > datetime.now():
        await message.answer("🔓 Sizning obunangiz faol. Funksiyalardan foydalanishingiz mumkin.", reply_markup=kb.main_menu)
    else:
        await message.answer("⏳ Sizning obunangiz tugagan. Davom etish uchun obuna bo‘ling.", reply_markup=kb.sub_menu)

# Obuna tugmalari
@dp.callback_query_handler(lambda c: c.data in ["sub_1m", "sub_3m"])
async def buy_subscription(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    if callback_query.data == "sub_1m":
        price = 15000
        period = 30
    else:
        price = 40000
        period = 90
    db.set_invoice(user_id, price, period)
    await bot.send_message(user_id, f"💳 To‘lov qilish uchun quyidagi havoladan foydalaning:
{config.CLICK_LINK}",
                           reply_markup=kb.pay_confirm)

# To‘lov tasdiqlash tugmasi
@dp.callback_query_handler(lambda c: c.data == "confirm_pay")
async def confirm_pay(callback_query: types.CallbackQuery):
    await bot.send_message(config.ADMIN_ID, f"👤 {callback_query.from_user.full_name} ({callback_query.from_user.id}) to‘lovni amalga oshirdi. Tasdiqlaysizmi?",
                           reply_markup=kb.admin_confirm(callback_query.from_user.id))
    await bot.send_message(callback_query.from_user.id, "✅ To‘lov ma’lumoti adminga yuborildi.")

# Admin tasdiqlashi
@dp.callback_query_handler(lambda c: c.data.startswith("admin_yes"))
async def admin_confirm(callback_query: types.CallbackQuery):
    user_id = int(callback_query.data.split("_")[2])
    price, period = db.get_invoice(user_id)
    db.activate_sub(user_id, period)
    await bot.send_message(user_id, "🎉 Obunangiz muvaffaqiyatli faollashtirildi!", reply_markup=kb.main_menu)
    await callback_query.answer("✅ Tasdiqlandi")

@dp.callback_query_handler(lambda c: c.data.startswith("admin_no"))
async def admin_decline(callback_query: types.CallbackQuery):
    user_id = int(callback_query.data.split("_")[2])
    await bot.send_message(user_id, "❌ To‘lovingiz rad etildi. Iltimos qaytadan urinib ko‘ring.")
    await callback_query.answer("❌ Rad etildi")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
