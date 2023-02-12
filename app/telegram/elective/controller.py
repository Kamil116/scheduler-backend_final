import arrow
from app.db import db
from app.telegram.schedule import data


def get_user(user_id):
    user = db.user.find_unique(where={'id': user_id})
    return user


def get_user_with_settings(user_id):
    user = db.user.find_unique(
        where={'id': user_id}, include={"main_group": True})
    return user


def get_user_with_elective(user_id):
    user = db.user.find_unique(
        where={'id': user_id}, include={"elective_courses": True})
    return user


def register_user(user_id, handle=""):
    return db.user.create(data={
        "id": user_id,
        "handle": handle
    })


def update_user_alias(user_id, handle):
    return db.user.update(where={'id': user_id}, data={"handle": handle})


def get_elective_courses(group_level):
    elective_courses = db.course.find_many(where={
        "valid_group": group_level,
        "is_elective": True
    })
    abbreviations = list(
        map(lambda course: course.short_name, elective_courses))
    return abbreviations


def get_optional_courses():
    return db.course.find_many(where={"valid_group": "ALL"})


def get_specific_group(group_level):
    specific_groups = db.group.find_many(where={"level_name": group_level})
    return list(map(lambda group: group.specific_group, specific_groups))


def add_user_elective(elective, user_id):
    course = db.course.find_first(where={"short_name": elective})
    if not course:
        return []
    return db.user.update(
        data={
            "elective_courses": {
                "connect": {
                    "id": course.id,
                }
            }
        },
        where={
            "id": user_id,
        }
    )


def add_user_optional_course(optional_course_short_name, user_id):
    course = db.course.find_first(
        where={"short_name": optional_course_short_name})
    if not course:
        return []
    return db.user.update(
        data={
            "optional_course": {
                "connect": {
                    "id": course.id,
                }
            }
        },
        where={
            "id": user_id,
        }
    )


def clear_elective_courses(user_id, ids_to_disconnect):
    return db.user.update(
        data={
            "elective_courses": {
                "disconnect": ids_to_disconnect
            }
        }, where={"id": user_id})


def get_electives(user_id):
    user = db.user.find_unique(
        where={"id": user_id},
        include={"elective_courses": True}
    )
    return user.elective_courses


def get_current_lesson(user_id):
    user = db.user.find_unique(where={"id": user_id}, include={
                               "elective_courses": True})
    elective_courses_ids = list(
        map(lambda course: course.id, user.elective_courses))
    timenow = arrow.now(data.TIMEZONE).isoformat()
    lesson = db.slot.find_first(
        where={
            "OR": [
                {"group_id": user.group_id},
                {"course_id": {
                    "in": elective_courses_ids
                }}],
            "start_time": {
                "lte": timenow
            },
            "end_time": {
                "gte": timenow
            }
        }
    )
    return lesson


def get_next_lesson(user_id):
    user = db.user.find_unique(where={"id": user_id}, include={
                               "elective_courses": True})
    elective_courses_ids = list(
        map(lambda course: course.id, user.elective_courses))
    timenow = arrow.now(data.TIMEZONE)
    iso_timenow = timenow.datetime
    date_start = arrow.get(timenow.date())
    date_end = date_start.shift(days=+1)
    lessons = db.slot.find_many(
        order={
            "start_time": "asc"
        },
        where={
            "OR": [
                {"group_id": user.group_id},
                {"course_id": {
                    "in": elective_courses_ids
                }}],
            "start_time": {
                "gte": date_start.isoformat(),
                "lte": date_end.isoformat()
            }
        }
    )
    for lesson in lessons:
        lesson_start = get_time_in_timezone_datetime(lesson.start_time)
        if lesson_start > iso_timenow:
            return lesson
    return None


def get_day_lessons(user_id, day):
    user = db.user.find_unique(where={"id": user_id}, include={
                               "elective_courses": True})
    elective_courses_ids = list(
        map(lambda course: course.id, user.elective_courses))
    current_time = arrow.now(data.TIMEZONE)
    current_weekday = current_time.weekday()
    choosen_date = current_time.shift(days=day-current_weekday).date()

    date_start = arrow.get(choosen_date)
    date_end = date_start.shift(days=+1)
    lessons = db.slot.find_many(
        order={
            "start_time": "asc"
        },
        where={
            "OR": [
                {"group_id": user.group_id},
                {"course_id": {
                    "in": elective_courses_ids
                }}],
            "start_time": {
                "gte": date_start.isoformat(),
                "lte": date_end.isoformat()
            }
        }
    )
    return lessons


def get_week_lessons(user_id):
    user = db.user.find_unique(where={"id": user_id}, include={
                               "elective_courses": True})
    elective_courses_ids = list(
        map(lambda course: course.id, user.elective_courses))
    current_time = arrow.now(data.TIMEZONE)
    monday_morning = current_time.shift(
        weekday=0).replace(hour=1, minute=0, second=0)
    friday_evening = monday_morning.shift(
        weekday=5).replace(hour=23, minute=0, second=0)

    lessons = db.slot.find_many(
        order={
            "start_time": "asc"
        },
        where={
            "OR": [
                {"group_id": user.group_id},
                {"course_id": {
                    "in": elective_courses_ids
                }}],
            "start_time": {
                "gte": monday_morning.isoformat(),
                "lte": friday_evening.isoformat()
            }
        }
    )
    return lessons


def get_week_number():
    time_now = arrow.now(data.TIMEZONE)
    start_academic_yr = arrow.get(data.ACADEMIC_YEAR_START).to(data.TIMEZONE)
    weeks = 0
    for i in arrow.Arrow.span_range("week", start_academic_yr, time_now):
        weeks += 1
    return weeks


###############
# Helper methods
###############


def get_time_in_timezone_datetime(time):
    return arrow.get(time).to(data.TIMEZONE).datetime


def get_time_in_timezone_arrow(time):
    return arrow.get(time).to(data.TIMEZONE)


def get_time_in_local_timezone(time):
    return arrow.get(time).to('local')


def minutes_until_end(slot):
    seconds_left = get_time_in_timezone_arrow(
        slot.end_time) - arrow.now(data.TIMEZONE)
    print(f"SECONDS LEFT for {slot.course_name}:",
          seconds_left.total_seconds() / 60)
    return round(seconds_left.total_seconds() / 60)


def minutes_before_start(slot):
    seconds_to_begin = get_time_in_timezone_arrow(
        slot.start_time) - arrow.now(data.TIMEZONE)
    print(f"SECONDS TO BEGIN {slot.course_name}:",
          seconds_to_begin.total_seconds() / 60)
    return round(seconds_to_begin.total_seconds() / 60)


def get_str_current(slot):
    min_until_end = minutes_until_end(slot)
    hours_until_end = min_until_end // 60
    return f"{print_slot(slot)}⏸️ {str(hours_until_end) + 'h ' if hours_until_end > 0 else ''}"\
        f"{min_until_end % 60}m\n"


def get_str_future(slot):
    min_before_start = minutes_before_start(slot)
    hours_before_start = min_before_start // 60
    return f"{print_slot(slot)}▶ ️ {str(hours_before_start) + 'h ' if hours_before_start > 0 else ''}"\
        f"{min_before_start % 60}m\n"


def print_slot(slot):
    start = get_time_in_timezone_arrow(
        slot.start_time).format('HH:mm')
    end = get_time_in_timezone_arrow(slot.end_time).format('HH:mm')
    return f"{slot.course_name}\n"\
        f"👨‍🏫 {slot.instructor_name}\n"\
        f"🕐 {start} - {end}\n"\
        f"🚪 {slot.room_number if slot.room_number else '?'}"


def get_day_of_the_week():
    return arrow.now(data.TIMEZONE).weekday()
