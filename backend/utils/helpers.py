from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    """
    Make a keyboard with one row of buttons.

    Parameters:
        items: list of button names

    Returns:
        ReplyKeyboardMarkup
    """

    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)


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

start_menu = ['Today', 'Week', 'Month', 'Settings']
settings_menu = ['Select course', 'Select group', 'Manage notifications']


def get_marked_courses():
    local_courses = available_courses.copy()

    for course in local_courses:
        course += " ✅"

    return local_courses


def get_marked_groups():
    # add mark to selected groups
    local_groups = available_groups.copy()

    for group in local_groups:
        group += " ✅"

    return local_groups
