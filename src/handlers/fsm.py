from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from helpers import make_row_keyboard

router = Router()

available_courses = ['BS22-CS-01', 'BS22-CS-02', 'BS22-CS-03']
available_courses_marked = []
for course in available_courses:
    available_courses_marked.append(course + " ✅")

available_lectures = ['Sport', 'Math', 'English', 'Programming', 'History']
available_lectures_marked = []
for lecture in available_lectures:
    available_lectures_marked.append(lecture + " ✅")
start_menu = ['Select course', 'Select lectures', 'Manage notifications']

users_settings = {}  # {user id: UserSettings}


class UserSettings:
    # three arrays: courses, lectures, notifications
    def __init__(self):
        self.course = None
        self.lectures = []
        self.notifications = None

    def select_course(self, course):
        self.course = course

    def add_lecture(self, lecture):
        self.lectures.append(lecture)

    def remove_course(self, course):
        self.course = None

    def remove_lecture(self, lecture):
        self.lectures.remove(lecture)

    def get_course(self):
        return self.course

    def get_lectures(self):
        return self.lectures


def get_marked_courses(message: Message):
    # add mark to selected courses
    local_courses = available_courses.copy()

    if users_settings[message.from_user.id].get_course() is not None:
        local_courses[local_courses.index(
            users_settings[message.from_user.id].get_course())] += " ✅"

    return local_courses


def get_marked_lectures(message: Message):
    # add mark to selected lectures
    local_lectures = available_lectures.copy()

    for lecture in users_settings[message.from_user.id].get_lectures():
        local_lectures[local_lectures.index(lecture)] += " ✅"

    return local_lectures


class SettingsStates(StatesGroup):
    select_course = State()
    select_lectures = State()
    manage_notifications = State()
    start = State()


@router.message(Command("start"))
async def start(message: Message, state: FSMContext):
    # DB
    if message.from_user.id not in users_settings:
        users_settings[message.from_user.id] = UserSettings()

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


# ------------------- Select course -------------------

@router.message(Command("select_course"))
async def select_course(message: Message, state: FSMContext):
    available_courses_marked = get_marked_courses(message)
    await message.answer("Select course", reply_markup=make_row_keyboard(available_courses_marked))
    await state.set_state(SettingsStates.select_course)


@router.message(SettingsStates.select_course, F.text.in_(available_courses))
async def select_course_handler(message: Message, state: FSMContext):
    # Write selected course to database

    if message.from_user.id not in users_settings:
        users_settings[message.from_user.id] = UserSettings()
    users_settings[message.from_user.id].select_course(message.text)

    await message.answer("Course selected!", reply_markup=ReplyKeyboardRemove())
    await start(message, state)


# if course was marked with ✅, remove it from user settings
@router.message(SettingsStates.select_course, F.text.in_(available_courses_marked))
async def select_course_handler(message: Message, state: FSMContext):
    # Write selected course to database
    course = message.text.split(" ")[0]  # remove ✅
    users_settings[message.from_user.id].remove_course(course)

    await message.answer("Course deleted!", reply_markup=ReplyKeyboardRemove())
    await start(message, state)


# Incorrect course case
@router.message(SettingsStates.select_course)
async def select_course_handler(message: Message, state: FSMContext):
    await message.answer("Invalid course", reply_markup=make_row_keyboard(available_courses))
    await start(message, state)


# ------------------- Select lectures -------------------

@router.message(Command("select_lectures"))
async def select_lectures(message: Message, state: FSMContext):
    available_lectures_marked = get_marked_lectures(message)
    await message.answer("Select lectures", reply_markup=make_row_keyboard(available_lectures_marked))
    await state.set_state(SettingsStates.select_lectures)


@router.message(SettingsStates.select_lectures, F.text.in_(available_lectures))
async def select_lectures_handler(message: Message, state: FSMContext):
    # Logic for selecting lectures
    users_settings[message.from_user.id].add_lecture(message.text)
    await message.answer("Lectures selected!", reply_markup=ReplyKeyboardRemove())
    await start(message, state)


@router.message(SettingsStates.select_lectures, F.text.in_(available_lectures_marked))
async def select_lectures_handler(message: Message, state: FSMContext):
    # Logic for selecting lectures
    lecture = message.text.split(" ")[0]
    users_settings[message.from_user.id].remove_lecture(lecture)
    await message.answer("Lecture deleted!", reply_markup=ReplyKeyboardRemove())
    await start(message, state)


@router.message(SettingsStates.select_lectures)
async def select_lectures_handler(message: Message):
    await message.answer("Invalid lectures", reply_markup=make_row_keyboard(available_lectures))

# ------------------- Manage notifications -------------------


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
