from fastapi import FastAPI, UploadFile
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles
from db_interface import DBInterface

# Create a FastAPI app
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

db_interface = DBInterface("sqlite:///your_database.db")


@app.on_event("startup")
def startup():
    db_interface.initialize_database()


@app.get("/")
async def query():
    return FileResponse("static/index.html")


@app.get("/users/{user}/")
async def query_user(user):
    return db_interface.get_user_infos(user).to_dict(orient="records")


@app.get("/panels/{panel}/")
async def query_serial_number(panel):
    return db_interface.get_panel_info(panel).to_dict(orient="records")


@app.get("/users/{user}/download")
async def download_user(user):
    df = db_interface.get_user_infos(user)
    return db_interface.download_df(df, user)


@app.get("/panels/{panel}/download")
async def download_panel(panel):
    df = db_interface.get_panel_info(panel)
    return db_interface.download_df(df, panel)


@app.post("/upload_orders/")
async def upload_orders(file: UploadFile):
    db_interface.import_order_infos(file.file)


@app.post("/upload_flash/")
async def upload_flash(file: UploadFile):
    db_interface.import_flash_infos(file.file)
