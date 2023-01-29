from threading import Thread
from fastapi import FastAPI
from starlette.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from app.db import db
from app.telegram.core.handlers import bot
# import sys
# print(sys.executable)
# print(sys.path)

from app.version import router as final_router





app = FastAPI(
    title="ScheduleAPI",
    description="Seemless scheduling",
    version="1.0",
)

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,
    allow_credentials= True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(final_router, prefix="/api/v1")


@app.on_event("startup")
async def startup():
    print(f'db connected...')
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    print(f'db disconnected...')
    await db.disconnect()

@app.get('/any')
async def something():
    user = await db.user.create(
        {
            'id': '54545612',
            'handle': 'yuuityi',
        }
    )
    print(f'created user: {user.json(indent=2, sort_keys=True)}')

    found = await db.user.find_unique(where={'id': user.id})
    assert found is not None
    print(f'found post: {found.json(indent=2, sort_keys=True)}')


@app.get("/", response_class=HTMLResponse)
def index():
    return """
    <!Doctype html>
    <html>
        <body>
            <h1>ScheduleAPI</h1>
            <p>Everything setup perfectly</p>
            <div class="btn-group">
                <a href="/docs"><button>SwaggerUI</button></a>
                <a href="/redoc"><button>Redoc</button></a>
            </div>
        </body>
    </html>
    """


def polling_telegram_bot_commands():
    print("Bot begins polling")
    bot.polling(none_stop=False, timeout=50)


polling_thread = Thread(target=polling_telegram_bot_commands, daemon=True)
polling_thread.start()

