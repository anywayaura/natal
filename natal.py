import swisseph as swe
from datetime import datetime, timezone, timedelta
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz

from varga_algorithms import calculate_varga

# ---------------------------------------------------------------
# Константы
# ---------------------------------------------------------------

PLANET_KEYS = ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Rahu", "Ketu"]

PLANET_IDS = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mercury": swe.MERCURY,
    "Venus": swe.VENUS,
    "Mars": swe.MARS,
    "Jupiter": swe.JUPITER,
    "Saturn": swe.SATURN,
    "Rahu": swe.MEAN_NODE,
}

SIGN_NAMES = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]

SIGN_NAMES_RU = [
    "Овен ♈", "Телец ♉", "Близнецы ♊", "Рак ♋",
    "Лев ♌", "Дева ♍", "Весы ♎", "Скорпион ♏",
    "Стрелец ♐", "Козерог ♑", "Водолей ♒", "Рыбы ♓",
]

NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni",
    "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha",
    "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha",
    "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada",
    "Uttara Bhadrapada", "Revati",
]

NAKSHATRA_NAMES_RU = [
    "Ашвини", "Бхарани", "Криттика", "Рохини", "Мригашира", "Ардра",
    "Пунарвасу", "Пушья", "Ашлеша", "Магха", "Пурва-пхалгуни",
    "Уттара-пхалгуни", "Хаста", "Читра", "Свати", "Вишакха",
    "Анурадха", "Джьештха", "Мула", "Пурва-ашадха", "Уттара-ашадха",
    "Шравана", "Дхаништха", "Шатабхиша", "Пурва-бхадрапада",
    "Уттара-бхадрапада", "Ревати",
]

NAKSHATRA_LORDS = [
    "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury",
]

NAKSHATRA_LORDS_RU = [
    "Кету", "Венера", "Солнце", "Луна", "Марс", "Раху", "Юпитер", "Сатурн", "Меркурий",
]

DASHA_LENGTHS = {
    "Ketu": 7, "Venus": 20, "Sun": 6, "Moon": 10, "Mars": 7,
    "Rahu": 18, "Jupiter": 16, "Saturn": 19, "Mercury": 17,
}

NAKSHATRA_LEN = 13.333333333333334

VARGAS = [
    ("D1 — Раши (Rasi)", 1, "Тело, общая судьба"),
    ("D2 — Хора (Hora)", 2, "Богатство, финансы"),
    ("D3 — Дреккана (Drekkana)", 3, "Братья/сёстры, смелость"),
    ("D4 — Чатуртхамша (Chaturthamsa)", 4, "Недвижимость, удача"),
    ("D5 — Панчамша (Panchamsa)", 5, "Власть, слава, знания"),
    ("D7 — Саптамша (Saptamsa)", 7, "Дети, творчество"),
    ("D8 — Аштамша (Ashtamsa)", 8, "Препятствия, неожиданности"),
    ("D9 — Навамша (Navamsa)", 9, "Брак, партнёр, дхарма"),
    ("D10 — Дашамша (Dasamsa)", 10, "Карьера, профессия"),
    ("D12 — Двадашамша (Dwadasamsa)", 12, "Родители, наследственность"),
    ("D16 — Шодашамша (Shodasamsa)", 16, "Комфорт, транспорт"),
    ("D20 — Вимшамша (Vimsamsa)", 20, "Духовность, аскетизм"),
    ("D24 — Чатурвимшамша (Chaturvimsamsa)", 24, "Образование, знания"),
    ("D27 — Саптавимшамша (Saptavimsamsa)", 27, "Сильные стороны"),
    ("D30 — Тримшамша (Trimsamsa)", 30, "Негатив, трудности"),
    ("D40 — Кхаведамша (Khavedamsa)", 40, "Заслуги, благосостояние"),
    ("D45 — Акшаведамша (Akshavedamsa)", 45, "Поведение, мораль"),
    ("D60 — Шаштьямша (Shashtyamsa)", 60, "Кармический баланс"),
]

# ---------------------------------------------------------------
# Геокодирование и часовой пояс
# ---------------------------------------------------------------

def get_coords(city_name: str) -> tuple[float, float] | None:
    geolocator = Nominatim(user_agent="natal_chart_bot")
    location = geolocator.geocode(city_name)
    if location is None:
        return None
    return location.latitude, location.longitude


def get_timezone_name(lat: float, lon: float) -> str | None:
    tf = TimezoneFinder()
    return tf.timezone_at(lat=lat, lng=lon)


# ---------------------------------------------------------------
# Основной расчёт
# ---------------------------------------------------------------

def calculate(city: str, date_str: str, time_str: str, lat: float | None = None, lon: float | None = None) -> dict:
    """Полный расчёт натальной карты.

    Если lat/lon не переданы — определяет по названию города.
    """
    result = {}

    # Парсим дату/время
    birth_local = datetime.strptime(f"{date_str} {time_str}", "%d.%m.%Y %H:%M")
    result["birth_local"] = birth_local

    # Координаты
    if lat is not None and lon is not None:
        result["lat"] = lat
        result["lon"] = lon
        result["city"] = city
    else:
        coords = get_coords(city)
        if coords is None:
            raise ValueError(f"Не удалось найти город '{city}'")
        result["lat"] = coords[0]
        result["lon"] = coords[1]
        result["city"] = city

    lat, lon = result["lat"], result["lon"]

    # Часовой пояс
    tz_name = get_timezone_name(lat, lon)
    if tz_name is None:
        tz = timezone.utc
        tz_name = "UTC"
    else:
        tz = pytz.timezone(tz_name)
    result["tz_name"] = tz_name

    local_tz = tz.localize(birth_local, is_dst=None)
    utc_dt = local_tz.astimezone(pytz.utc)
    result["utc_dt"] = utc_dt

    # Юлианский день
    jd = swe.julday(
        utc_dt.year, utc_dt.month, utc_dt.day,
        utc_dt.hour + utc_dt.minute / 60.0 + utc_dt.second / 3600.0,
    )
    result["jd"] = jd

    # Эфемериды
    swe.set_ephe_path(None)
    swe.set_sid_mode(swe.SIDM_LAHIRI)

    # D1 позиции планет
    d1 = {}
    for name in PLANET_KEYS:
        if name == "Ketu":
            res = swe.calc_ut(jd, swe.MEAN_NODE, swe.FLG_SIDEREAL)
            pos = (res[0][0] + 180) % 360
        else:
            res = swe.calc_ut(jd, PLANET_IDS[name], swe.FLG_SIDEREAL)
            pos = res[0][0]
        d1[name] = pos
    result["d1_positions"] = d1

    # Лагна (сидерические дома)
    cusps, ascmc = swe.houses_ex(jd, lat, lon, b"P", swe.FLG_SIDEREAL)
    lagna_abs = ascmc[0]
    result["lagna_abs"] = lagna_abs
    result["lagna_sign"] = int(lagna_abs // 30)
    result["lagna_degree"] = lagna_abs % 30

    # Накшатра Луны
    moon_abs = d1["Moon"]
    nak_idx = int(moon_abs // NAKSHATRA_LEN)
    nak_deg = moon_abs % NAKSHATRA_LEN
    pada = int(nak_deg // (NAKSHATRA_LEN / 4)) + 1
    lord_idx = nak_idx % 9
    moon_lord = NAKSHATRA_LORDS[lord_idx]
    result["nakshatra_index"] = nak_idx
    result["nakshatra_degree"] = nak_deg
    result["pada"] = pada
    result["moon_lord"] = moon_lord

    # Вимшоттари-даша
    remaining_deg = NAKSHATRA_LEN - nak_deg
    ratio = remaining_deg / NAKSHATRA_LEN
    balance_years = ratio * DASHA_LENGTHS[moon_lord]
    result["balance_years"] = balance_years

    seq = []
    lords_order = list(NAKSHATRA_LORDS)
    start_idx = lords_order.index(moon_lord)
    current_date_calc = birth_local + timedelta(days=balance_years * 365.25)
    seq.append((moon_lord, birth_local, current_date_calc))
    idx = (start_idx + 1) % 9
    while current_date_calc.year < 2100:
        lord = lords_order[idx]
        years = DASHA_LENGTHS[lord]
        start_d = current_date_calc
        end_d = current_date_calc + timedelta(days=years * 365.25)
        seq.append((lord, start_d, end_d))
        current_date_calc = end_d
        idx = (idx + 1) % 9
    result["dasha_sequence"] = seq

    # -------------------------------------------------------------
    # Варги
    # -------------------------------------------------------------
    # ВАЖНО (фикс бага Раху/Кету):
    # Раньше Кету брался уже готовым из d1 (Rahu + 180) и просто
    # умножался на divisor вместе со всеми планетами:
    #     div_long = (abs_pos * divisor) % 360
    # Для ЧЁТНЫХ divisor это давало 180*divisor % 360 == 0, то есть
    # варговая позиция Кету схлопывалась в позицию Раху (D2, D4, D8,
    # D10, D12, D16, D20, D24, D30, D40, D60 — все чётные, все были
    # затронуты). Для нечётных divisor 180*divisor % 360 == 180,
    # поэтому там (D1, D3, D5, D7, D9, D27, D45) узлы случайно
    # оставались корректными — оппозиция сохранялась.
    #
    # Правильный порядок: сначала считаем варговую позицию РАХУ,
    # а варговую позицию КЕТУ получаем как оппозицию УЖЕ ПОСЛЕ
    # деления на varga, а не до него.

    all_positions = dict(d1)
    all_positions["Lagna"] = lagna_abs

    vargas_result = []
    for title, divisor, desc in VARGAS:
        chart = {}
        for name, abs_pos in all_positions.items():
            s, deg = calculate_varga(divisor, abs_pos)
            div_long = s * 30 + deg
            chart[name] = {"sign_num": s, "degree": deg, "absolute": div_long}

        vargas_result.append({
            "title": title,
            "divisor": divisor,
            "description": desc,
            "chart": chart,
        })
    result["vargas"] = vargas_result

    return result


# ---------------------------------------------------------------
# Форматирование для вывода
# ---------------------------------------------------------------

def format_planet_line(name: str, sign_num: int, degree: float, ru: bool = True) -> str:
    if name == "Lagna":
        label = "🌞 Лагна" if ru else "Lagna"
    else:
        planet_emoji = {
            "Sun": "☀", "Moon": "☽", "Mercury": "☿", "Venus": "♀",
            "Mars": "♂", "Jupiter": "♃", "Saturn": "♄", "Rahu": "🌑", "Ketu": "🌘",
            "Lagna": "🌞",
        }
        label = f"{planet_emoji.get(name, '')} {name}"
    signs = SIGN_NAMES_RU if ru else SIGN_NAMES
    return f"  {label:<16} {signs[sign_num]:<12} {degree:>6.2f}°"


def format_result(result: dict, ru: bool = True) -> str:
    lines = []
    lines.append("🔮 **Натальная карта (Джйотиш)**")
    lines.append("")
    lines.append(f"📍 Город: {result['city']}")
    lines.append(f"🕐 Локальное время: {result['birth_local'].strftime('%d.%m.%Y %H:%M')}")
    lines.append(f"🌍 UTC: {result['utc_dt'].strftime('%d.%m.%Y %H:%M:%S')}")
    lines.append(f"🗺 Часовой пояс: {result['tz_name']}")
    lines.append(f"📌 Координаты: {result['lat']:.4f}, {result['lon']:.4f}")
    lines.append("")
    lines.append("**── D1 — Раши-чакра ──**")
    lines.append("")

    lines.append(format_planet_line("Lagna", result["lagna_sign"], result["lagna_degree"], ru))
    for name in PLANET_KEYS:
        pos = result["d1_positions"][name]
        s = int(pos // 30)
        d = pos % 30
        lines.append(format_planet_line(name, s, d, ru))
    lines.append("")

    nak_idx = result["nakshatra_index"]
    nak_name = NAKSHATRA_NAMES_RU[nak_idx] if ru else NAKSHATRAS[nak_idx]
    lord_ru = NAKSHATRA_LORDS_RU[NAKSHATRA_LORDS.index(result["moon_lord"])] if ru else result["moon_lord"]
    lines.append(f"🌙 Накшатра Луны: {nak_name}, Пада: {result['pada']}")
    lines.append(f"👑 Владыка накшатры: {lord_ru}")
    lines.append(f"📅 Родовая даша: {lord_ru}, остаток: {result['balance_years']:.2f} лет")
    lines.append("")

    lines.append("**── Вимшоттари-даша (Махадаша) ──**")
    for lord, start, end in result["dasha_sequence"]:
        if start.year <= 2030:
            lord_label = NAKSHATRA_LORDS_RU[NAKSHATRA_LORDS.index(lord)] if ru else lord
            lines.append(f"  {lord_label:<12} {start.strftime('%d.%m.%Y')} — {end.strftime('%d.%m.%Y')}")
    lines.append("")

    lines.append("**── Варги (Divisional Charts) ──**")
    for v in result["vargas"]:
        lines.append("")
        lines.append(f"**{v['title']}** — {v['description']}")
        for name in ["Lagna"] + PLANET_KEYS:
            d = v["chart"][name]
            lines.append(format_planet_line(name, d["sign_num"], d["degree"], ru))

    return "\n".join(lines)


def format_short_result(result: dict, ru: bool = True) -> str:
    """Короткий вывод — только D1 и даши."""
    lines = []
    lines.append("🔮 **Натальная карта**")
    lines.append(f"📍 {result['city']}, {result['birth_local'].strftime('%d.%m.%Y %H:%M')}")
    lines.append("")

    lines.append(format_planet_line("Lagna", result["lagna_sign"], result["lagna_degree"], ru))
    for name in PLANET_KEYS:
        pos = result["d1_positions"][name]
        s = int(pos // 30)
        d = pos % 30
        lines.append(format_planet_line(name, s, d, ru))
    lines.append("")

    nak_idx = result["nakshatra_index"]
    nak_name = NAKSHATRA_NAMES_RU[nak_idx] if ru else NAKSHATRAS[nak_idx]
    lord_ru = NAKSHATRA_LORDS_RU[NAKSHATRA_LORDS.index(result["moon_lord"])] if ru else result["moon_lord"]
    lines.append(f"🌙 Накшатра: {nak_name}, Пада: {result['pada']}")
    lines.append(f"👑 Владыка: {lord_ru}")
    lines.append(f"📅 Баланс даши: {result['balance_years']:.2f} лет")
    lines.append("")

    lines.append("**Даши до 2030:**")
    for lord, start, end in result["dasha_sequence"]:
        if start.year <= 2030:
            lord_label = NAKSHATRA_LORDS_RU[NAKSHATRA_LORDS.index(lord)] if ru else lord
            lines.append(f"  {lord_label:<12} {start.strftime('%d.%m.%Y')} — {end.strftime('%d.%m.%Y')}")

    return "\n".join(lines)
