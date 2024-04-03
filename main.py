from modules.line_handler import(
  handle_signature,
  events_handler,
  image_map
)

from modules.google_drive import get_drive

from dotenv import load_dotenv;load_dotenv()
from fastapi import Request, FastAPI
from fastapi.responses import FileResponse
from starlette.responses import StreamingResponse
import io

app = FastAPI()
favicon_path = './public/favicon.ico'

@app.get("/")
def read_root():
  return {"message": "bot server start"}

@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
  return FileResponse(favicon_path)

@app.post("/callback")
async def handle_callback(request: Request):
  signature = request.headers['X-Line-Signature']
  body = await request.body()
  body = body.decode()

  events = handle_signature(body, signature)
  await events_handler(events)

@app.get("/picture/{user_id}")
async def get_picture(user_id: str):
  print(image_map.keys())
  binary_data = image_map[user_id]
  return StreamingResponse(io.BytesIO(binary_data), media_type="image/jpg")

