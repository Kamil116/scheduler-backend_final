import arrow
from fastapi import APIRouter
from app.db import db

# seed data
from app.data import MAIN_GROUPS, TIMEZONE, \
    MAIN_COURSES, ELECTIVE_COURSES, MAIN_SLOTS, \
    SNE_SLOTS, MS_ELECTIVE_SLOTS, SNE_COURSES, \
    B20_ELECTIVE_SLOTS, B19_ELECTIVE_SLOTS, \
    MS_ELECTIVE_NAMES, BS4_ELECTIVE_NAMES, BS3_ELECTIVE_NAMES, \
    RFL_COURSES, RFL_SLOTS

router = APIRouter(tags=["Seed"], prefix="")


@router.get('/seed_group')
def seed_group():
    for key in MAIN_GROUPS:
        for group in MAIN_GROUPS[key]:
            db.group.create({
                "level_name": key, "specific_group": group
            })
    return {"message": "successful"}


@router.get('/fix_slots')
def fix_slots():
    groups = ['B22-CS-01', 'B22-CS-02', 'B22-CS-03', 'B22-CS-04', 'B22-CS-05',
              'B22-CS-06', 'B22-DSAI-01', 'B22-DSAI-02', 'B22-DSAI-03', 'B22-DSAI-04',
              'SD21-01', 'SD21-02', 'SD21-03', 'CS21-01', 'DS21-01', 'DS21-02', 'AAI21-01', 'RO21-01',
              'B20-SD-01', 'B20-SD-02', 'B20-CS', 'B20-AI', 'B20-DS', 'B20-RO',
              'B19-SD-01', 'B19-SD-02', 'B19-DS-01', 'B19-AI-01', 'B19-CS-01', 'B19-RO-01',
              'M22-SE-01', 'M22-SE-02', 'M22-DS-01', 'M22-RO-01', 'M22-TE-01']
    slot = db.slot.delete_many(where={
        "start_time": {
            "gte": "2023-03-06T01:00:00.000Z"
        },
        "end_time": {
            "lte": "2023-03-11T21:00:00.000Z",
        },
        "group_id": {
            "not": None
        },
        "specific_group": {
            "in": groups
        }
    })
    print(slot)
    return {"message": "successful"}


@router.get('/generate_slot_for_next_week')
def generate_slot_for_next_week():
    groups = ['B22-CS-01', 'B22-CS-02', 'B22-CS-03', 'B22-CS-04', 'B22-CS-05',
              'B22-CS-06', 'B22-DSAI-01', 'B22-DSAI-02', 'B22-DSAI-03', 'B22-DSAI-04',
              'SD21-01', 'SD21-02', 'SD21-03', 'CS21-01', 'DS21-01', 'DS21-02', 'AAI21-01', 'RO21-01',
              'B20-SD-01', 'B20-SD-02', 'B20-CS', 'B20-AI', 'B20-DS', 'B20-RO',
              'B19-SD-01', 'B19-SD-02', 'B19-DS-01', 'B19-AI-01', 'B19-CS-01', 'B19-RO-01',
              'M22-SE-01', 'M22-SE-02', 'M22-DS-01', 'M22-RO-01', 'M22-TE-01']
    slots = db.slot.find_many(where={
        "start_time": {
            "gte": "2023-02-27T01:00:00.000Z"
        },
        "end_time": {
            "lte": "2023-03-04T20:00:00.000Z",
        },
        "group_id": {
            "not": None
        },
        "specific_group": {
            "in": groups
        }
    })
    new_slots = list(map(lambda x: {
        "instructor_name": x.instructor_name,
        "room_number": x.room_number,
        "start_time": arrow.get(x.start_time).to(TIMEZONE).shift(weeks=+1).isoformat(),
        "end_time": arrow.get(x.end_time).to(TIMEZONE).shift(weeks=+1).isoformat(),
        "course_id": x.course_id,
        "course_name": x.course_name,
        "type": x.type,
        "group_id": x.group_id,
        "specific_group": x.specific_group,
    }, slots))
    db.slot.create_many(data=new_slots)
    return {"message": "successful"}


@router.get('/create_slot')
def create_slot():
    groups = ['B22-CS-01', 'B22-CS-02', 'B22-CS-03', 'B22-CS-04', 'B22-CS-05',
              'B22-CS-06', 'B22-DSAI-01', 'B22-DSAI-02', 'B22-DSAI-03', 'B22-DSAI-04',
              'SD21-01', 'SD21-02', 'SD21-03', 'CS21-01', 'DS21-01', 'DS21-02', 'AAI21-01', 'RO21-01',
              'B20-SD-01', 'B20-SD-02', 'B20-CS', 'B20-AI', 'B20-DS', 'B20-RO',
              'B19-SD-01', 'B19-SD-02', 'B19-DS-01', 'B19-AI-01', 'B19-CS-01', 'B19-RO-01',
              'M22-SE-01', 'M22-SE-02', 'M22-DS-01', 'M22-RO-01', 'M22-TE-01']

    selected_groups = [
        {"specific_group": 'B19-SD-01', "group_id": "cldhhy443001cmzwcdjoqazxa"},
        {"specific_group": 'B19-SD-02', "group_id": "cldhhy4qy001emzwcim4em7ku"},
        {"specific_group": 'B19-DS-01', "group_id": "cldhhy5dt001gmzwcjqgtye4o"},
        {"specific_group": 'B19-AI-01', "group_id": "cldhhy61a001imzwcvvg74fe4"},
        {"specific_group": 'B19-CS-01', "group_id": "cldhhy6pj001kmzwc9monseu0"},
        {"specific_group": 'B19-RO-01', "group_id": "cldhhy7em001mmzwcn233fhin"},
    ]
    start_time = "2023-03-11T14:50:00+03:00"
    end_time = "2023-03-11T16:20:00+03:00"
    instructor_name = "Andrei Anisimov"
    room_number = "105"
    course_id = "cldhhzqrt003emzwcppqyu41u"
    course_name = "Theoretical Sports - Physiology"
    type = "LEC"

    new_slots = list(map(lambda x: {
        "instructor_name": instructor_name,
        "room_number": room_number,
        "start_time": arrow.get(start_time).isoformat(),
        "end_time": arrow.get(end_time).isoformat(),
        "course_id": course_id,
        "course_name": course_name,
        "type": type,
        "group_id": x["group_id"],
        "specific_group": x["specific_group"],
    }, selected_groups))
    print(new_slots)
    db.slot.create_many(data=new_slots)
    return {"message": "successful"}


@router.get('/delete_specific_slot')
def delete_specific_slot():
    groups = ['B22-CS-01', 'B22-CS-02', 'B22-CS-03', 'B22-CS-04', 'B22-CS-05',
              'B22-CS-06', 'B22-DSAI-01', 'B22-DSAI-02', 'B22-DSAI-03', 'B22-DSAI-04',
              'SD21-01', 'SD21-02', 'SD21-03', 'CS21-01', 'DS21-01', 'DS21-02', 'AAI21-01', 'RO21-01',
              'B20-SD-01', 'B20-SD-02', 'B20-CS', 'B20-AI', 'B20-DS', 'B20-RO',
              'B19-SD-01', 'B19-SD-02', 'B19-DS-01', 'B19-AI-01', 'B19-CS-01', 'B19-RO-01',
              'M22-SE-01', 'M22-SE-02', 'M22-DS-01', 'M22-RO-01', 'M22-TE-01']

    selected_groups = [{"specific_group": 'M22-SE-01', "group_id": "cldhhy81g001omzwcez2x4byx"},
                       {"specific_group": 'M22-SE-02', "group_id": "cldhhy8pg001qmzwccuyc547x"}]
    start_time = "2023-02-27T01:40:00+03:00"
    end_time = "2023-03-04T20:10:00+03:00"

    slots = db.slot.delete_many(where={
        "group_id": {
            "in": ["cldhhy443001cmzwcdjoqazxa", "cldhhy4qy001emzwcim4em7ku", "cldhhy5dt001gmzwcjqgtye4o", "cldhhy61a001imzwcvvg74fe4", "cldhhy6pj001kmzwc9monseu0", "cldhhy7em001mmzwcn233fhin"]
        },
        "start_time": {
            "gte": start_time,
        },
        "end_time": {
            "lte": end_time,
        },
        "course_id": {
            "in": ["cldhhzqrt003emzwcppqyu41u"]
        }})
    print(slots)
    return {"message": "successful"}


@router.get('/seed_course')
def seed_course():
    # SNE_COURSES, MAIN_COURSES, ELECTIVE_COURSES
    for course in ELECTIVE_COURSES:
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
                "description": course["description"],
                "is_elective": course["is_elective"],
                # "groups": {
                #     "connect": course_groups_ids
                # }
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


@router.get('/seed_russian_course')
def seed_russian_course():
    for course in RFL_COURSES:
        # create course and connect groups by id
        db.course.create(data={
            "description": course["description"],
            "is_elective": course["is_elective"],
            "short_name": course["short_name"],
        })
    return {"message": "successful"}


@router.get('/seed_slot')
def seed_slot():
    # MAIN_SLOTS, SNE_SLOTS, RFL_SLOTS
    db.slot.create_many(data=RFL_SLOTS)
    return {"message": "successful"}


@router.get('/duplicate_main_course_slots')
def duplicate_main_course_slots():
    new_slots = db.slot.find_many(where={
        "specific_group": {
            "not_in": ["M22-SNE-01", "B20", "B19", "M22"]
        }})
    new_slots = list(map(lambda x: {
        "instructor_name": x.instructor_name,
        "room_number": x.room_number,
        "start_time": arrow.get(x.start_time).to(TIMEZONE).shift(weeks=+1).isoformat(),
        "end_time": arrow.get(x.end_time).to(TIMEZONE).shift(weeks=+1).isoformat(),
        "course_id": x.course_id,
        "course_name": x.course_name,
        "type": x.type,
        "group_id": x.group_id,
        "specific_group": x.specific_group,
    }, new_slots))
    # db.slot.create_many(data=new_slots)

    for _ in range(3, 10):
        new_slots = list(map(lambda x: {
            "instructor_name": x["instructor_name"],
            "room_number": x["room_number"],
            "start_time": arrow.get(x["start_time"]).to(TIMEZONE).shift(weeks=+1).isoformat(),
            "end_time": arrow.get(x["end_time"]).to(TIMEZONE).shift(weeks=+1).isoformat(),
            "course_id": x["course_id"],
            "course_name": x["course_name"],
            "type": x["type"],
            "group_id": x["group_id"],
            "specific_group": x["specific_group"],
        }, new_slots))
        # db.slot.create_many(data=new_slots)
    return {"message": "successful"}


@router.get('/drop_slot')
def drop_slot():
    db.slot.delete_many()
    return {"message": "successful"}


@router.get('/quick_course_fix')
def quick_course_fix():
    slots = db.slot.find_many(include={"course": True})
    print(slots[0])
    for slot in slots:
        if not slot.course_name:
            db.slot.update(where={"id": slot.id}, data={
                "course_name": slot.course.description if slot.course else ""})
    return {"message": "successful"}


@router.get('/connect_slot_course_group')
def connect_slot_course_group():
    slots = db.slot.find_many(where={"specific_group": {
        "in": ["RFL-INTER", "RFL-BEGIN-M1", "RFL-BEGIN-M2", "RFL-BEGIN-BACH"]}})
    for slot in slots:
        course = db.course.find_first(
            where={"short_name": slot.specific_group})

        if course:
            db.slot.update(data={
                "course": {
                    "connect": {
                        "id": course.id
                    }
                }
            }, where={"id": slot.id})
    return {"message": "successful"}


@router.get('/course_abbrevation_validgroup')
def fill_course_abbrevation():
    courses = db.course.find_many(
        where={"is_elective": True},
        include={"time_slots": True})
    final_names = dict(MS_ELECTIVE_NAMES)
    final_names.update(BS4_ELECTIVE_NAMES)
    final_names.update(BS3_ELECTIVE_NAMES)
    for course in courses:
        if course.time_slots:
            valid_group = course.time_slots[0].specific_group
            db.course.update(data={
                "valid_group": valid_group,
                "short_name": final_names[course.description][0],
            }, where={"id": course.id})
    return {"message": "successful"}


@router.get('/add_specific_slots')
def add_specific_slots():
    groups = [
        {"name": 'SD21-01', "id": "cldhhxuhh000kmzwca922bvxd"},
        {"name": 'SD21-02', "id": "cldhhxv4d000mmzwc16ukq2tt"},
        {"name": 'SD21-03', "id": "cldhhxvt3000omzwcvy16sv9e"},
        {"name": 'CS21-01', "id": "cldhhxvt3000omzwcvy16sv9e"},
        {"name": 'DS21-01', "id": "cldhhxx3m000smzwczt5sep42"},
        {"name": 'DS21-02', "id": "cldhhxxto000umzwcmvfekkym"},
        {"name": 'AAI21-01', "id": "cldhhxygj000wmzwcy2mfv253"},]
    for group in groups:
        new_slot = {
            "instructor_name": "Darko Bozhinoski",
            "room_number": "105",
            "start_time": "2023-02-24T08:00:00.000Z",
            "end_time": "2023-02-24T09:30:00.000Z",
            "course_id": "cldhhz421002kmzwcvgc87luy",
            "course_name": "Databases",
            "type": "LEC",
            "group_id": group["id"],
            "specific_group": group["name"],
        }
        db.slot.create(data=new_slot)
    return {"message": "successful"}
