from fastapi import FastAPI
from starlette.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from app.db import db
from app.telegram.init import setup_telegram_bot
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
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(final_router, prefix="/api/v1")


@app.on_event("startup")
def startup():
    print(f'db connected...')
    db.connect()

    # Running telegram bot
    setup_telegram_bot()


@app.on_event("shutdown")
def shutdown():
    print(f'db disconnected...')
    db.disconnect()



@app.get("/", response_class=HTMLResponse, include_in_schema=False)
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


