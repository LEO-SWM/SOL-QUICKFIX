from fastapi import FastAPI, UploadFile
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles
from db_interface import DBInterface

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

db_interface = DBInterface("sqlite:///your_database.db")


@app.on_event("startup")
def startup():
    db_interface.initialize_database()


@app.get("/")
async def query():
    return FileResponse("static/html/index.html")


@app.get("/students/{student}/")
async def query_student(student):
    return db_interface.get_student_infos(student).to_dict(orient="records")


@app.get("/panels/{panel}/")
async def query_serial_number(panel):
    return db_interface.get_panel_info(panel).to_dict(orient="records")


@app.get("/mixed/{query}/")
async def query_mixed(query):
    return db_interface.get_mixed_infos(query).to_dict(orient="records")


@app.get("/students/{student}/download")
async def download_student(student):
    df = db_interface.get_student_infos(student)
    return db_interface.download_df(df, student)


@app.get("/panels/{panel}/download")
async def download_panel(panel):
    df = db_interface.get_panel_info(panel)
    return db_interface.download_df(df, panel)


@app.get("/mixed/{query}/download")
async def download_mixed(query):
    df = db_interface.get_mixed_infos(query)
    return db_interface.download_df(df, query)


@app.post("/upload_orders/")
async def upload_orders(file: UploadFile):
    db_interface.import_order_infos(file.file)


@app.post("/upload_flash/")
async def upload_flash(file: UploadFile):
    db_interface.import_flash_infos(file.file)
