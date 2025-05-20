from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# 🧑‍💼 Mavjud ish o‘rinlari
vacancy_options = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="💰 Kassir", callback_data="job_kassir"),
            InlineKeyboardButton(text="🛍 Sotuvchi", callback_data="job_sotuvchi"),
        ],
        [
            InlineKeyboardButton(text="🛡 Qo‘riqchi", callback_data="job_oxrana"),
        ]
    ]
)

# 👤 Jinsni tanlang
sex_options = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="👨 Erkak", callback_data="sex_male"),
            InlineKeyboardButton(text="👩 Ayol", callback_data="sex_female")
        ]
    ]
)

# 👪 Oilaviy holat
family_options = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="💍 Turmush qurgan", callback_data="family_married"),
            InlineKeyboardButton(text="🕊 Bo‘ydoq / Turmush qurmagan", callback_data="family_single")
        ]
    ]
)

# 🎓 Ta’lim darajasi
education_options = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🎓 Oliy", callback_data="edu_higher"),
            InlineKeyboardButton(text="🏫 O‘rta maxsus", callback_data="edu_secondary")
        ],
        [
            InlineKeyboardButton(text="📘 Umumiy o‘rta", callback_data="edu_general")
        ]
    ]
)

# ⚖️ Sudlanganlik
convicted_options = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Ha", callback_data="convicted_yes"),
            InlineKeyboardButton(text="❌ Yo‘q", callback_data="convicted_no")
        ]
    ]
)

# 🇷🇺 Rus tilini bilish darajasi
rus_lang_options = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🚫 Bilmayman", callback_data="rus_lang_no"),
            InlineKeyboardButton(text="🔤 Boshlang‘ich", callback_data="rus_lang_beginner")
        ],
        [
            InlineKeyboardButton(text="📗 O‘rtacha", callback_data="rus_lang_medium"),
            InlineKeyboardButton(text="📘 Yuqori", callback_data="rus_lang_high")
        ]
    ]
)

# ⏳ Ish davomiyligi
job_duration_options = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🕐 Vaqtinchalik", callback_data="duration_temp"),
            InlineKeyboardButton(text="📆 1-2 yil", callback_data="duration_1_2")
        ],
        [
            InlineKeyboardButton(text="📌 Vaziyatga qarab", callback_data="duration_situation"),
            InlineKeyboardButton(text="🏢 Doimiy", callback_data="duration_permanent")
        ]
    ]
)

# 🎖 Harbiy guvohnoma
military_certificate_options = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🎖 Mavjud", callback_data="military_yes"),
            InlineKeyboardButton(text="🚫 Yo‘q", callback_data="military_no")
        ]
    ]
)

# ✅ Tasdiqlash yoki ❌ Bekor qilish
confirmation_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Tasdiqlayman", callback_data="confirm_yes"),
            InlineKeyboardButton(text="❌ Bekor qilish", callback_data="cancel")
        ]
    ]
)
