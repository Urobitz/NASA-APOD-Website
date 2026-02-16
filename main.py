from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import requests

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request, "index.html")

@app.post("/submit", response_class=HTMLResponse)
def get_info(request:Request, api_key: str=Form(), user_date: str=Form()):
    print(api_key)
    print(user_date)

    url = "https://api.nasa.gov/planetary/apod"

    params ={

        "api_key": api_key,
        "date" : user_date
    }

    r = requests.get(url,params=params)

    print(r.json())

    data = r.json()["explanation"]
    image = r.json()["hdurl"]

    return templates.TemplateResponse(

        "sentinfor.html",

        {
            "request" : request,
            "information" : data,
            "image" : image
        }

    )


