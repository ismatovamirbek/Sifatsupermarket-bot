from loader import dp, bot  # dispetcher va bot obyektlari import qilingan
from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup

# Vakansiya bo‘yicha foydalanuvchi to‘ldiradigan anketaning bosqichlari
class Vacancy(StatesGroup):       # Bo‘sh ish o‘rni
    fullname = State()      # To‘liq ism
    phone = State()         # Telefon raqam
    age = State()            # Yosh
    sex = State()           # Jinsi
    location = State()      # Yashash joyi
    birthday = State()      # Tug‘ilgan sana
    family = State()        # Oilaviy holati va farzandlari borligi
    education = State()     # Ma'lumoti
    convicted = State()     # Sudlanganlik holati
    rus_lang = State()      # Rus tilini bilish darajasi
    picture = State()       # Rasm
    previous_job = State()  # Avvalgi ish joyi
    job = State()           # Tanlangan ish o‘rni
    job_duration = State()  # Tanlangan ish o‘rnida ishlash davomiyligi
    military_certificate = State()  # Harbiy guvohnoma
    confirmation = State()  # Adminga yuborishga rozilik
    waiting_for_military = State()