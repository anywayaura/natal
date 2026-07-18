"""
Analyze TWO datasets to deduce exact varga formulas.
Dataset 1: 30.12.1995, 14:30, Novosibirsk
Dataset 2: 16.03.1989, 03:00, Novosibirsk
"""
from natal import calculate

# Reference data for BOTH datasets
# Format: {varga: {planet: (sign, degree)}}
REF1 = {
    "D5": {"AS":(9,25),"SU":(8,11),"MO":(0,13),"ME":(1,16),"VE":(11,23),"MA":(6,25),"JU":(0,26),"SA":(6,7),"RA":(7,23),"KE":(7,23)},
    "D10":{"AS":(4,20),"SU":(0,23),"MO":(0,26),"ME":(6,3),"VE":(10,17),"MA":(5,20),"JU":(9,23),"SA":(6,14),"RA":(10,17),"KE":(4,17)},
    "D24":{"AS":(9,12),"SU":(3,14),"MO":(6,3),"ME":(5,19),"VE":(4,13),"MA":(3,8),"JU":(8,7),"SA":(0,11),"RA":(1,29),"KE":(1,29)},
    "D30":{"AS":(9,0),"SU":(8,10),"MO":(0,19),"ME":(1,9),"VE":(11,23),"MA":(6,2),"JU":(10,9),"SA":(6,14),"RA":(7,21),"KE":(7,21)},
    "D40":{"AS":(0,20),"SU":(7,4),"MO":(3,15),"ME":(10,13),"VE":(4,11),"MA":(2,23),"JU":(7,2),"SA":(9,29),"RA":(8,8),"KE":(8,8)},
}

REF2 = {
    "D5": {"AS":(9,1),"SU":(1,7),"MO":(2,2),"ME":(8,12),"VE":(6,12),"MA":(5,15),"JU":(5,4),"SA":(2,5),"RA":(10,20),"KE":(10,20)},
    "D10":{"AS":(9,3),"SU":(7,15),"MO":(8,4),"ME":(2,24),"VE":(6,24),"MA":(0,0),"JU":(11,9),"SA":(2,10),"RA":(1,11),"KE":(7,11)},
    "D24":{"AS":(5,20),"SU":(4,6),"MO":(6,22),"ME":(3,15),"VE":(1,3),"MA":(10,6),"JU":(8,17),"SA":(7,7),"RA":(0,4),"KE":(0,4)},
    "D30":{"AS":(11,10),"SU":(1,15),"MO":(2,12),"ME":(8,12),"VE":(6,12),"MA":(5,0),"JU":(5,29),"SA":(2,1),"RA":(8,5),"KE":(8,5)},
    "D40":{"AS":(6,13),"SU":(8,0),"MO":(0,16),"ME":(7,6),"VE":(10,6),"MA":(6,0),"JU":(3,9),"SA":(1,11),"RA":(1,16),"KE":(1,16)},
}

PVAL = {"AS":"Lagna","SU":"Sun","MO":"Moon","ME":"Mercury","VE":"Venus","MA":"Mars","JU":"Jupiter","SA":"Saturn","RA":"Rahu","KE":"Ketu"}
PLANETS = ["AS","SU","MO","ME","VE","MA","JU","SA","RA","KE"]

# Calculate D1 for both datasets
r1 = calculate("Новосибирск", "30.12.1995", "14:30", lat=55.0288, lon=82.9227)
r2 = calculate("Новосибирск", "16.03.1989", "03:00", lat=55.0288, lon=82.9227)

d1_1 = {"Lagna": r1["lagna_abs"]}
for k in ["Sun","Moon","Mercury","Venus","Mars","Jupiter","Saturn","Rahu","Ketu"]:
    d1_1[k] = r1["d1_positions"][k]

d1_2 = {"Lagna": r2["lagna_abs"]}
for k in ["Sun","Moon","Mercury","Venus","Mars","Jupiter","Saturn","Rahu","Ketu"]:
    d1_2[k] = r2["d1_positions"][k]

print("D1 positions for dataset 2:")
for p in PLANETS:
    abs_pos = d1_2[PVAL[p]]
    s = int(abs_pos // 30)
    d = abs_pos % 30
    print(f"  {p}: sign={s} deg={d:.2f}")

# For each varga, analyze BOTH datasets together
for vn in ["D5","D10","D24","D30","D40"]:
    div = int(vn[1:])
    part_size = 30.0 / div
    
    print(f"\n{'='*70}")
    print(f"  {vn} — COMBINED ANALYSIS (both datasets)")
    print(f"{'='*70}")
    
    # Collect all (sign, part) → varga_sign mappings
    mappings = {}
    
    for ref, d1_data in [(REF1, d1_1), (REF2, d1_2)]:
        for p in PLANETS:
            s_ref, d_ref = ref[vn][p]
            d1_abs = d1_data[PVAL[p]]
            s1 = int(d1_abs // 30)
            d1_deg = d1_abs % 30
            part = int(d1_deg / part_size)
            key = (s1, part)
            if key not in mappings:
                mappings[key] = set()
            mappings[key].add(s_ref)
    
    # Check consistency
    conflicts = []
    for key, ref_signs in sorted(mappings.items()):
        if len(ref_signs) > 1:
            conflicts.append((key, ref_signs))
    
    if conflicts:
        print(f"  CONFLICTS (same sign+part → different varga signs):")
        for key, signs in conflicts:
            print(f"    sign={key[0]}, part={key[1]} → {signs}")
    else:
        print(f"  All mappings are consistent!")
    
    # Print the mapping table
    print(f"\n  Mapping table (sign, part) → varga_sign:")
    for s1 in range(12):
        row = []
        for part in range(div):
            key = (s1, part)
            if key in mappings:
                signs = list(mappings[key])
                row.append(str(signs[0]))
            else:
                row.append("?")
        print(f"  sign={s1:2d}: [{', '.join(row)}]")
    
    # Try to find formula
    print(f"\n  Trying formulas:")
    
    # Formula 1: (sign + part) % 12
    matches = 0
    total = 0
    for ref, d1_data in [(REF1, d1_1), (REF2, d1_2)]:
        for p in PLANETS:
            s_ref, d_ref = ref[vn][p]
            d1_abs = d1_data[PVAL[p]]
            s1 = int(d1_abs // 30)
            d1_deg = d1_abs % 30
            part = int(d1_deg / part_size)
            calc = (s1 + part) % 12
            total += 1
            if calc == s_ref:
                matches += 1
    print(f"  (s1+part)%12: {matches}/{total}")
    
    # Formula 2: (sign * div + part) % 12
    matches = 0
    for ref, d1_data in [(REF1, d1_1), (REF2, d1_2)]:
        for p in PLANETS:
            s_ref, d_ref = ref[vn][p]
            d1_abs = d1_data[PVAL[p]]
            s1 = int(d1_abs // 30)
            d1_deg = d1_abs % 30
            part = int(d1_deg / part_size)
            calc = (s1 * div + part) % 12
            if calc == s_ref:
                matches += 1
    print(f"  (s1*div+part)%12: {matches}/{total}")
    
    # Formula 3: Navamsa-like
    matches = 0
    for ref, d1_data in [(REF1, d1_1), (REF2, d1_2)]:
        for p in PLANETS:
            s_ref, d_ref = ref[vn][p]
            d1_abs = d1_data[PVAL[p]]
            s1 = int(d1_abs // 30)
            d1_deg = d1_abs % 30
            part = int(d1_deg / part_size)
            if s1 in (0,3,6,9): start = 0
            elif s1 in (1,4,7,10): start = 4
            else: start = 8
            calc = (start + part) % 12
            if calc == s_ref:
                matches += 1
    print(f"  Navamsa-like: {matches}/{total}")
    
    # Formula 4: (sign + part * div) % 12
    matches = 0
    for ref, d1_data in [(REF1, d1_1), (REF2, d1_2)]:
        for p in PLANETS:
            s_ref, d_ref = ref[vn][p]
            d1_abs = d1_data[PVAL[p]]
            s1 = int(d1_abs // 30)
            d1_deg = d1_abs % 30
            part = int(d1_deg / part_size)
            calc = (s1 + part * div) % 12
            if calc == s_ref:
                matches += 1
    print(f"  (s1+part*div)%12: {matches}/{total}")
    
    # Formula 5: (sign * div + part * div) % 12 = (sign+part)*div % 12
    matches = 0
    for ref, d1_data in [(REF1, d1_1), (REF2, d1_2)]:
        for p in PLANETS:
            s_ref, d_ref = ref[vn][p]
            d1_abs = d1_data[PVAL[p]]
            s1 = int(d1_abs // 30)
            d1_deg = d1_abs % 30
            part = int(d1_deg / part_size)
            calc = ((s1 + part) * div) % 12
            if calc == s_ref:
                matches += 1
    print(f"  (s1+part)*div%12: {matches}/{total}")
    
    # Formula 6: sequential (abs_pos * div) % 360
    matches = 0
    for ref, d1_data in [(REF1, d1_1), (REF2, d1_2)]:
        for p in PLANETS:
            s_ref, d_ref = ref[vn][p]
            d1_abs = d1_data[PVAL[p]]
            calc_abs = (d1_abs * div) % 360
            calc = int(calc_abs // 30)
            if calc == s_ref:
                matches += 1
    print(f"  sequential (abs*div)%360: {matches}/{total}")