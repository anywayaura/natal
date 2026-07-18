"""
Analyze reference data to deduce correct varga algorithms.
For each varga and each planet, computes the mapping from D1 to varga.
"""
from natal import calculate

# Reference data: (sign, degree) for each varga and planet
REF = {
    "D1": {"AS":(1,23),"SU":(8,14),"MO":(0,2),"ME":(9,3),"VE":(9,16),"MA":(8,29),"JU":(8,5),"SA":(10,25),"RA":(5,28),"KE":(11,28)},
    "D2": {"AS":(4,16),"SU":(4,28),"MO":(4,5),"ME":(3,6),"VE":(4,3),"MA":(3,28),"JU":(4,10),"SA":(3,20),"RA":(4,27),"KE":(4,27)},
    "D3": {"AS":(9,9),"SU":(0,13),"MO":(0,7),"ME":(9,9),"VE":(1,20),"MA":(4,27),"JU":(8,15),"SA":(6,16),"RA":(1,26),"KE":(7,26)},
    "D4": {"AS":(10,2),"SU":(11,27),"MO":(0,10),"ME":(9,13),"VE":(3,7),"MA":(5,26),"JU":(8,21),"SA":(7,11),"RA":(2,24),"KE":(8,24)},
    "D5": {"AS":(9,25),"SU":(8,11),"MO":(0,13),"ME":(1,16),"VE":(11,23),"MA":(6,25),"JU":(0,26),"SA":(6,7),"RA":(7,23),"KE":(7,23)},
    "D7": {"AS":(0,11),"SU":(11,10),"MO":(0,18),"ME":(3,23),"VE":(6,27),"MA":(2,23),"JU":(9,7),"SA":(3,28),"RA":(5,21),"KE":(11,21)},
    "D8": {"AS":(2,4),"SU":(7,24),"MO":(0,21),"ME":(0,26),"VE":(4,14),"MA":(11,22),"JU":(5,12),"SA":(2,23),"RA":(11,19),"KE":(11,19)},
    "D9": {"AS":(3,27),"SU":(4,9),"MO":(0,23),"ME":(9,29),"VE":(2,1),"MA":(8,21),"JU":(1,17),"SA":(1,19),"RA":(5,18),"KE":(11,18)},
    "D10":{"AS":(4,20),"SU":(0,23),"MO":(0,26),"ME":(6,3),"VE":(10,17),"MA":(5,20),"JU":(9,23),"SA":(6,14),"RA":(10,17),"KE":(4,17)},
    "D12":{"AS":(10,6),"SU":(1,22),"MO":(1,1),"ME":(10,9),"VE":(3,21),"MA":(7,19),"JU":(10,3),"SA":(8,5),"RA":(4,14),"KE":(10,14)},
    "D16":{"AS":(4,8),"SU":(3,19),"MO":(1,12),"ME":(1,23),"VE":(8,28),"MA":(11,15),"JU":(10,24),"SA":(5,17),"RA":(11,9),"KE":(11,9)},
    "D20":{"AS":(11,10),"SU":(1,17),"MO":(1,22),"ME":(2,6),"VE":(11,5),"MA":(11,11),"JU":(7,16),"SA":(0,29),"RA":(11,4),"KE":(11,4)},
    "D24":{"AS":(9,12),"SU":(3,14),"MO":(6,3),"ME":(5,19),"VE":(4,13),"MA":(3,8),"JU":(8,7),"SA":(0,11),"RA":(1,29),"KE":(1,29)},
    "D27":{"AS":(11,21),"SU":(0,27),"MO":(2,11),"ME":(5,29),"VE":(6,3),"MA":(2,5),"JU":(4,23),"SA":(4,28),"RA":(4,25),"KE":(10,25)},
    "D30":{"AS":(9,0),"SU":(8,10),"MO":(0,19),"ME":(1,9),"VE":(11,23),"MA":(6,2),"JU":(10,9),"SA":(6,14),"RA":(7,21),"KE":(7,21)},
    "D40":{"AS":(0,20),"SU":(7,4),"MO":(3,15),"ME":(10,13),"VE":(4,11),"MA":(2,23),"JU":(7,2),"SA":(9,29),"RA":(8,8),"KE":(8,8)},
    "D45":{"AS":(2,15),"SU":(5,16),"MO":(3,28),"ME":(4,29),"VE":(1,5),"MA":(3,18),"JU":(3,28),"SA":(6,6),"RA":(3,2),"KE":(3,2)},
    "D60":{"AS":(11,0),"SU":(0,21),"MO":(5,8),"ME":(3,19),"VE":(6,17),"MA":(6,5),"JU":(6,18),"SA":(0,29),"RA":(2,13),"KE":(8,13)},
}

PLANETS = ["AS","SU","MO","ME","VE","MA","JU","SA","RA","KE"]
PVAL = {"AS":"Lagna","SU":"Sun","MO":"Moon","ME":"Mercury","VE":"Venus","MA":"Mars","JU":"Jupiter","SA":"Saturn","RA":"Rahu","KE":"Ketu"}

# Get D1 positions
result = calculate("Новосибирск", "30.12.1995", "14:30", lat=55.0288, lon=82.9227)
d1 = {}  # key = 'Lagna', 'Sun', 'Moon', ...
d1['Lagna'] = result['lagna_abs']
for k in ['Sun','Moon','Mercury','Venus','Mars','Jupiter','Saturn','Rahu','Ketu']:
    d1[k] = result['d1_positions'][k]

SIGN_TYPES = {0:"M",1:"F",2:"D",3:"M",4:"F",5:"D",6:"M",7:"F",8:"D",9:"M",10:"F",11:"D"}

# For each varga, analyze the mapping
VARGAS = [2,3,4,5,7,8,9,10,12,16,20,24,27,30,40,45,60]

for div in VARGAS:
    vn = f"D{div}"
    if vn not in REF:
        continue
    print(f"\n{'='*60}")
    print(f"  {vn} (divisor={div})")
    print(f"{'='*60}")
    print(f"{'Planet':<6} {'D1_sign':<8} {'D1_deg':<8} {'part':<6} {'Ref_s':<6} {'Ref_d':<6} {'offset':<8} {'stype':<6}")
    print("-"*60)
    
    for p in PLANETS:
        s_ref, d_ref = REF[vn][p]
        d1_abs = d1[PVAL[p]]
        s1 = int(d1_abs // 30)
        d1_deg = d1_abs % 30
        part_size = 30 / div
        part = int(d1_deg / part_size)
        offset = (s_ref - s1) % 12
        stype = SIGN_TYPES[s1]
        print(f"{p:<6} {s1:<8} {d1_deg:<8.2f} {part:<6} {s_ref:<6} {d_ref:<6} {offset:<8} {stype:<6}")

print("\n\n=== SEQUENTIAL FORMULA CHECK ===")
print("Comparing (abs_pos * divisor) % 360 with reference\n")

for div in VARGAS:
    vn = f"D{div}"
    if vn not in REF:
        continue
    fails = []
    for p in PLANETS:
        s_ref, d_ref = REF[vn][p]
        d1_abs = d1[PVAL[p]]
        v_abs = (d1_abs * div) % 360
        s_seq = int(v_abs // 30)
        d_seq = v_abs % 30
        if s_seq != s_ref or abs(d_seq - d_ref) > 2:
            fails.append(f"  {p}: D1={d1_abs:.2f}° → seq={s_seq}°{d_seq:.1f}°, ref={s_ref}°{d_ref}°")
    status = "✅" if len(fails) == 0 else f"❌ ({len(fails)} failures)"
    print(f"{vn} {status}")
    if fails:
        for f in fails[:3]:
            print(f)