from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main_menu = InlineKeyboardMarkup(row_width=2)
main_menu.add(InlineKeyboardButton("➕ Kirim", callback_data="kirim"),
              InlineKeyboardButton("➖ Chiqim", callback_data="chiqim"))
main_menu.add(InlineKeyboardButton("📊 Statistika", callback_data="stat"))

sub_menu = InlineKeyboardMarkup(row_width=2)
sub_menu.add(InlineKeyboardButton("1 oy - 15,000 so‘m", callback_data="sub_1m"))
sub_menu.add(InlineKeyboardButton("3 oy - 40,000 so‘m", callback_data="sub_3m"))

pay_confirm = InlineKeyboardMarkup()
pay_confirm.add(InlineKeyboardButton("✅ To‘lov qildim", callback_data="confirm_pay"))

def admin_confirm(user_id):
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("✅ Ha", callback_data=f"admin_yes_{user_id}"))
    kb.add(InlineKeyboardButton("❌ Yo‘q", callback_data=f"admin_no_{user_id}"))
    return kb
