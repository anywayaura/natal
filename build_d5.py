"""Build complete D5 formula from 24-hour dataset."""
import re
from collections import Counter

SIGN_MAP = {"Ari":0,"Tau":1,"Gem":2,"Can":3,"Leo":4,"Vir":5,"Lib":6,"Sco":7,"Sag":8,"Cap":9,"Aqu":10,"Pis":11}
PLANETS = ["AS","SU","MO","ME","VE","MA","JU","SA","RA","KE"]

with open("dataset 16.03.1989 Novosibirsk") as f:
    text = f.read()

blocks = [b.strip() for b in text.split("\n\n") if b.strip()]

from natal import calculate
PVAL = {"AS":"Lagna","SU":"Sun","MO":"Moon","ME":"Mercury","VE":"Venus","MA":"Mars","JU":"Jupiter","SA":"Saturn","RA":"Rahu","KE":"Ketu"}

# Collect ALL (sign, part) -> {varga_sign} counts
vote = {}  # (sign, part) -> Counter of varga_signs

for block in blocks:
    lines = block.split("\n")
    hour_match = re.match(r"(\d{2}:\d{2})", lines[0])
    if not hour_match:
        continue
    hour = hour_match.group(1)
    h = int(hour[:2])
    
    # Skip getting D1 at this hour - too slow. Instead, use the fact that
    # planets move slowly. We'll calculate D1 once and adjust.
    
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
            # Parse sign+deg pairs
            for i in range(0, len(vals), 2):
                if i+1 < len(vals):
                    sign_str = vals[i]
                    deg_str = vals[i+1]
                    deg_match = re.match(r"(\d+)°", deg_str)
                    if deg_match:
                        planet_idx = i // 2
                        if planet_idx < len(PLANETS):
                            p = PLANETS[planet_idx]
                            sign = SIGN_MAP.get(sign_str, 0)
                            deg = int(deg_match.group(1))
                            
                            # Calculate D1 position for this planet at this hour
                            r = calculate("Новосибирск", "16.03.1989", f"{h:02d}:00", lat=55.0288, lon=82.9227)
                            d1_abs = r["lagna_abs"] if p == "AS" else r["d1_positions"][PVAL[p]]
                            s1 = int(d1_abs // 30)
                            d1_deg = d1_abs % 30
                            d5_part = int(d1_deg / 6.0)
                            
                            key = (s1, d5_part)
                            if key not in vote:
                                vote[key] = Counter()
                            vote[key][sign] += 1
            break

print(f"Collected {len(vote)} unique (sign, part) combinations")

# Print the majority vote table
print("\nD5 formula from data:")
print("VARGAS_5 = {")
for s1 in range(12):
    for part in range(5):
        key = (s1, part)
        if key in vote:
            c = vote[key]
            best_sign = c.most_common(1)[0][0]
            total = sum(c.values())
            conflicts = len(c)
            if conflicts > 1:
                print(f"    ({s1}, {part}): {best_sign},  # {c.most_common()}")
            else:
                print(f"    ({s1}, {part}): {best_sign},")
        else:
            print(f"    ({s1}, {part}): 0,  # NO DATA")

print("}")

# Check if there's a pattern
print("\n\nPattern analysis:")
for s1 in range(12):
    row = []
    for part in range(5):
        key = (s1, part)
        if key in vote:
            best = vote[key].most_common(1)[0][0]
            row.append(str(best))
        else:
            row.append("?")
    print(f"  sign={s1:2d}: [{', '.join(row)}]")