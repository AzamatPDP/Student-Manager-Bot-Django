import asyncio
import requests
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

# Sozlamalar
API_TOKEN = '8175475429:AAHFY5pcpX8v3SLFZReEve46OSbl4SmjNLk'
BASE_URL = 'http://127.0.0.1:8000/api/'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


class StudentForm(StatesGroup):
    first_name = State()
    last_name = State()
    group = State()
    phone = State()


# --- ASOSIY MENYU (DEFAULT BUTTONS) ---
def main_menu():
    builder = ReplyKeyboardBuilder()
    builder.button(text="📋 Talabalar ro'yxati")
    builder.button(text="➕ Yangi talaba")
    builder.button(text="🗑 Talabani o'chirish")
    builder.adjust(2)  # Tugmalarni 2 qatorga bo'ladi
    return builder.as_markup(resize_keyboard=True)


@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer(
        "🎓 **Student Manager** tizimiga xush kelibsiz!\nPastdagi menyudan foydalaning:",
        reply_markup=main_menu()
    )


# --- 1. RO'YXATNI KO'RISH (TEXT OR BUTTON) ---
@dp.message(F.text == "📋 Talabalar ro'yxati")
@dp.message(Command("students"))
async def get_students(message: types.Message):
    try:
        response = requests.get(f"{BASE_URL}students/")
        if response.status_code == 200:
            students = response.json()
            if not students:
                await message.answer("📭 Hozircha bazada talabalar mavjud emas.")
                return

            text = "🎓 **Talabalar ro'yxati:**\n" + "—" * 15 + "\n"
            for s in students:
                text += f"👤 {s.get('first_name')} {s.get('last_name')}\n📞 {s.get('phone')}\n" + "—" * 15 + "\n"
            await message.answer(text)
    except Exception as e:
        await message.answer(f"❌ Xatolik: {e}")


# --- 2. YANGI TALABA (TEXT OR BUTTON) ---
@dp.message(F.text == "➕ Yangi talaba")
@dp.message(Command("new"))
async def start_form(message: types.Message, state: FSMContext):
    await message.answer("Talabaning ismini kiriting:", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(StudentForm.first_name)


@dp.message(StudentForm.first_name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(first_name=message.text)
    await message.answer("Familiyasini kiriting:")
    await state.set_state(StudentForm.last_name)


@dp.message(StudentForm.last_name)
async def process_lastname(message: types.Message, state: FSMContext):
    await state.update_data(last_name=message.text)

    # Inline guruhlar
    try:
        response = requests.get(f"{BASE_URL}groups/")
        groups = response.json()
        builder = InlineKeyboardBuilder()
        for g in groups:
            builder.row(types.InlineKeyboardButton(text=f"📁 {g['name']}", callback_data=f"group_{g['id']}"))

        await message.answer("Guruhni tanlang:", reply_markup=builder.as_markup())
        await state.set_state(StudentForm.group)
    except:
        await message.answer("❌ Xatolik yuz berdi.", reply_markup=main_menu())


@dp.callback_query(F.data.startswith("group_"), StudentForm.group)
async def select_group(callback: types.CallbackQuery, state: FSMContext):
    group_id = callback.data.split("_")[1]
    await state.update_data(group=int(group_id))
    await callback.message.edit_text("✅ Guruh tanlandi. Endi telefon raqamini kiriting:")
    await state.set_state(StudentForm.phone)


@dp.message(StudentForm.phone)
async def process_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text)
    user_data = await state.get_data()
    response = requests.post(f"{BASE_URL}students/", data=user_data)

    if response.status_code == 201:
        await message.answer("🎉 Saqlandi!", reply_markup=main_menu())
    else:
        await message.answer("❌ Xato!", reply_markup=main_menu())
    await state.clear()


# --- 3. O'CHIRISH (TEXT OR BUTTON) ---
@dp.message(F.text == "🗑 Talabani o'chirish")
@dp.message(Command("delete"))
async def list_students_for_delete(message: types.Message):
    try:
        response = requests.get(f"{BASE_URL}students/")
        students = response.json()
        if not students:
            await message.answer("❌ O'chirishga talaba yo'q.")
            return

        builder = InlineKeyboardBuilder()
        for s in students:
            builder.row(types.InlineKeyboardButton(text=f"🗑 {s['first_name']} {s['last_name']}", callback_data=f"del_{s['id']}"))

        await message.answer("Kimni o'chiramiz?", reply_markup=builder.as_markup())
    except:
        await message.answer("❌ Xatolik.")


@dp.callback_query(F.data.startswith("del_"))
async def delete_callback(callback: types.CallbackQuery):
    student_id = callback.data.split("_")[1]
    requests.delete(f"{BASE_URL}students/{student_id}/")
    await callback.message.edit_text("✅ O'chirildi!")
    await callback.answer()


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())