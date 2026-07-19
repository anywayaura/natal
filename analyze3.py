"""
Analyze THREE datasets to deduce varga formulas for D5, D10, D24, D30, D40.
"""
from natal import calculate

PVAL = {"AS":"Lagna","SU":"Sun","MO":"Moon","ME":"Mercury","VE":"Venus","MA":"Mars","JU":"Jupiter","SA":"Saturn","RA":"Rahu","KE":"Ketu"}
PLANETS = ["AS","SU","MO","ME","VE","MA","JU","SA","RA","KE"]

# Dataset 3: 10.01.1970, 19:20, New York
R3 = {
    "D5": {"AS":(7,20),"SU":(6,14),"MO":(10,26),"ME":(1,11),"VE":(2,28),"MA":(6,11),"JU":(10,20),"SA":(10,13),"RA":(2,16),"KE":(2,16)},
    "D10":{"AS":(8,10),"SU":(4,29),"MO":(1,22),"ME":(5,23),"VE":(3,26),"MA":(6,22),"JU":(9,11),"SA":(2,26),"RA":(5,3),"KE":(11,3)},
    "D24":{"AS":(1,12),"SU":(1,16),"MO":(1,1),"ME":(4,26),"VE":(10,26),"MA":(1,0),"JU":(0,3),"SA":(10,27),"RA":(9,1),"KE":(9,1)},
    "D30":{"AS":(7,0),"SU":(6,27),"MO":(8,8),"ME":(1,10),"VE":(2,18),"MA":(6,7),"JU":(8,4),"SA":(10,19),"RA":(2,9),"KE":(2,9)},
    "D40":{"AS":(7,10),"SU":(10,27),"MO":(3,1),"ME":(9,4),"VE":(7,14),"MA":(10,0),"JU":(1,15),"SA":(10,16),"RA":(4,12),"KE":(4,12)},
}

r3 = calculate("New York", "10.01.1970", "19:20", lat=40.72, lon=-74.0)
d1_3 = {"Lagna": r3["lagna_abs"]}
for k in ["Sun","Moon","Mercury","Venus","Mars","Jupiter","Saturn","Rahu","Ketu"]:
    d1_3[k] = r3["d1_positions"][k]

print("D1 positions for dataset 3 (New York):")
for p in PLANETS:
    abs_pos = d1_3[PVAL[p]]
    s = int(abs_pos // 30)
    d = abs_pos % 30
    print(f"  {p}: sign={s} deg={d:.2f}")

# For each varga, analyze patterns
for vn in ["D5","D10","D24","D30","D40"]:
    div = int(vn[1:])
    part_size = 30.0 / div
    
    print(f"\n{'='*70}")
    print(f"  {vn} — New data points")
    print(f"{'='*70}")
    
    for p in PLANETS:
        s_ref, d_ref = R3[vn][p]
        d1_abs = d1_3[PVAL[p]]
        s1 = int(d1_abs // 30)
        d1_deg = d1_abs % 30
        part = int(d1_deg / part_size)
        
        # Try formulas
        seq = int(((d1_abs * div) % 360) // 30)
        sp = (s1 + part) % 12
        nav = None
        if s1 in (0,3,6,9): start=0
        elif s1 in (1,4,7,10): start=4
        else: start=8
        nav = (start + part) % 12
        
        match_seq = "✅" if seq == s_ref else ""
        match_sp = "✅" if sp == s_ref else ""
        match_nav = "✅" if nav == s_ref else ""
        
        print(f"  {p}: D1({s1},{d1_deg:.1f}) part={part} → ref={s_ref} | seq={seq}{match_seq} sp={sp}{match_sp} nav={nav}{match_nav}")

print("\n\n=== BEST FORMULA SUMMARY ===")
for vn in ["D5","D10","D24","D30","D40"]:
    div = int(vn[1:])
    part_size = 30.0 / div
    seq_count = 0
    sp_count = 0
    nav_count = 0
    total = 0
    for p in PLANETS:
        s_ref, d_ref = R3[vn][p]
        d1_abs = d1_3[PVAL[p]]
        s1 = int(d1_abs // 30)
        d1_deg = d1_abs % 30
        part = int(d1_deg / part_size)
        total += 1
        if int(((d1_abs * div) % 360) // 30) == s_ref: seq_count += 1
        if (s1 + part) % 12 == s_ref: sp_count += 1
        if s1 in (0,3,6,9): start=0
        elif s1 in (1,4,7,10): start=4
        else: start=8
        if (start + part) % 12 == s_ref: nav_count += 1
    print(f"{vn}: seq={seq_count}/{total}  (s1+part)={sp_count}/{total}  navamsa={nav_count}/{total}")