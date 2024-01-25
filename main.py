from fastapi import FastAPI, UploadFile, HTTPException
from starlette.responses import FileResponse, StreamingResponse
from starlette.staticfiles import StaticFiles
import io
from transfer import *
from querier import Querier

# Create a FastAPI app
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
transfer = Transfer(
    ["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"],
    "sqlite:///your_database.db",
    "flash",
    "orders",
)

querier = Querier("sqlite:///your_database.db", "flash", "orders")


# Route to get entries based on a SQL query
@app.get("/users/{user}/")
async def query_user(user):
    return querier.get_user_infos(user).to_dict(orient="records")


@app.get("/panels/{panel}/")
async def query_serial_number(panel):
    return querier.get_panel_info(panel).to_dict(orient="records")


@app.get("/download_user/{user}/")
async def download_user(user):
    df = querier.get_user_infos(user)
    return transfer.download_df(df, user)


@app.get("/download_panel/{panel}/")
async def download_panel(panel):
    df = querier.get_panel_info(panel)
    return transfer.download_df(df, panel)


@app.get("/query/")
async def query():
    return FileResponse("static/index.html")


@app.post("/upload_orders/")
async def upload_orders(file: UploadFile):
    transfer.import_order_infos(file.file)


@app.post("/upload_flash/")
async def upload_flash(file: UploadFile):
    transfer.import_flash_infos(file.file)
