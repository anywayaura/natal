"""Fix D40 rounding and find D10 formula."""
from natal import calculate

PVAL = {"AS":"Lagna","SU":"Sun","MO":"Moon","ME":"Mercury","VE":"Venus","MA":"Mars","JU":"Jupiter","SA":"Saturn","RA":"Rahu","KE":"Ketu"}
PLANETS = ["AS","SU","MO","ME","VE","MA","JU","SA","RA","KE"]

DATASETS = [
    ("30.12.1995", "14:30", "Novosibirsk", 55.0288, 82.9227),
    ("16.03.1989", "03:00", "Novosibirsk", 55.0288, 82.9227),
    ("10.01.1970", "19:20", "New York", 40.72, -74.0),
]

REF40 = {
    ("30.12.1995","14:30"): {"AS":0,"SU":7,"MO":3,"ME":10,"VE":4,"MA":2,"JU":7,"SA":9,"RA":8,"KE":8},
    ("16.03.1989","03:00"): {"AS":6,"SU":8,"MO":0,"ME":7,"VE":10,"MA":6,"JU":3,"SA":1,"RA":1,"KE":1},
    ("10.01.1970","19:20"): {"AS":7,"SU":10,"MO":3,"ME":9,"VE":7,"MA":10,"JU":1,"SA":10,"RA":4,"KE":4},
}

REF10 = {
    ("30.12.1995","14:30"): {"AS":4,"SU":0,"MO":0,"ME":6,"VE":10,"MA":5,"JU":9,"SA":6,"RA":10,"KE":4},
    ("16.03.1989","03:00"): {"AS":9,"SU":7,"MO":8,"ME":2,"VE":6,"MA":0,"JU":11,"SA":2,"RA":1,"KE":7},
    ("10.01.1970","19:20"): {"AS":8,"SU":4,"MO":1,"ME":5,"VE":3,"MA":6,"JU":9,"SA":2,"RA":5,"KE":11},
}

REF5 = {
    ("30.12.1995","14:30"): {"AS":9,"SU":8,"MO":0,"ME":1,"VE":11,"MA":6,"JU":0,"SA":6,"RA":7,"KE":7},
    ("16.03.1989","03:00"): {"AS":9,"SU":1,"MO":2,"ME":8,"VE":6,"MA":5,"JU":5,"SA":2,"RA":10,"KE":10},
    ("10.01.1970","19:20"): {"AS":7,"SU":6,"MO":10,"ME":1,"VE":2,"MA":6,"JU":10,"SA":10,"RA":2,"KE":2},
}

# Pre-calc all D1
all_d1 = {}
for date, time, city, lat, lon in DATASETS:
    r = calculate(city, date, time, lat=lat, lon=lon)
    d1 = {"Lagna": r["lagna_abs"]}
    for k in ["Sun","Moon","Mercury","Venus","Mars","Jupiter","Saturn","Rahu","Ketu"]:
        d1[k] = r["d1_positions"][k]
    all_d1[(date,time)] = d1

# === D40 with rounding ===
print("D40 — with rounding (odd→Aries(0), even→Libra(6)):")
total_ok = 0
for date, time, city, lat, lon in DATASETS:
    d1 = all_d1[(date,time)]
    ok = 0
    for p in PLANETS:
        s_ref = REF40[(date,time)][p]
        abs_pos = d1[PVAL[p]]
        s1 = int(abs_pos // 30)
        d1_deg = abs_pos % 30
        part = int(round(d1_deg) / 0.75)
        start = 0 if s1 % 2 == 0 else 6
        calc = (start + part) % 12
        if calc == s_ref:
            ok += 1
        else:
            print(f"  {city[:4]} {p}: calc={calc} ref={s_ref} (deg={d1_deg:.2f} part={part})")
    print(f"  {city} {date}: {ok}/10")
    total_ok += ok
print(f"  TOTAL: {total_ok}/30")

# === D10 — try BPHS formula with different starting signs ===
print("\n\nD10 — BPHS formula (movable→same, fixed→9th, dual→5th):")
for date, time, city, lat, lon in DATASETS:
    d1 = all_d1[(date,time)]
    ok = 0
    for p in PLANETS:
        s_ref = REF10[(date,time)][p]
        abs_pos = d1[PVAL[p]]
        s1 = int(abs_pos // 30)
        d1_deg = abs_pos % 30
        part = int(d1_deg / 3.0)
        if s1 in (0,3,6,9): start = s1
        elif s1 in (1,4,7,10): start = (s1 + 8) % 12
        else: start = (s1 + 4) % 12
        calc = (start + part) % 12
        if calc == s_ref: ok += 1
    print(f"  {city} {date}: {ok}/10")

# D10 — try: movable→Aries(0), fixed→Leo(4), dual→Sag(8) (Navamsa-like)
print("\nD10 — Navamsa-like (mov→0, fix→4, dual→8):")
for date, time, city, lat, lon in DATASETS:
    d1 = all_d1[(date,time)]
    ok = 0
    for p in PLANETS:
        s_ref = REF10[(date,time)][p]
        abs_pos = d1[PVAL[p]]
        s1 = int(abs_pos // 30)
        d1_deg = abs_pos % 30
        part = int(d1_deg / 3.0)
        if s1 in (0,3,6,9): start = 0
        elif s1 in (1,4,7,10): start = 4
        else: start = 8
        calc = (start + part) % 12
        if calc == s_ref: ok += 1
    print(f"  {city} {date}: {ok}/10")

# D10 — try: sequential (abs*div)%360
print("\nD10 — sequential (abs*div)%360:")
for date, time, city, lat, lon in DATASETS:
    d1 = all_d1[(date,time)]
    ok = 0
    for p in PLANETS:
        s_ref = REF10[(date,time)][p]
        abs_pos = d1[PVAL[p]]
        calc = int(((abs_pos * 10) % 360) // 30)
        if calc == s_ref: ok += 1
    print(f"  {city} {date}: {ok}/10")

# D10 — try: (sign + part) % 12
print("\nD10 — (sign+part)%12:")
for date, time, city, lat, lon in DATASETS:
    d1 = all_d1[(date,time)]
    ok = 0
    for p in PLANETS:
        s_ref = REF10[(date,time)][p]
        abs_pos = d1[PVAL[p]]
        s1 = int(abs_pos // 30)
        d1_deg = abs_pos % 30
        part = int(d1_deg / 3.0)
        calc = (s1 + part) % 12
        if calc == s_ref: ok += 1
    print(f"  {city} {date}: {ok}/10")

# === D5 — try various ===
print("\n\nD5 — sequential (abs*div)%360:")
for date, time, city, lat, lon in DATASETS:
    d1 = all_d1[(date,time)]
    ok = 0
    for p in PLANETS:
        s_ref = REF5[(date,time)][p]
        abs_pos = d1[PVAL[p]]
        calc = int(((abs_pos * 5) % 360) // 30)
        if calc == s_ref: ok += 1
    print(f"  {city} {date}: {ok}/10")

print("\nD5 — (sign+part)%12:")
for date, time, city, lat, lon in DATASETS:
    d1 = all_d1[(date,time)]
    ok = 0
    for p in PLANETS:
        s_ref = REF5[(date,time)][p]
        abs_pos = d1[PVAL[p]]
        s1 = int(abs_pos // 30)
        d1_deg = abs_pos % 30
        part = int(d1_deg / 6.0)
        calc = (s1 + part) % 12
        if calc == s_ref: ok += 1
    print(f"  {city} {date}: {ok}/10")

print("\nD5 — Navamsa-like (mov→0, fix→4, dual→8):")
for date, time, city, lat, lon in DATASETS:
    d1 = all_d1[(date,time)]
    ok = 0
    for p in PLANETS:
        s_ref = REF5[(date,time)][p]
        abs_pos = d1[PVAL[p]]
        s1 = int(abs_pos // 30)
        d1_deg = abs_pos % 30
        part = int(d1_deg / 6.0)
        if s1 in (0,3,6,9): start = 0
        elif s1 in (1,4,7,10): start = 4
        else: start = 8
        calc = (start + part) % 12
        if calc == s_ref: ok += 1
    print(f"  {city} {date}: {ok}/10")