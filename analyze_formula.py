"""
Varga offset formula analysis.
Tests the formula: offset = (sign // 3) * d + (d // 3) * (sign % 3) % 12
"""
from natal import calculate

REF = {
    "D5": {"AS":(9,25),"SU":(8,11),"MO":(0,13),"ME":(1,16),"VE":(11,23),"MA":(6,25),"JU":(0,26),"SA":(6,7),"RA":(7,23),"KE":(7,23)},
    "D10":{"AS":(4,20),"SU":(0,23),"MO":(0,26),"ME":(6,3),"VE":(10,17),"MA":(5,20),"JU":(9,23),"SA":(6,14),"RA":(10,17),"KE":(4,17)},
    "D12":{"AS":(10,6),"SU":(1,22),"MO":(1,1),"ME":(10,9),"VE":(3,21),"MA":(7,19),"JU":(10,3),"SA":(8,5),"RA":(4,14),"KE":(10,14)},
    "D24":{"AS":(9,12),"SU":(3,14),"MO":(6,3),"ME":(5,19),"VE":(4,13),"MA":(3,8),"JU":(8,7),"SA":(0,11),"RA":(1,29),"KE":(1,29)},
    "D30":{"AS":(9,0),"SU":(8,10),"MO":(0,19),"ME":(1,9),"VE":(11,23),"MA":(6,2),"JU":(10,9),"SA":(6,14),"RA":(7,21),"KE":(7,21)},
    "D40":{"AS":(0,20),"SU":(7,4),"MO":(3,15),"ME":(10,13),"VE":(4,11),"MA":(2,23),"JU":(7,2),"SA":(9,29),"RA":(8,8),"KE":(8,8)},
    "D45":{"AS":(2,15),"SU":(5,16),"MO":(3,28),"ME":(4,29),"VE":(1,5),"MA":(3,18),"JU":(3,28),"SA":(6,6),"RA":(3,2),"KE":(3,2)},
    "D60":{"AS":(11,0),"SU":(0,21),"MO":(5,8),"ME":(3,19),"VE":(6,17),"MA":(6,5),"JU":(6,18),"SA":(0,29),"RA":(2,13),"KE":(8,13)},
}

PVAL = {"AS":"Lagna","SU":"Sun","MO":"Moon","ME":"Mercury","VE":"Venus","MA":"Mars","JU":"Jupiter","SA":"Saturn","RA":"Rahu","KE":"Ketu"}
PLANETS = ["AS","SU","MO","ME","VE","MA","JU","SA","RA","KE"]

result = calculate("Новосибирск", "30.12.1995", "14:30", lat=55.0288, lon=82.9227)
d1 = {"Lagna": result["lagna_abs"]}
for k in ["Sun","Moon","Mercury","Venus","Mars","Jupiter","Saturn","Rahu","Ketu"]:
    d1[k] = result["d1_positions"][k]

def calc_varga_offset(sign_num, deg_in_sign, divisor):
    part_size = 30 / divisor
    part = int(deg_in_sign / part_size)
    d3 = divisor // 3
    offset = (sign_num // 3) * divisor + d3 * (sign_num % 3)
    result_sign = (sign_num + offset + part) % 12
    result_deg = (deg_in_sign % part_size) * divisor
    return result_sign, result_deg

# Test all vargas
for vn in ["D5","D10","D12","D24","D30","D40","D45","D60"]:
    div = int(vn[1:])
    print(f"\n{'='*60}")
    print(f"  {vn} (divisor={div})")
    print(f"{'='*60}")
    passes = 0
    total = 0
    for p in PLANETS:
        s_ref, d_ref = REF[vn][p]
        d1_abs = d1[PVAL[p]]
        s1 = int(d1_abs // 30)
        d1_deg = d1_abs % 30
        s_calc, d_calc = calc_varga_offset(s1, d1_deg, div)
        ok = (s_calc == s_ref) and abs(d_calc - d_ref) < 2
        total += 1
        if ok:
            passes += 1
        else:
            print(f"  {p}: calc sign={s_calc} deg={d_calc:.1f}, ref sign={s_ref} deg={d_ref} {'✅' if ok else '❌'}")
    print(f"  TOTAL: {passes}/{total} {'✅' if passes == total else '❌'}")