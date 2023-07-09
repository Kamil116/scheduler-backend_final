from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from db import StudentsInfoDatabase
from parsedDataToDatabase import coursesDatabase
from bot import bot
from datetime import datetime, timedelta
from apsched import send_notification
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from helpers import make_row_keyboard

router = Router()
db = StudentsInfoDatabase('users.db')

available_courses = ['B19', 'B20', 'B21', 'B22', 'MS1', 'MS2']
available_courses_marked = []
for course in available_courses:
    available_courses_marked.append(course + " ✅")

# TODO: match course and studying groups. For example, in B19 we have only 6 groups.
available_groups = ['CS-01', 'CS-02', 'CS-03', 'CS-04', 'CS-05']
available_groups_marked = []
for group in available_groups:
    available_groups_marked.append(group + " ✅")

available_lectures = ['Sport', 'Math', 'English', 'Programming', 'History']
available_lectures_marked = []
for lecture in available_lectures:
    available_lectures_marked.append(lecture + " ✅")
start_menu = ['Select course', 'Select group',
              'Select lectures', 'Manage notifications']


def get_marked_courses(message: Message):
    # add mark to selected courses
    local_courses = available_courses.copy()

    user_course = db.get_course(message.from_user.id)

    if user_course != '':
        local_courses[local_courses.index(user_course)] += " ✅"

    return local_courses


def get_marked_groups(message: Message):
    # add mark to selected groups
    local_groups = available_groups.copy()

    user_group = db.get_group(message.from_user.id)

    if user_group != '':
        local_groups[local_groups.index(
            user_group)] += " ✅"

    return local_groups


# def get_marked_lectures(message: Message):
#     # add mark to selected lectures
#     local_lectures = available_lectures.copy()
#
#     for lecture in users_settings[message.from_user.id].get_lectures():
#         local_lectures[local_lectures.index(lecture)] += " ✅"
#
#     return local_lectures


class SettingsStates(StatesGroup):
    select_course = State()
    select_group = State()
    select_lectures = State()
    manage_notifications = State()
    start = State()


@router.message(Command("start"))
async def start(message: Message, state: FSMContext):
    # if not db.user_exists(message.from_user.id):
    #     db.add_user(message.from_user.id)
    if True:
        await state.set_state(SettingsStates.start)
        await message.answer("You are not registered. Please send your course and group:",
                             reply_markup=make_row_keyboard(start_menu))
    else:
        await state.set_state(SettingsStates.start)
        await message.answer("Please select action:", reply_markup=make_row_keyboard(start_menu))


@router.message(SettingsStates.start, F.text.in_(start_menu))
async def start_handler(message: Message, state: FSMContext):
    if message.text == "Select course":
        await select_course(message, state)
    elif message.text == "Select group":
        await select_group(message, state)
    # elif message.text == "Select lectures":
    #     await select_lectures(message, state)
    elif message.text == "Manage notifications":
        await manage_notifications(message, state)
    else:
        await message.answer("Invalid action", reply_markup=make_row_keyboard(start_menu))


# ------------------- Select course -------------------

@router.message(Command("select_course"))
async def select_course(message: Message, state: FSMContext):
    available_courses_marked = get_marked_courses(message)
    await message.answer("Please select course:", reply_markup=make_row_keyboard(available_courses_marked))
    await state.set_state(SettingsStates.select_course)


@router.message(SettingsStates.select_course, F.text.in_(available_courses))
async def select_course_handler(message: Message, state: FSMContext):
    # Write selected course to database

    # if message.from_user.id not in users_settings:
    #     users_settings[message.from_user.id] = UserSettings()
    # users_settings[message.from_user.id].select_course(message.text)

    # Saving info about course in DB
    db.update_course(message.text, message.chat.id)

    await message.answer("Course selected!", reply_markup=ReplyKeyboardRemove())
    await start(message, state)


# # if course was marked with ✅, remove it from user settings
# @router.message(SettingsStates.select_course, F.text.in_(available_courses_marked))
# async def select_course_handler(message: Message, state: FSMContext):
#     # Write selected course to database
#     course = message.text.split(" ")[0]  # remove ✅
#     users_settings[message.from_user.id].remove_course(course)
#
#     await message.answer("Course deleted!", reply_markup=ReplyKeyboardRemove())
#     await start(message, state)


# Incorrect course case
@router.message(SettingsStates.select_course)
async def select_course_handler(message: Message, state: FSMContext):
    await message.answer("Invalid course", reply_markup=make_row_keyboard(available_courses))
    await start(message, state)


# ------------------- Select group -------------------

@router.message(Command("select_group"))
async def select_group(message: Message, state: FSMContext):
    available_groups_marked = get_marked_groups(message)
    await message.answer("Please select group:", reply_markup=make_row_keyboard(available_groups_marked))
    await state.set_state(SettingsStates.select_group)


@router.message(SettingsStates.select_group, F.text.in_(available_groups))
async def select_group_handler(message: Message, state: FSMContext, apscheduler: AsyncIOScheduler):
    # Saving info about group in DB
    db.update_group(message.text, message.chat.id)

    cur_user_course = db.get_course(message.from_user.id)
    cur_user_group = db.get_group(message.from_user.id)

    # sending notification when we have user's course and study group
    courses = coursesDatabase.get_courses()

    for cur_course in courses:
        if cur_user_course + '-' + cur_user_group == cur_course[3]:
            if db.get_group(message.from_user.id) != '' and db.get_course(message.from_user.id) != '':
                # getting date and time
                date_and_time = cur_course[1].split("T")
                date = date_and_time[0]
                year = int(date.split('-')[0])
                month = int(date.split('-')[1])
                day = int(date.split('-')[2])
                time = date_and_time[1]
                hour = int(time.split(':')[0])
                minute = int(time.split(':')[1])

                apscheduler.add_job(send_notification, trigger='date',
                                    run_date=datetime(
                                        year, month, day, hour, minute, 0) + timedelta(minutes=-15),
                                    misfire_grace_time=59,
                                    kwargs={'bot': bot, 'chat_id': message.from_user.id, 'title': cur_course[0],
                                            'room': cur_course[2]})

    await message.answer("Group selected!", reply_markup=ReplyKeyboardRemove())
    await start(message, state)


# # if group was marked with ✅, remove it from user settings
# @router.message(SettingsStates.select_group, F.text.in_(available_groups_marked))
# async def select_group_handler(message: Message, state: FSMContext):
#     # Write selected course to database
#     group = message.text.split(" ")[0]  # remove ✅
#     users_settings[message.from_user.id].remove_group(group)
#
#     await message.answer("Group deleted!", reply_markup=ReplyKeyboardRemove())
#     await start(message, state)


# Incorrect group case
@router.message(SettingsStates.select_group)
async def select_group_handler(message: Message, state: FSMContext):
    await message.answer("Invalid group", reply_markup=make_row_keyboard(available_groups))
    await start(message, state)


#
# # ------------------- Select lectures -------------------
#
# @router.message(Command("select_lectures"))
# async def select_lectures(message: Message, state: FSMContext):
#     available_lectures_marked = get_marked_lectures(message)
#     await message.answer("Select lectures", reply_markup=make_row_keyboard(available_lectures_marked))
#     await state.set_state(SettingsStates.select_lectures)
#
#
# @router.message(SettingsStates.select_lectures, F.text.in_(available_lectures))
# async def select_lectures_handler(message: Message, state: FSMContext):
#     # Logic for selecting lectures
#     users_settings[message.from_user.id].add_lecture(message.text)
#     await message.answer("Lectures selected!", reply_markup=ReplyKeyboardRemove())
#     await start(message, state)
#
#
# @router.message(SettingsStates.select_lectures, F.text.in_(available_lectures_marked))
# async def select_lectures_handler(message: Message, state: FSMContext):
#     # Logic for selecting lectures
#     lecture = message.text.split(" ")[0]
#     users_settings[message.from_user.id].remove_lecture(lecture)
#     await message.answer("Lecture deleted!", reply_markup=ReplyKeyboardRemove())
#     await start(message, state)
#
#
# @router.message(SettingsStates.select_lectures)
# async def select_lectures_handler(message: Message):
#     await message.answer("Invalid lectures", reply_markup=make_row_keyboard(available_lectures))
#

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
