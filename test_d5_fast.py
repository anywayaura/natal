"""Fast test: D5 formula on 3 datasets."""
from natal import calculate

PVAL = {"AS":"Lagna","SU":"Sun","MO":"Moon","ME":"Mercury","VE":"Venus","MA":"Mars","JU":"Jupiter","SA":"Saturn","RA":"Rahu","KE":"Ketu"}
PLANETS = ["AS","SU","MO","ME","VE","MA","JU","SA","RA","KE"]

DATASETS = [
    ("30.12.1995", "14:30", "Novosibirsk", 55.0288, 82.9227),
    ("16.03.1989", "03:00", "Novosibirsk", 55.0288, 82.9227),
    ("10.01.1970", "19:20", "New York", 40.72, -74.0),
]

REF5 = {
    ("30.12.1995","14:30"): {"AS":9,"SU":8,"MO":0,"ME":1,"VE":11,"MA":6,"JU":0,"SA":6,"RA":7,"KE":7},
    ("16.03.1989","03:00"): {"AS":9,"SU":1,"MO":2,"ME":8,"VE":6,"MA":5,"JU":5,"SA":2,"RA":10,"KE":10},
    ("10.01.1970","19:20"): {"AS":7,"SU":6,"MO":10,"ME":1,"VE":2,"MA":6,"JU":10,"SA":10,"RA":2,"KE":2},
}

# Pre-calc D1
all_d1 = {}
for date, time, city, lat, lon in DATASETS:
    r = calculate(city, date, time, lat=lat, lon=lon)
    d1 = {"Lagna": r["lagna_abs"]}
    for k in ["Sun","Moon","Mercury","Venus","Mars","Jupiter","Saturn","Rahu","Ketu"]:
        d1[k] = r["d1_positions"][k]
    all_d1[(date,time)] = d1

print("Testing D5 formula: (sign + offset + part) % 12")
for off_odd in range(12):
    for off_even in range(12):
        ok = 0
        total = 0
        for date, time, city, lat, lon in DATASETS:
            d1 = all_d1[(date,time)]
            for p in PLANETS:
                s_ref = REF5[(date,time)][p]
                abs_pos = d1[PVAL[p]]
                s1 = int(abs_pos // 30)
                d1_deg = abs_pos % 30
                part = int(d1_deg / 6.0)
                total += 1
                if s1 % 2 == 0:
                    start = (s1 + off_odd) % 12
                else:
                    start = (s1 + off_even) % 12
                if (start + part) % 12 == s_ref:
                    ok += 1
        if ok > 10:
            print(f"  odd_off={off_odd} even_off={off_even}: {ok}/{total}")