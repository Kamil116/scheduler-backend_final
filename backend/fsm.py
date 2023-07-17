from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
import json

import data.data_parser as parser

from backend.bot import bot

from backend.db import StudentsInfoDatabase
from backend.apsched import send_notification
from backend.parsedDataToDatabase import coursesDatabase
from backend.utils.helpers import make_row_keyboard, get_marked_courses, get_marked_groups, start_menu, settings_menu, \
    available_courses, available_groups

router = Router()

db = StudentsInfoDatabase("data/users.db")


class MenuStates(StatesGroup):
    start = State()
    day = State()
    week = State()
    month = State()
    settings = State()


class SettingsStates(StatesGroup):
    select_course = State()
    select_group = State()
    select_lectures = State()
    manage_notifications = State()


# ------------------- Start -------------------


@router.message(Command("start"))
async def start(message: Message, state: FSMContext):
    await state.set_state(MenuStates.start)
    if not db.user_exists(message.from_user.id):
        db.add_user(message.from_user.id)
        await message.answer("You are not registered. Please send your course and group:",
                             reply_markup=make_row_keyboard(start_menu))
    else:
        await message.answer("Please select action:", reply_markup=make_row_keyboard(start_menu))


@router.message(MenuStates.start, F.text.in_(start_menu))
async def start_handler(message: Message, state: FSMContext):
    # read json file with parsed data

    match message.text:
        case "Today":
            await today(parser.today, state)
        case "Week":
            await week(parser.week, state)
        case "Month":
            await month(parser.month, state)
        case "Settings":
            await settings(message, state)
        case _:
            await message.answer("Invalid action", reply_markup=make_row_keyboard(start_menu))


# ------------------- Menu States Logic -------------------


@router.message(Command("Today"))
async def today(message: Message, state: FSMContext):
    # read json file
    with open("data/output.json") as f:
        data = json.load(f)

    await message.answer("Today")
    await start(message, state)


@router.message(Command("Week"))
async def week(message: Message, state: FSMContext):
    await message.answer("Week")
    await start(message, state)


@router.message(Command("Month"))
async def month(message: Message, state: FSMContext):
    await message.answer("Month")
    await start(message, state)


@router.message(Command("Settings"))
async def settings(message: Message, state: FSMContext):
    await state.set_state(MenuStates.settings)
    await message.answer("Select option:", reply_markup=make_row_keyboard(settings_menu))


@router.message(MenuStates.settings, F.text.in_(settings_menu))
async def settings_handler(message: Message, state: FSMContext):
    match message.text:
        case "Select course":
            await select_course(message, state)
        case "Select group":
            await select_group(message, state)
        case "Manage notifications":
            await manage_notifications(message, state)


@router.message(MenuStates.settings)
async def settings_handler(message: Message, state: FSMContext):
    await message.answer("Invalid action", reply_markup=make_row_keyboard(settings_menu))


# ------------------- Select course -------------------


@router.message(Command("Select course"))
async def select_course(message: Message, state: FSMContext):
    available_courses_marked = get_marked_courses()
    await message.answer("Please select course:", reply_markup=make_row_keyboard(available_courses_marked))
    await state.set_state(SettingsStates.select_course)


@router.message(SettingsStates.select_course, F.text.in_(available_courses))
async def select_course_handler(message: Message, state: FSMContext):
    '''Write course to DB and send message to user'''

    # Saving info about course in DB
    db.update_course(message.text, message.chat.id)

    await message.answer("Course selected!", reply_markup=ReplyKeyboardRemove())
    await start(message, state)


# Incorrect course case
@router.message(SettingsStates.select_course)
async def select_course_handler(message: Message, state: FSMContext, apscheduler: AsyncIOScheduler):
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
    await message.answer("Invalid course", reply_markup=make_row_keyboard(available_courses))
    await start(message, state)


# ------------------- Select group -------------------


@router.message(Command("select_group"))
async def select_group(message: Message, state: FSMContext):
    available_groups_marked = get_marked_groups()
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


# Incorrect group case
@router.message(SettingsStates.select_group)
async def select_group_handler(message: Message, state: FSMContext):
    await message.answer("Invalid group", reply_markup=make_row_keyboard(available_groups))
    await start(message, state)


# ------------------- Manage notifications -------------------


@router.message(Command("Manage notifications"))
async def manage_notifications(message: Message, state: FSMContext):
    await message.answer("Manage notifications", reply_markup=make_row_keyboard(["Enable", "Disable"]))
    await state.set_state(SettingsStates.manage_notifications)


@router.message(SettingsStates.manage_notifications, F.text.in_(["Enable"]))
async def manage_notifications_handler(message: Message, state: FSMContext):
    # Logic for managing notifications
    await message.answer("Notifications are enabled!", reply_markup=ReplyKeyboardRemove())
    await start(message, state)


@router.message(SettingsStates.manage_notifications, F.text.in_(["Disable"]))
async def manage_notifications_handler(message: Message, state: FSMContext):
    # Logic for managing notifications
    await message.answer("Notifications are disabled!", reply_markup=ReplyKeyboardRemove())
    await start(message, state)


@router.message(SettingsStates.manage_notifications)
async def manage_notifications_handler(message: Message, state: FSMContext):
    await message.answer("Invalid action", reply_markup=make_row_keyboard(["Enable", "Disable"]))
    await state.set_state(SettingsStates.manage_notifications)
