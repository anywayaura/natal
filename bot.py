import logging
import os
import io
import re
from datetime import datetime
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from natal import (
    calculate,
    PLANET_KEYS,
    SIGN_NAMES_RU,
    NAKSHATRA_NAMES_RU,
    NAKSHATRA_LORDS,
    NAKSHATRA_LORDS_RU,
)
from varga_algorithms import calculate_varga, SIGN_NAMES

# ---------------------------------------------------------------
# Настройка
# ---------------------------------------------------------------
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.WARNING,
)
logger = logging.getLogger(__name__)

# Убавляем логи httpx и telegram
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("telegram").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)

load_dotenv()
TOKEN = os.environ.get("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN не найден! Добавь его в .env файл.")

# ---------------------------------------------------------------
# Состояния
# ---------------------------------------------------------------
user_data: dict[int, dict] = {}

# ---------------------------------------------------------------
# Константы
# ---------------------------------------------------------------
PLANET_EMOJI = {
    "Lagna": "🌞",
    "Sun": "☀️", "Moon": "🌙", "Mercury": "☿️", "Venus": "♀️",
    "Mars": "♂️", "Jupiter": "♃", "Saturn": "♄", "Rahu": "🌑", "Ketu": "🌘",
}

PLANET_LABELS_RU = {
    "Lagna": "Лагна",
    "Sun": "Сурья", "Moon": "Чандра", "Mercury": "Будха", "Venus": "Шукра",
    "Mars": "Мангала", "Jupiter": "Гуру", "Saturn": "Шани", "Rahu": "Раху", "Ketu": "Кету",
}

VARGAS_MD = [
    ("D1 — Раши (Rasi)",          1,  "Тело, общая судьба"),
    ("D2 — Хора (Hora)",          2,  "Богатство, финансы"),
    ("D3 — Дреккана (Drekkana)",  3,  "Братья/сёстры, смелость"),
    ("D4 — Чатуртхамша (Chaturthamsa)", 4,  "Недвижимость, удача"),
    ("D5 — Панчамша (Panchamsa)", 5,  "Власть, слава, знания"),
    ("D7 — Саптамша (Saptamsa)",  7,  "Дети, творчество"),
    ("D8 — Аштамша (Ashtamsa)",   8,  "Препятствия, неожиданности"),
    ("D9 — Навамша (Navamsa)",    9,  "Брак, партнёр, дхарма"),
    ("D10 — Дашамша (Dasamsa)",  10,  "Карьера, профессия"),
    ("D12 — Двадашамша (Dwadasamsa)", 12, "Родители, наследственность"),
    ("D16 — Шодашамша (Shodasamsa)", 16, "Комфорт, транспорт"),
    ("D20 — Вимшамша (Vimsamsa)", 20,  "Духовность, аскетизм"),
    ("D24 — Чатурвимшамша (Chaturvimsamsa)", 24, "Образование, знания"),
    ("D27 — Саптавимшамша (Saptavimsamsa)", 27, "Сильные стороны"),
    ("D30 — Тримшамша (Trimsamsa)", 30, "Негатив, трудности"),
    ("D40 — Кхаведамша (Khavedamsa)", 40, "Заслуги, благосостояние"),
    ("D45 — Акшаведамша (Akshavedamsa)", 45, "Поведение, мораль"),
    ("D60 — Шаштьямша (Shashtyamsa)", 60, "Кармический баланс"),
]


# ---------------------------------------------------------------
# Форматирование Markdown
# ---------------------------------------------------------------
def md_planet_table(result: dict, planet_names: list[str]) -> str:
    """Markdown-таблица планет."""
    lines = []
    lines.append("| Граха | Знак | Градус |")
    lines.append("|-------|------|--------|")
    # Лагна
    s = SIGN_NAMES_RU[result["lagna_sign"]]
    d = result["lagna_degree"]
    lines.append(f"| {PLANET_EMOJI['Lagna']} {PLANET_LABELS_RU['Lagna']} | {s} | {d:.2f}° |")
    # Планеты
    for name in planet_names:
        pos = result["d1_positions"][name]
        sign_num = int(pos // 30)
        degree = pos % 30
        lines.append(
            f"| {PLANET_EMOJI.get(name, '')} {PLANET_LABELS_RU.get(name, name)} "
            f"| {SIGN_NAMES_RU[sign_num]} | {degree:.2f}° |"
        )
    return "\n".join(lines)


def md_varga_table(chart: dict) -> str:
    """Markdown-таблица для варги."""
    lines = []
    lines.append("| Граха | Знак | Градус |")
    lines.append("|-------|------|--------|")
    for name in ["Lagna"] + PLANET_KEYS:
        d = chart[name]
        label = PLANET_LABELS_RU.get(name, name)
        emoji = PLANET_EMOJI.get(name, "")
        lines.append(
            f"| {emoji} {label} | {SIGN_NAMES_RU[d['sign_num']]} | {d['degree']:.2f}° |"
        )
    return "\n".join(lines)


def build_md(result: dict, full_mode: bool) -> str:
    lines = []

    # Заголовок
    lines.append("# 🔮 Джьотиш — Натальная карта")
    lines.append("")
    lines.append(
        f"**📍 {result['city']}** — {result['birth_local'].strftime('%d.%m.%Y %H:%M')}  \n"
        f"🗺 UTC {result['utc_dt'].strftime('%H:%M')} | {result['tz_name']} | "
        f"{result['lat']:.4f}, {result['lon']:.4f}"
    )
    lines.append("")

    # D1
    lines.append("## 📊 D1 — Раши-чакра")
    lines.append("")
    lines.append(md_planet_table(result, PLANET_KEYS))
    lines.append("")

    # Накшатра
    nak_idx = result["nakshatra_index"]
    nak_name = NAKSHATRA_NAMES_RU[nak_idx]
    lord_ru = NAKSHATRA_LORDS_RU[NAKSHATRA_LORDS.index(result["moon_lord"])]
    lines.append(
        f"- 🌙 **Накшатра:** {nak_name}, Пада: {result['pada']}\n"
        f"- 👑 **Управитель:** {lord_ru}\n"
        f"- 📅 **Баланс даши:** {result['balance_years']:.2f} лет"
    )
    lines.append("")

    # Даши
    lines.append("## 📅 Вимшоттари-даша (Махадаша)")
    lines.append("")
    lines.append("| Даша | Начало | Конец |")
    lines.append("|------|--------|-------|")
    for lord, start, end in result["dasha_sequence"]:
        if start.year <= 2030:
            lord_label = NAKSHATRA_LORDS_RU[NAKSHATRA_LORDS.index(lord)]
            lines.append(
                f"| {lord_label} | {start.strftime('%d.%m.%Y')} | {end.strftime('%d.%m.%Y')} |"
            )
    lines.append("")

    # Варги
    if full_mode:
        lines.append("---")
        lines.append("## 📊 Варги (Divisional Charts)")
        lines.append("")

        all_positions = dict(result["d1_positions"])
        all_positions["Lagna"] = result["lagna_abs"]

        for title, divisor, desc in VARGAS_MD:
            lines.append(f"### {title}")
            lines.append(f"*{desc}*")
            lines.append("")

            chart = {}
            for name, abs_pos in all_positions.items():
                s, deg = calculate_varga(divisor, abs_pos)
                chart[name] = {"sign_num": s, "degree": deg}

            lines.append(md_varga_table(chart))
            lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------
# Команды
# ---------------------------------------------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    uid = update.effective_user.id
    uid = update.effective_user.id
    user_data[uid] = {"awaiting_city": True}
    await update.message.reply_text(
        "👋 **Джьотиш-калькулятор**\n\n"
        "Сейчас я задам несколько вопросов:\n"
        "1️⃣ Город рождения\n"
        "2️⃣ Дату рождения\n"
        "3️⃣ Время рождения",
        parse_mode="Markdown",
    )
    await update.message.reply_text(
        "**Введи город рождения:**",
        parse_mode="Markdown",
    )





# ---------------------------------------------------------------
# Парсинг ввода
# ---------------------------------------------------------------
def validate_date(date_str: str) -> bool:
    """Проверяет формат ДД.ММ.ГГГГ и реальность даты."""
    if date_str.count(".") != 2:
        return False
    parts = date_str.split(".")
    if len(parts) != 3:
        return False
    try:
        day, month, year = int(parts[0]), int(parts[1]), int(parts[2])
    except ValueError:
        return False
    if not (1 <= day <= 31 and 1 <= month <= 12 and 1900 <= year <= 2100):
        return False
    # Проверка через datetime
    try:
        datetime.strptime(date_str, "%d.%m.%Y")
        return True
    except ValueError:
        return False


def validate_time(time_str: str) -> bool:
    """Проверяет формат ЧЧ:ММ."""
    if time_str.count(":") != 1:
        return False
    parts = time_str.split(":")
    if len(parts) != 2:
        return False
    h, m = parts[0], parts[1]
    # оба — ровно 2 цифры
    if len(h) != 2 or len(m) != 2:
        return False
    try:
        hour, minute = int(h), int(m)
    except ValueError:
        return False
    return 0 <= hour <= 23 and 0 <= minute <= 59


# ---------------------------------------------------------------
# Парсинг ввода
# ---------------------------------------------------------------
def parse_input(text: str) -> tuple[str, str, str] | None:
    parts = [p.strip() for p in text.split(";")]
    if len(parts) != 3:
        return None
    city, date_str, time_str = parts
    if not city:
        return None
    if not validate_date(date_str):
        return None
    if not validate_time(time_str):
        return None
    return city, date_str, time_str


# ---------------------------------------------------------------
# Обработка сообщений
# ---------------------------------------------------------------
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text.strip()
    uid = update.effective_user.id

    # Пошаговый сбор
    if uid in user_data:
        ud = user_data[uid]
        if ud.get("awaiting_city"):
            if not text.strip():
                await update.message.reply_text("❌ Название города не может быть пустым. Попробуй ещё раз:")
                return
            # Проверяем, что город находится
            from geopy.geocoders import Nominatim
            geolocator = Nominatim(user_agent="natal_chart_bot")
            location = geolocator.geocode(text.strip(), featuretype="city", addressdetails=1)
            if location is None:
                await update.message.reply_text(
                    f"❌ Не удалось найти населённый пункт «{text}». Проверь название и попробуй ещё раз:"
                )
                return
            ud["city"] = text.strip()
            ud["lat"] = location.latitude
            ud["lon"] = location.longitude
            ud["awaiting_city"] = False
            ud["awaiting_date"] = True
            await update.message.reply_text("Теперь введи дату рождения (**ДД.ММ.ГГГГ**):", parse_mode="Markdown")
            return
        elif ud.get("awaiting_date"):
            if not validate_date(text):
                await update.message.reply_text(
                    "❌ Неверный формат. Введи дату как **ДД.ММ.ГГГГ**, например: `16.03.1989`",
                    parse_mode="Markdown",
                )
                return
            ud["date"] = text
            ud["awaiting_date"] = False
            ud["awaiting_time"] = True
            await update.message.reply_text("Теперь время рождения (**ЧЧ:ММ**):", parse_mode="Markdown")
            return
        elif ud.get("awaiting_time"):
            if not validate_time(text):
                await update.message.reply_text(
                    "❌ Неверный формат. Введи время как **ЧЧ:ММ**, например: `03:00`",
                    parse_mode="Markdown",
                )
                return
            ud["time"] = text
            ud["awaiting_time"] = False
            city, date_str, time_str = ud["city"], ud["date"], ud["time"]
            lat, lon = ud.get("lat"), ud.get("lon")
            del user_data[uid]
            await do_calc(update, city, date_str, time_str, lat=lat, lon=lon)
            return

    # Парсим строку
    parsed = parse_input(text)
    if parsed is not None:
        city, date_str, time_str = parsed
        await do_calc(update, city, date_str, time_str)
    else:
        user_data[uid] = {"awaiting_city": True}
        await update.message.reply_text("Введи город рождения:")


# ---------------------------------------------------------------
# Расчёт и отправка .md файлом
# ---------------------------------------------------------------
async def do_calc(
    update: Update, city: str, date_str: str, time_str: str,
    lat: float | None = None, lon: float | None = None,
) -> None:
    msg = await update.message.reply_text("🔮 Рассчитываю...")

    try:
        result = calculate(city, date_str, time_str, lat=lat, lon=lon)
    except ValueError as e:
        await msg.edit_text(f"❌ {e}")
        return
    except Exception as e:
        logger.exception("Ошибка расчёта")
        await msg.edit_text(f"❌ Ошибка: {e}")
        return

    md_content = build_md(result, full_mode=True)

    # Отправляем как .md файл
    label = "natalnaya-karta"
    filename = f"{label}.md"
    bio = io.BytesIO(md_content.encode("utf-8"))
    bio.name = filename

    await msg.delete()

    await update.message.reply_document(
        document=bio,
        filename=filename,
        caption=f"🔮 Натальная карта — {result['city']}, {result['birth_local'].strftime('%d.%m.%Y')}",
    )


# ---------------------------------------------------------------
# Запуск
# ---------------------------------------------------------------
def main() -> None:
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Бот запущен. Нажми Ctrl+C для остановки.")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()