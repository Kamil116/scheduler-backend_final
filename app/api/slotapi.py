import arrow
from fastapi import APIRouter
from app.db import db
from app.schema import schemas

router = APIRouter(tags=["Slots"], prefix="/slot")


@router.get("/")
def get_slots(start: str = "", end: str = "", group: str = "", course: str = "",):
    print("++++++++++++++++++++++++++++++")
    print(start, end, group, course)
    print("++++++++++++++++++++++++++++++")
    slots = []
    if group:
        group_with_time_slots = db.group.find_first(
            where={
                "specific_group": group,
            },
            include={
                "time_table": True
            }
        )
        # group_with_time_slots
        slots = group_with_time_slots.time_table
    elif course:
        course_time_slots = db.course.find_first(
            where={"description": course}, include={"time_slots": True})
        slots = course_time_slots.time_slots
    else:
        slots = db.slot.find_many(
            include={"course": True},
            where={
                "start_time": {
                    "gte": start if start else "2023-02-02T07:40:00+00:00"
                },
                "end_time": {
                    "lte": end if end else "2023-02-03T07:40:00+00:00"
                }
            }
        )
    return slots
# "\\copy public.\"Slot\" (id, instructor_name, room_number, start_time, end_time, course_id, course_name, type, group_id, specific_group) FROM '/Users/danielatonge/Downloads/week3_schedule/slot.csv' DELIMITER ',' CSV HEADER QUOTE '\"' ESCAPE '''';""

@router.post("/")
def create_slot(slotInput: schemas.Slot):
    return db.slot.create(data={
        "start_time": slotInput.start_time.isoformat(),
        "end_time": slotInput.end_time.isoformat(),
        "instructor_name": slotInput.instructor_name,
        "room_number": slotInput.room_number,
        "course_id": slotInput.course_id,
        "group_id": slotInput.group_id,
        "course_name": slotInput.course_name,
        "type": slotInput.type
    })


@router.post("/:slot_id")
def generate_within_range(slot_id: str, slotRange: schemas.SlotRange):
    slot = db.slot.find_unique(where={"id": slot_id})

    slot_start_datetime = arrow.get(slot.start_time).to('Europe/Moscow')
    slot_start_weekday = slot_start_datetime.weekday()
    slot_start_time = slot_start_datetime.time()

    slot_end_datetime = arrow.get(slot.end_time).to('Europe/Moscow')
    slot_end_time = slot_end_datetime.time()

    start_date = arrow.get(slotRange.start_date)
    end_date = arrow.get(slotRange.end_date)

    # print(
    #     f"BEGIN - start_date: {start_date} \t end_date: {end_date} \t others: {slot_start_time}, {slot_end_time}")
    while start_date <= end_date:
        start_datetime = start_date.shift(
            weekday=slot_start_weekday).replace(hour=slot_start_time.hour, minute=slot_start_time.minute)
        end_datetime = end_date.shift(
            weekday=slot_start_weekday).replace(hour=slot_end_time.hour, minute=slot_end_time.minute)
        # print(
        #     f"FINAL - start_datetime: {start_datetime} \t end_datetime: {end_datetime}")
        db.slot.create(data={
            "start_time": start_datetime.isoformat(),
            "end_time": end_datetime.isoformat(),
            "instructor_name": slot.instructor_name,
            "room_number": slot.room_number,
            "course_id": slot.course_id,
            "group_id": slot.group_id,
            "course_name": slot.course_name,
            "type": slot.type,
            "specific_group": slot.specific_group
        })
        start_date = start_date.shift(weeks=+1)

    return {"message": "success"}


@router.patch("/:slot_id")
def modify_slot(slot_id: str, slotUpdate: schemas.SlotUpdate):
    return db.slot.update(where={"id": slot_id}, data=slotUpdate)


@router.delete("/:slot_id")
def delete_slot(slot_id: str):
    return db.slot.delete(where={"id": slot_id})
