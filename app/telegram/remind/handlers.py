from app.telegram.core.handlers import bot, log, main_markup
from app.telegram.remind import data, controller
from app.telegram.schedule import controller as schedule_controller
import telebot
import schedule


def attach_remind_module():

    @bot.message_handler(commands=['config_remind'])
    def remind_configuration(message):
        log(data.MODULE_NAME, message)
        if message.text == '/config_remind':
            print(f"CONFIG REMIND pressed by {message.from_user.id}")
            markup = telebot.types.ReplyKeyboardMarkup(True, False)
            markup.add(data.MESSAGE_YES, data.MESSAGE_NO)
            msg = bot.send_message(
                message.chat.id, data.REQUEST_REMINDERS, reply_markup=markup)
            bot.register_next_step_handler(msg, process_reminders_step)

    def process_reminders_step(message):
        log(data.MODULE_NAME, message)
        if not message.text:
            bot.send_message(message.chat.id, data.MESSAGE_ERROR,
                             reply_markup=main_markup)
            return
        user_id = message.from_user.id
        print(f"{message.text} pressed by {message.from_user.id}")
        if message.text == data.MESSAGE_YES:
            controller.set_reminder_on(user_id)
        elif message.text == data.MESSAGE_NO:
            controller.set_reminder_off(user_id)
        else:
            bot.send_message(message.chat.id, data.MESSAGE_ERROR,
                             reply_markup=main_markup)
            return
        bot.send_message(
            message.chat.id, data.MESSAGE_SETTINGS_SAVED, reply_markup=main_markup)

    def remind_time():
        # get relevant reminders for current moment
        print(f"STARTING REMIND SCHEDULER")
        for remind in controller.get_reminder_subscribers():
            user_id, slot = remind[0], remind[1]
            try:
                bot.send_message(user_id, data.HEADER_REMIND +
                                 schedule_controller.print_slot(slot), reply_markup=main_markup)
                print(f"Reminder sent to {user_id}")
            except Exception as exception:
                print(f"Error occured Sending Reminder sent to {user_id}")
                # if hasattr(exception, 'result') and exception.result.status_code == 403:
                controller.set_reminder_off(user_id)
                continue
        print(f"STOPPING REMIND SCHEDULER")

    # calculate time when to call remind_time
    for time_start in controller.get_reminder_times():
        schedule.every().day.at(time_start).do(remind_time)
