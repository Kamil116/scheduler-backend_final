from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from helpers import make_row_keyboard

router = Router()

available_courses = ['BS22-CS-01', 'BS22-CS-02', 'BS22-CS-03',
                     'BS22-CS-04', 'BS22-CS-05', 'BS22-CS-06',
                     'BS22-DS-01', 'BS22-DS-02', 'BS22-DS-03',
                     'BS22-DS-04']
available_lectures = ['Sport', 'Math', 'English', 'Programming', 'History']
start_menu = ['Select course', 'Select lectures', 'Manage notifications']


class SettingsStates(StatesGroup):
    select_course = State()
    select_lectures = State()
    manage_notifications = State()
    start = State()


@router.message(Command("start"))
async def start(message: Message, state: FSMContext):
    await state.set_state(SettingsStates.start)
    await message.answer("Select action:", reply_markup=make_row_keyboard(start_menu))


@router.message(SettingsStates.start, F.text.in_(start_menu))
async def start_handler(message: Message, state: FSMContext):
    if message.text == "Select course":
        await select_course(message, state)
    elif message.text == "Select lectures":
        await select_lectures(message, state)
    elif message.text == "Manage notifications":
        await manage_notifications(message, state)
    else:
        await message.answer("Invalid action", reply_markup=make_row_keyboard(start_menu))


@router.message(Command("select_course"))
async def select_course(message: Message, state: FSMContext):
    await message.answer("Select course", reply_markup=make_row_keyboard(available_courses))
    await state.set_state(SettingsStates.select_course)


@router.message(SettingsStates.select_course, F.text.in_(available_courses))
async def select_course_handler(message: Message, state: FSMContext):
    # Logic for selecting course
    await message.answer("Course selected", reply_markup=ReplyKeyboardRemove())
    await start(message, state)


@router.message(SettingsStates.select_course)
async def select_course_handler(message: Message, state: FSMContext):
    await message.answer("Invalid course", reply_markup=make_row_keyboard(available_courses))
    await start(message, state)


@router.message(Command("select_lectures"))
async def select_lectures(message: Message, state: FSMContext):
    await message.answer("Select lectures", reply_markup=make_row_keyboard(available_lectures))
    await state.set_state(SettingsStates.select_lectures)


@router.message(SettingsStates.select_lectures, F.text.in_(available_lectures))
async def select_lectures_handler(message: Message, state: FSMContext):
    # Logic for selecting lectures
    await message.answer("Lectures selected", reply_markup=ReplyKeyboardRemove())
    await start(message, state)


@router.message(SettingsStates.select_lectures)
async def select_lectures_handler(message: Message):
    await message.answer("Invalid lectures", reply_markup=make_row_keyboard(available_lectures))


@router.message(Command("manage_notifications"))
async def manage_notifications(message: Message, state: FSMContext):
    await message.answer("Manage notifications", reply_markup=make_row_keyboard(["Enable", "Disable"]))
    await state.set_state(SettingsStates.manage_notifications)


@router.message(SettingsStates.manage_notifications, F.text.in_(["Enable", "Disable"]))
async def manage_notifications_handler(message: Message, state: FSMContext):
    # Logic for managing notifications
    await message.answer("Notifications managed", reply_markup=ReplyKeyboardRemove())
    await start(message, state)


@router.message(SettingsStates.manage_notifications)
async def manage_notifications_handler(message: Message):
    await message.answer("Invalid action", reply_markup=make_row_keyboard(["Enable", "Disable"]))
    await start(message, state)


if __name__ == "__main__":
    asyncio.run(dp.start_polling())
