from pytz import timezone

MODULE_NAME = "schedule"

TEXT_DAYS_OF_WEEK = ("Mo", "Tu", "We", "Th", "Fr", "Sa")
TEXT_BUTTON_NOW = "NOW❗"
TEXT_BUTTON_DAY = "DAY⌛"
TEXT_BUTTON_WEEK = "WEEK 🗓️"

MESSAGE_USER_NOT_CONFIGURED = "Sorry. I do not know your groups yet. 😥\n" \
                              "Please use /configure_schedule command to set it up"
MESSAGE_FULL_WEEK = "[Full week schedule](https://docs.google.com/spreadsheets/d/1hVcGurw7LAOmTpk6n19Kho67xyDtvTiIA0KM4G71mdU/edit#gid=398810915)"
MESSAGE_FREE_DAY = "No lessons on this day! Lucky you are!"
MESSAGE_FRIEND_NOT_FOUND = "Sorry. Your friend is not registered.\nPlease tell him about our cool bot!"
MESSAGE_ERROR = "Sorry, I did not understand you"
MESSAGE_SETTINGS_SAVED = "Your schedule settings have been saved successfully!\n" \
                         "If you want to receive reminders about upcoming lectures use /configure_remind"

REQUEST_COURSE = "What's your course?"
REQUEST_GROUP = "What's your group?"
REQUEST_ENGLISH = "What's your English group?"
REQUEST_ALIAS = "What's your friend's alias?\n" \
                "By the way, now you can just send friend's alias without calling these command"
REQUEST_WEEKDAY = "Select day of the week"

HEADER_NOW = "\n"
HEADER_NEXT = "\n"
HEADER_NO_NEXT_LESSONS = "                  🗽"
HEADER_SEPARATOR = "\n"

TIMEZONE = timezone("Europe/Moscow")