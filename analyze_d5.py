"""Parse the 24-hour dataset and find D5 formula."""
import re

SIGN_MAP = {"Ari":0,"Tau":1,"Gem":2,"Can":3,"Leo":4,"Vir":5,"Lib":6,"Sco":7,"Sag":8,"Cap":9,"Aqu":10,"Pis":11}
PLANETS = ["AS","SU","MO","ME","VE","MA","JU","SA","RA","KE"]

with open("dataset 16.03.1989 Novosibirsk") as f:
    text = f.read()

blocks = [b.strip() for b in text.split("\n\n") if b.strip()]
print(f"Found {len(blocks)} blocks")

from natal import calculate
PVAL = {"AS":"Lagna","SU":"Sun","MO":"Moon","ME":"Mercury","VE":"Venus","MA":"Mars","JU":"Jupiter","SA":"Saturn","RA":"Rahu","KE":"Ketu"}

d5_refs = {}  # {hour: {planet: (sign, deg)}}

for block in blocks:
    lines = block.split("\n")
    hour_match = re.match(r"(\d{2}:\d{2})", lines[0])
    if not hour_match:
        continue
    hour = hour_match.group(1)
    
    in_signs = False
    for line in lines:
        if "D1-D60: Signs" in line:
            in_signs = True
            continue
        if not in_signs:
            continue
        if line.strip().startswith("D5"):
            parts = line.split()
            vals = parts[1:]
            d5_refs[hour] = {}
            for i in range(0, len(vals), 2):
                if i+1 < len(vals):
                    sign_str = vals[i]
                    deg_str = vals[i+1]
                    deg_match = re.match(r"(\d+)°", deg_str)
                    if deg_match:
                        planet_idx = i // 2
                        if planet_idx < len(PLANETS):
                            sign = SIGN_MAP.get(sign_str, 0)
                            deg = int(deg_match.group(1))
                            d5_refs[hour][PLANETS[planet_idx]] = (sign, deg)
            break

print(f"Parsed D5 for {len(d5_refs)} hours")

# Collect mappings
mappings = {}
bphs_ok = 0
bphs_total = 0

for hour, planets in sorted(d5_refs.items()):
    h = int(hour[:2])
    r = calculate("Новосибирск", "16.03.1989", f"{h:02d}:00", lat=55.0288, lon=82.9227)
    d1 = {"Lagna": r["lagna_abs"]}
    for k in ["Sun","Moon","Mercury","Venus","Mars","Jupiter","Saturn","Rahu","Ketu"]:
        d1[k] = r["d1_positions"][k]
    
    for p in PLANETS:
        if p not in planets:
            continue
        s_ref, d_ref = planets[p]
        abs_pos = d1[PVAL[p]]
        s1 = int(abs_pos // 30)
        d1_deg = abs_pos % 30
        part = int(d1_deg / 6.0)
        key = (s1, part)
        if key not in mappings:
            mappings[key] = {}
        mappings[key][p] = s_ref
        
        # Test BPHS formula
        bphs_total += 1
        if s1 % 2 == 0:
            start = s1
        else:
            start = (s1 + 8) % 12
        if (start + part) % 12 == s_ref:
            bphs_ok += 1

# Print mapping table
print(f"\nD5 mapping table ({len(mappings)}/60 entries):")
for s1 in range(12):
    row = []
    for part in range(5):
        key = (s1, part)
        if key in mappings:
            vals = set(mappings[key].values())
            if len(vals) == 1:
                row.append(f"{list(vals)[0]:2d}")
            else:
                row.append("XX")
        else:
            row.append(" ?")
    print(f"  sign={s1:2d}: [{', '.join(row)}]")

print(f"\nBPHS formula: {bphs_ok}/{bphs_total}")

# Check conflicts
conflicts = [(k, v) for k, v in mappings.items() if len(set(v.values())) > 1]
if conflicts:
    print(f"\n❌ Conflicts: {len(conflicts)}")
    for k, v in conflicts:
        print(f"  sign={k[0]} part={k[1]}: {v}")
else:
    print(f"\n✅ No conflicts!")

# Brute force: all combinations of offset for odd/even signs
print(f"\nBrute force (odd_offset, even_offset):")
best = (0, 0, 0)
for off_odd in range(12):
    for off_even in range(12):
        ok = 0
        total = 0
        for hour, planets in sorted(d5_refs.items()):
            h = int(hour[:2])
            r = calculate("Новосибирск", "16.03.1989", f"{h:02d}:00", lat=55.0288, lon=82.9227)
            d1 = {"Lagna": r["lagna_abs"]}
            for k in ["Sun","Moon","Mercury","Venus","Mars","Jupiter","Saturn","Rahu","Ketu"]:
                d1[k] = r["d1_positions"][k]
            for p in PLANETS:
                if p not in planets:
                    continue
                s_ref, d_ref = planets[p]
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
        if ok > best[0]:
            best = (ok, off_odd, off_even)
            print(f"  odd_off={off_odd} even_off={off_even}: {ok}/{total}")

print(f"\nBest: odd_off={best[1]} even_off={best[2]}: {best[0]}/{bphs_total}")

# Also try: different start for each sign type (movable/fixed/dual)
print(f"\nBrute force by sign type (movable, fixed, dual):")
best2 = (0, 0, 0, 0)
for sm in range(12):
    for sf in range(12):
        for sd in range(12):
            ok = 0
            total = 0
            for hour, planets in sorted(d5_refs.items()):
                h = int(hour[:2])
                r = calculate("Новосибирск", "16.03.1989", f"{h:02d}:00", lat=55.0288, lon=82.9227)
                d1 = {"Lagna": r["lagna_abs"]}
                for k in ["Sun","Moon","Mercury","Venus","Mars","Jupiter","Saturn","Rahu","Ketu"]:
                    d1[k] = r["d1_positions"][k]
                for p in PLANETS:
                    if p not in planets:
                        continue
                    s_ref, d_ref = planets[p]
                    abs_pos = d1[PVAL[p]]
                    s1 = int(abs_pos // 30)
                    d1_deg = abs_pos % 30
                    part = int(d1_deg / 6.0)
                    total += 1
                    if s1 in (0,3,6,9): start = (s1 + sm) % 12
                    elif s1 in (1,4,7,10): start = (s1 + sf) % 12
                    else: start = (s1 + sd) % 12
                    if (start + part) % 12 == s_ref:
                        ok += 1
            if ok > best2[0]:
                best2 = (ok, sm, sf, sd)
                print(f"  m={sm} f={sf} d={sd}: {ok}/{total}")

print(f"\nBest: m={best2[1]} f={best2[2]} d={best2[3]}: {best2[0]}/{total}")