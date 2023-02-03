from app.telegram.core.handlers import bot, log, main_markup
from app.telegram.schedule import data, controller
import telebot


def attach_schedule_module():

    @bot.message_handler(commands=['config_schedule'])
    def schedule_configuration(message):
        log(data.MODULE_NAME, message)

        if message.text == "/config_schedule":
            user = controller.get_user(message.from_user.id)
            if not user:
                controller.register_user(
                    message.from_user.id, message.from_user.username)

            options = telebot.types.ReplyKeyboardMarkup(True, False)
            group_levels = controller.get_group_levels()
            options.add(*group_levels)
            msg = bot.send_message(
                message.chat.id, data.REQUEST_COURSE, reply_markup=options)
            bot.register_next_step_handler(
                msg, process_course_step, group_levels)

    def process_course_step(message, group_levels):
        log(data.MODULE_NAME, message)

        if not message.text:
            bot.send_message(message.chat.id, data.MESSAGE_ERROR,
                             reply_markup=main_markup)
            return

        course = message.text
        if course not in group_levels:
            bot.send_message(message.chat.id, data.MESSAGE_ERROR,
                             reply_markup=main_markup)
            return

        options = telebot.types.ReplyKeyboardMarkup(True, False)
        specific_groups = controller.get_specific_group(course)
        options.add(*specific_groups)
        msg = bot.send_message(
            message.chat.id, data.REQUEST_GROUP, reply_markup=options)
        bot.register_next_step_handler(
            msg, process_group_step, specific_groups)

    def process_group_step(message, specific_groups):
        log(data.MODULE_NAME, message)
        if not message.text:
            bot.send_message(message.chat.id, data.MESSAGE_ERROR,
                             reply_markup=main_markup)
            return

        if message.text not in specific_groups:
            bot.send_message(message.chat.id, data.MESSAGE_ERROR,
                             reply_markup=main_markup)
            return
        specific_group = message.text
        controller.add_user_group(specific_group, message.from_user.id)
        bot.send_message(message.chat.id, data.MESSAGE_SETTINGS_SAVED,
                         reply_markup=main_markup)

    @bot.message_handler(regexp=f"^({data.TEXT_BUTTON_NOW}|"
                         f"{data.TEXT_BUTTON_DAY}|"
                         f"{data.TEXT_BUTTON_WEEK})$"
                         )
    def main_buttons_handler(message):
        log(data.MODULE_NAME, message)
        user = controller.get_user(message.chat.id)
        if not user or not user.group_id:
            bot.send_message(
                message.chat.id, data.MESSAGE_USER_NOT_configD, reply_markup=main_markup)
            return
        if user.handle != message.from_user.username:
            controller.update_user_alias(
                message.from_user.id, message.from_user.username)

        if message.text == data.TEXT_BUTTON_NOW:
            send_current_schedule(message.chat.id, message.from_user.id)
        elif message.text == data.TEXT_BUTTON_DAY:
            markup = telebot.types.ReplyKeyboardMarkup(True)
            buttons = list()
            day_of_week = controller.get_day_of_the_week()
            for i, day in enumerate(data.TEXT_DAYS_OF_WEEK):
                buttons.append(telebot.types.KeyboardButton(
                    day if day_of_week != i else day + "⭐"))
            markup.add(*buttons)
            bot.send_message(
                message.chat.id, data.REQUEST_WEEKDAY, reply_markup=markup)
        elif message.text == data.TEXT_BUTTON_WEEK:
            bot.send_message(message.chat.id, data.MESSAGE_FULL_WEEK,
                             reply_markup=main_markup, parse_mode="MarkdownV2")

    def send_current_schedule(chat_id, about_user_id):
        current_lesson = controller.get_current_lesson(about_user_id)
        next_lesson = controller.get_next_lesson(about_user_id)

        reply = data.HEADER_NOW + \
            controller.get_str_current(
                current_lesson) if current_lesson else ""

        if next_lesson:
            reply += data.HEADER_NEXT + controller.get_str_future(next_lesson)
        else:
            reply += data.HEADER_NO_NEXT_LESSONS
        bot.send_message(chat_id, reply, reply_markup=main_markup)

    @bot.message_handler(regexp=f"^({'|'.join(data.TEXT_DAYS_OF_WEEK)})⭐?$")
    def weekday_select_handler(message):
        log(data.MODULE_NAME, message)

        user = controller.get_user(message.chat.id)
        if not user or not user.group_id:
            bot.send_message(
                message.chat.id, data.MESSAGE_USER_NOT_configD, reply_markup=main_markup)
            return

        weekday = message.text[:2]
        if weekday not in data.TEXT_DAYS_OF_WEEK:
            return

        schedule = controller.get_day_lessons(
            message.from_user.id, day=data.TEXT_DAYS_OF_WEEK.index(weekday))

        reply = data.MESSAGE_FREE_DAY if not schedule else \
            data.HEADER_SEPARATOR.join(
                controller.print_slot(lesson) for lesson in schedule)
        bot.send_message(message.chat.id, reply, reply_markup=main_markup)
