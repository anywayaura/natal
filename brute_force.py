"""Brute-force formula search across 3 datasets."""
from natal import calculate

PVAL = {"AS":"Lagna","SU":"Sun","MO":"Moon","ME":"Mercury","VE":"Venus","MA":"Mars","JU":"Jupiter","SA":"Saturn","RA":"Rahu","KE":"Ketu"}
PLANETS = ["AS","SU","MO","ME","VE","MA","JU","SA","RA","KE"]
VARGAS = [5, 10, 24, 30, 40]

DATASETS = [
    ("30.12.1995", "14:30", "Новосибирск", 55.0288, 82.9227),
    ("16.03.1989", "03:00", "Новосибирск", 55.0288, 82.9227),
    ("10.01.1970", "19:20", "New York", 40.72, -74.0),
]

# Reference signs only (degree not needed for formula search)
REF = {
    ("30.12.1995","14:30"): {
        5: {"AS":9,"SU":8,"MO":0,"ME":1,"VE":11,"MA":6,"JU":0,"SA":6,"RA":7,"KE":7},
        10:{"AS":4,"SU":0,"MO":0,"ME":6,"VE":10,"MA":5,"JU":9,"SA":6,"RA":10,"KE":4},
        24:{"AS":9,"SU":3,"MO":6,"ME":5,"VE":4,"MA":3,"JU":8,"SA":0,"RA":1,"KE":1},
        30:{"AS":9,"SU":8,"MO":0,"ME":1,"VE":11,"MA":6,"JU":10,"SA":6,"RA":7,"KE":7},
        40:{"AS":0,"SU":7,"MO":3,"ME":10,"VE":4,"MA":2,"JU":7,"SA":9,"RA":8,"KE":8},
    },
    ("16.03.1989","03:00"): {
        5: {"AS":9,"SU":1,"MO":2,"ME":8,"VE":6,"MA":5,"JU":5,"SA":2,"RA":10,"KE":10},
        10:{"AS":9,"SU":7,"MO":8,"ME":2,"VE":6,"MA":0,"JU":11,"SA":2,"RA":1,"KE":7},
        24:{"AS":5,"SU":4,"MO":6,"ME":3,"VE":1,"MA":10,"JU":8,"SA":7,"RA":0,"KE":0},
        30:{"AS":11,"SU":1,"MO":2,"ME":8,"VE":6,"MA":5,"JU":5,"SA":2,"RA":8,"KE":8},
        40:{"AS":6,"SU":8,"MO":0,"ME":7,"VE":10,"MA":6,"JU":3,"SA":1,"RA":1,"KE":1},
    },
    ("10.01.1970","19:20"): {
        5: {"AS":7,"SU":6,"MO":10,"ME":1,"VE":2,"MA":6,"JU":10,"SA":10,"RA":2,"KE":2},
        10:{"AS":8,"SU":4,"MO":1,"ME":5,"VE":3,"MA":6,"JU":9,"SA":2,"RA":5,"KE":11},
        24:{"AS":1,"SU":1,"MO":1,"ME":4,"VE":10,"MA":1,"JU":0,"SA":10,"RA":9,"KE":9},
        30:{"AS":7,"SU":6,"MO":8,"ME":1,"VE":2,"MA":6,"JU":8,"SA":10,"RA":2,"KE":2},
        40:{"AS":7,"SU":10,"MO":3,"ME":9,"VE":7,"MA":10,"JU":1,"SA":10,"RA":4,"KE":4},
    },
}

print("Brute-force formula search: result_sign = (a*sign_num + b*part + c) % 12")
print("="*70)

for div in VARGAS:
    print(f"\nD{div} (divisor={div}):")
    best = (0, 0, 0, 0)  # (matches, a, b, c)
    
    for a in range(12):
        for b in range(12):
            for c in range(12):
                matches = 0
                total = 0
                for date, time, city, lat, lon in DATASETS:
                    r = calculate(city, date, time, lat=lat, lon=lon)
                    d1_data = {"Lagna": r["lagna_abs"]}
                    for k in ["Sun","Moon","Mercury","Venus","Mars","Jupiter","Saturn","Rahu","Ketu"]:
                        d1_data[k] = r["d1_positions"][k]
                    
                    ref_signs = REF[(date,time)][div]
                    for p in PLANETS:
                        s_ref = ref_signs[p]
                        abs_pos = d1_data[PVAL[p]]
                        s1 = int(abs_pos // 30)
                        d1_deg = abs_pos % 30
                        part = int(d1_deg / (30.0 / div))
                        calc = (a * s1 + b * part + c) % 12
                        total += 1
                        if calc == s_ref:
                            matches += 1
                
                if matches > best[0]:
                    best = (matches, a, b, c)
    
    m, a, b, c = best
    print(f"  Best: ({a}*sign + {b}*part + {c}) % 12 = {m}/{30} matches")
    
    # Also try with sign type
    for start_m in range(12):
        for start_f in range(12):
            for start_d in range(12):
                for b in range(12):
                    matches = 0
                    for date, time, city, lat, lon in DATASETS:
                        r = calculate(city, date, time, lat=lat, lon=lon)
                        d1_data = {"Lagna": r["lagna_abs"]}
                        for k in ["Sun","Moon","Mercury","Venus","Mars","Jupiter","Saturn","Rahu","Ketu"]:
                            d1_data[k] = r["d1_positions"][k]
                        
                        ref_signs = REF[(date,time)][div]
                        for p in PLANETS:
                            s_ref = ref_signs[p]
                            abs_pos = d1_data[PVAL[p]]
                            s1 = int(abs_pos // 30)
                            d1_deg = abs_pos % 30
                            part = int(d1_deg / (30.0 / div))
                            
                            # Determine sign type
                            if s1 in (0,3,6,9): start = start_m
                            elif s1 in (1,4,7,10): start = start_f
                            else: start = start_d
                            
                            calc = (start + b * part) % 12
                            if calc == s_ref:
                                matches += 1
                    
                    if matches > best[0]:
                        best = (matches, f"start(m={start_m},f={start_f},d={start_d})+{b}*part")
    
    m, formula = best
    print(f"  Best typed: {formula} = {m}/30 matches")