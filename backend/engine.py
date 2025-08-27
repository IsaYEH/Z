from lunar_python import Solar, Lunar
from typing import Dict, Any, List

PALACES = [
    "命宮","兄弟宮","夫妻宮","子女宮","財帛宮","疾厄宮",
    "遷移宮","交友宮","官祿宮","田宅宮","福德宮","父母宮"
]

STEMS = ["Jia","Yi","Bing","Ding","Wu","Ji","Geng","Xin","Ren","Gui"]

def ganzhi_year_stem(year: int) -> str:
    return STEMS[(year - 4) % 10]

def build_base_palaces() -> Dict[str, list]:
    return {p: [] for p in PALACES}

def locate_ming_shen(y:int,m:int,d:int,h:int):
    """
    命宮：以農曆月支 + 時辰來推算
    身宮：以年支 + 出生時辰來推算（簡化）
    """
    lunar = Solar.fromYmdHms(y,m,d,h,0,0).getLunar()
    month = lunar.getMonth()  # 農曆月
    hourIndex = lunar.getTimeZhiIndex()  # 0=子時,1=丑, ...

    ming_idx = (month + hourIndex - 1) % 12
    shen_idx = (lunar.getYearZhiIndex() + hourIndex) % 12
    return PALACES[ming_idx], PALACES[shen_idx]

def demo_major_stars(ming: str) -> Dict[str, list]:
    stars = build_base_palaces()
    ring = PALACES
    i = ring.index(ming)
    stars[ming].append({"name":"紫微","type":"major"})
    stars[ring[(i+1)%12]].append({"name":"天機","type":"major"})
    stars[ring[(i+2)%12]].append({"name":"太陽","type":"major"})
    stars[ring[(i+3)%12]].append({"name":"武曲","type":"major"})
    stars[ring[(i+4)%12]].append({"name":"天同","type":"major"})
    stars[ring[(i+5)%12]].append({"name":"廉貞","type":"major"})
    stars[ring[(i+6)%12]].append({"name":"天府","type":"major"})
    stars[ring[(i+7)%12]].append({"name":"太陰","type":"major"})
    stars[ring[(i+8)%12]].append({"name":"貪狼","type":"major"})
    stars[ring[(i+9)%12]].append({"name":"巨門","type":"major"})
    stars[ring[(i+10)%12]].append({"name":"天相","type":"major"})
    stars[ring[(i+11)%12]].append({"name":"天梁","type":"major"})
    return stars

def compute_chart(date_str: str, time_str: str, place: str):
    y, m, d = [int(x) for x in date_str.split("-")]
    hh, mm = [int(x) for x in time_str.split(":")]
    year_sky = ganzhi_year_stem(y)

    ming, shen = locate_ming_shen(y,m,d,hh)
    stars = demo_major_stars(ming)

    return {
        "meta": {"birth":{"date":date_str,"time":time_str,"place":place,"yearSky":year_sky}},
        "natal": {
            "lifePalace": ming,
            "bodyPalace": shen,
            "stars": stars
        }
    }
