from app.telegram.core.handlers import bot, log, main_markup
from app.telegram.elective import data, controller
import telebot


def attach_elective_module():

    @bot.message_handler(commands=['add_elective'])
    def elective_configuration(message):
        log(data.MODULE_NAME, message)
        print(f"ADD ELECTIVE pressed by {message.from_user.id}")
        user = controller.get_user_with_settings(message.from_user.id)
        if not user:
            controller.register_user(
                message.from_user.id, message.from_user.username)

        if not user.group_id:
            bot.send_message(
                message.chat.id, data.MESSAGE_USER_NOT_configD, reply_markup=main_markup)
            return

        options = telebot.types.ReplyKeyboardMarkup(True, False)
        group_level_name = user.main_group.level_name
        if not group_level_name:
            return

        elective_courses = controller.get_elective_courses(group_level_name)
        if not elective_courses:
            bot.send_message(
                message.chat.id, "You have no elective courses", reply_markup=main_markup)
            return

        options.add(*elective_courses)
        msg = bot.send_message(
            message.chat.id, data.REQUEST_ELECTIVE, reply_markup=options)
        bot.register_next_step_handler(
            msg, process_elective_step, elective_courses)

    def process_elective_step(message, elective_courses):
        log(data.MODULE_NAME, message)
        if not message.text:
            bot.send_message(message.chat.id, data.MESSAGE_ERROR,
                             reply_markup=main_markup)
            return

        elective = message.text
        if elective not in elective_courses:
            bot.send_message(message.chat.id, data.MESSAGE_ERROR,
                             reply_markup=main_markup)
            return

        print(f"{elective} pressed by {message.from_user.id}")
        controller.add_user_elective(elective, message.from_user.id)
        bot.send_message(message.chat.id, data.MESSAGE_SETTINGS_SAVED,
                         reply_markup=main_markup)

    @bot.message_handler(commands=['rm_electives'])
    def remove_elective(message):
        log(data.MODULE_NAME, message)
        print(f"REMOVE ELECTIVE pressed by {message.from_user.id}")
        user = controller.get_user_with_elective(message.from_user.id)
        if not user:
            controller.register_user(
                message.from_user.id, message.from_user.username)
        elective_courses = user.elective_courses
        if not elective_courses:
            bot.send_message(
                message.chat.id, "No elective courses", reply_markup=main_markup)
            return
        ids_to_disconnect = list(
            map(lambda course: {"id": course.id}, elective_courses))
        print(ids_to_disconnect)
        controller.clear_elective_courses(
            message.from_user.id, ids_to_disconnect)
        bot.send_message(
            message.chat.id, data.CLEARED_ELECTIVE, reply_markup=main_markup)

    @bot.message_handler(commands=['config_optional'])
    def config_optional(message):
        log(data.MODULE_NAME, message)
        print(f"CONFIG OPTIONAL pressed by {message.from_user.id}")
        user = controller.get_user(message.from_user.id)
        if not user:
            controller.register_user(
                message.from_user.id, message.from_user.username)

        options = telebot.types.ReplyKeyboardMarkup(True, False)
        optional_courses = controller.get_optional_courses()
        optional_short_names = list(
            map(lambda course: course.short_name, optional_courses))
        options.add(*optional_short_names)
        msg = bot.send_message(
            message.chat.id, data.REQUEST_OPTIONAL, reply_markup=options)
        bot.register_next_step_handler(
            msg, process_optional_course_step, optional_short_names)

    def process_optional_course_step(message, optional_short_names):
        log(data.MODULE_NAME, message)
        if not message.text:
            bot.send_message(message.chat.id, data.MESSAGE_ERROR,
                             reply_markup=main_markup)
            return

        optional_course_name = message.text
        if optional_course_name not in optional_short_names:
            bot.send_message(message.chat.id, data.MESSAGE_ERROR,
                             reply_markup=main_markup)
            return

        print(f"{optional_course_name} pressed by {message.from_user.id}")
        controller.add_user_optional_course(
            optional_course_name, message.from_user.id)
        bot.send_message(message.chat.id, data.MESSAGE_OPTIONAL_SETTINGS_SAVED,
                         reply_markup=main_markup)
