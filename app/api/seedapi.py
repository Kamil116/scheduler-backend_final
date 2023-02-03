from fastapi import APIRouter
from app.db import db

# seed data
from app.data import MAIN_GROUPS, MAIN_COURSES, MAIN_SLOTS

router = APIRouter(tags=["Seed"], prefix="")


@router.get('/seed_group')
def seed_group():
    for key in MAIN_GROUPS:
        for group in MAIN_GROUPS[key]:
            db.group.create({
                "level_name": key, "specific_group": group
            })
    return {"message": "successful"}


@router.get('/seed_course')
def seed_course():
    for course in MAIN_COURSES:
        if not course["for_all_sub_groups"]:
            # get the ids of all groups in 'sub_groups' attribute
            course_groups_ids = []
            specific_groups = course['sub_groups']
            for name in specific_groups:
                group = db.group.find_first(
                    where={"level_name": course['groups'], "specific_group": name})
                course_groups_ids.append({"id": group.id})
            # create course and connect groups by id
            db.course.create(data={
                "description": course["name"],
                "is_elective": False,
                "groups": {
                    "connect": course_groups_ids
                }
            })
        else:
            group_name = course["groups"]
            course_groups = db.group.find_many(
                where={"level_name": group_name})
            print(course_groups)
            course_groups_ids = list(
                map(lambda course: {"id": course.id}, course_groups))
            print(course_groups_ids)
            db.course.create(data={
                "description": course["name"],
                "is_elective": False,
                "groups": {
                    "connect": course_groups_ids
                }
            })
    return {"message": "successful"}


@router.get('/seed_slot')
def seed_slot():
    db.slot.create_many(data=MAIN_SLOTS)
    return {"message": "successful"}


@router.get('/drop_slot')
def drop_slot():
    db.slot.delete_many()
    return {"message": "successful"}


@router.get('/connect_slot_course_group')
def connect_slot_course_group():
    slots = db.slot.find_many()
    for slot in slots:
        course = db.course.find_first(where={"description": slot.course_name})
        group = db.group.find_first(
            where={"specific_group": slot.specific_group})

        if course and group:
            db.slot.update(data={
                "course": {
                    "connect": {
                        "id": course.id
                    }
                },
                "group": {
                    "connect": {
                        "id": group.id
                    }
                }
            }, where={"id": slot.id})
        elif course:
            db.slot.update(data={
                "course": {
                    "connect": {
                        "id": course.id
                    }
                }
            }, where={"id": slot.id})
        elif group:
            db.slot.update(data={
                "group": {
                    "connect": {
                        "id": group.id
                    }
                }
            }, where={"id": slot.id})
    return {"message": "successful"}
