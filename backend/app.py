from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import yaml, os

# ⚠️ 修正這行：相對匯入 engine
from .engine import compute_chart

app = FastAPI()

# 載入四化規則
RULE_FILE = os.path.join(os.path.dirname(__file__), "data", "rules", "wenmo-1.0.yaml")
with open(RULE_FILE, "r", encoding="utf-8") as f:
    RULES = yaml.safe_load(f)

BY_STEM_TABLE = RULES["transforms"]["by_stem_table"]

class ChartRequest(BaseModel):
    date: str
    time: str
    place: str
    yearSky: Optional[str] = None
    lat: Optional[float] = 25.033
    lon: Optional[float] = 121.565

STORE = {}

@app.post("/api/charts")
def create_chart(payload: ChartRequest):
    chart = compute_chart(payload.date, payload.time, payload.place)
    # 年干四化
    sky = chart["meta"]["birth"]["yearSky"]
    chart["natal"]["transforms"] = BY_STEM_TABLE.get(sky, {})
    chart["id"] = f"demo-{payload.date}-{payload.time}-{payload.place}"
    chart["meta"]["birth"]["lat"] = payload.lat
    chart["meta"]["birth"]["lon"] = payload.lon
    STORE[chart["id"]] = chart
    return chart

@app.get("/")
def root():
    return {"msg": "Ziwei API is running"}
