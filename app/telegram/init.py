from app.telegram.core.handlers import attach_core_module, compose_attached_modules
from app.telegram.schedule.handlers import attach_schedule_module
from app.telegram.remind.handlers import attach_remind_module
from app.telegram.elective.handlers import attach_elective_module
from app.telegram.admin.handlers import attach_admin_module


def setup_telegram_bot():
    # attach required modules
    attach_core_module()
    attach_schedule_module()
    attach_remind_module()
    attach_elective_module()
    attach_admin_module()
    

    # compose modules and start listening
    compose_attached_modules()