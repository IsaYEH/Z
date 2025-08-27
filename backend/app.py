from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
import os, json, yaml

BASE_DIR = os.path.dirname(__file__)
FRONTEND_DIR = os.path.join(os.path.dirname(BASE_DIR), "frontend")
DATA_DIR = os.path.join(BASE_DIR, "data")

with open(os.path.join(DATA_DIR, "sample_chart.json"), "r", encoding="utf-8") as f:
    SAMPLE = json.load(f)
with open(os.path.join(DATA_DIR, "rules", "wenmo-1.0.yaml"), "r", encoding="utf-8") as f:
    RULES = yaml.safe_load(f)

BY_STEM_TABLE = RULES.get("transforms",{}).get("by_stem_table",{})

STORE = {SAMPLE["id"]: SAMPLE}

class ChartRequest(BaseModel):
    date: str
    time: str
    tz: str = "+08:00"
    place: str = "台北"
    lat: float = 25.033
    lon: float = 121.565
    ruleset: str = "wenmo-1.0"
    yearSky: str = "Jia"

app = FastAPI(title="Ziwei Render API")

app.mount("/assets", StaticFiles(directory=FRONTEND_DIR), name="assets")

@app.get("/")
def index():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

@app.post("/api/charts")
def create_chart(payload: ChartRequest):
    chart = json.loads(json.dumps(SAMPLE,ensure_ascii=False))
    chart["id"]=f"demo-{payload.date}-{payload.time}-{payload.place}"
    chart["meta"]["birth"]={"date":payload.date,"time":payload.time,"place":payload.place,"lat":payload.lat,"lon":payload.lon,"yearSky":payload.yearSky}
    chart["natal"]["transforms"]=BY_STEM_TABLE.get(payload.yearSky,{})
    STORE[chart["id"]]=chart
    return chart
