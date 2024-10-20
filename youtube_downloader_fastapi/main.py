import os
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import yt_dlp

app = FastAPI()
templates = Jinja2Templates(directory="templates")

download_path = os.path.join(os.getcwd(), "downloads")
os.makedirs(download_path, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/download", response_class=HTMLResponse)
async def download_video(request: Request, url: str = Form(...)):
    try:
        ydl_opts = {
            'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s')  
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return templates.TemplateResponse("success.html", {"request": request, "message": "Video downloaded successfully!"})
    
    except Exception as e:
        return templates.TemplateResponse("error.html", {"request": request, "error": str(e)})
