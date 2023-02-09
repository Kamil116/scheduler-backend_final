import arrow
from app.db import db
from app.telegram.schedule import controller as schedule_controller
from app.telegram.remind import data


def set_reminder_off(user_id):
    db.user.update(where={"id": user_id}, data={"remind_me": False})


def set_reminder_on(user_id):
    db.user.update(where={"id": user_id}, data={"remind_me": True})


def get_reminder_times():
    start_times = db.query_raw(
        '''
        SELECT DISTINCT start_time 
        FROM "Slot"
        ORDER BY start_time
        ''')
    unique_start_times = []

    for start_time in start_times:
        arrow_time = schedule_controller.get_time_in_local_timezone(
            start_time['start_time']).shift(minutes=-data.REMIND_WHEN_LEFT_MINUTES)
        string_time = arrow_time.format('HH:mm')
        if string_time not in unique_start_times:
            unique_start_times.append(string_time)
    print(unique_start_times)
    return unique_start_times


def get_reminder_subscribers():
    users = db.user.find_many()
    need_remind = []
    for user in users:
        if not user.remind_me or not user.group_id:
            continue
        slot = schedule_controller.get_next_lesson(user.id)
        if not slot:
            continue
        min_before_start = schedule_controller.minutes_before_start(slot)
        print(min_before_start)
        if slot and abs(min_before_start - data.REMIND_WHEN_LEFT_MINUTES) <= 5:
            need_remind.append((user.id, slot))
    print(need_remind)
    print(f"Reminding #{len(need_remind)} subscribers")
    return need_remind
