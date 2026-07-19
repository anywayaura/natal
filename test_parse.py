"""Quick test on first 55 lines."""
import re

SIGN_MAP = {"Ari":0,"Tau":1,"Gem":2,"Can":3,"Leo":4,"Vir":5,"Lib":6,"Sco":7,"Sag":8,"Cap":9,"Aqu":10,"Pis":11}
PLANETS = ["AS","SU","MO","ME","VE","MA","JU","SA","RA","KE"]

with open("dataset 16.03.1989 Novosibirsk") as f:
    text = f.read()

blocks = [b.strip() for b in text.split("\n\n") if b.strip()]
b = blocks[0]
lines = b.split("\n")

# Find D5
for line in lines:
    if line.strip().startswith("D5"):
        parts = line.split()
        # parts[0] = 'D5', then sign+deg pairs
        vals = parts[1:]
        # Combine: parts[1] + parts[2] = 'Sag 26°', etc.
        data = {}
        for i in range(0, len(vals), 2):
            if i+1 < len(vals):
                sign_str = vals[i]
                deg_str = vals[i+1]
                deg_match = re.match(r"(\d+)°", deg_str)
                if deg_match:
                    sign = SIGN_MAP.get(sign_str, 0)
                    deg = int(deg_match.group(1))
                    planet_idx = i // 2
                    if planet_idx < len(PLANETS):
                        data[PLANETS[planet_idx]] = (sign, deg)
        
        print(f"Parsed {len(data)} planets:")
        for p, (s, d) in data.items():
            print(f"  {p}: sign={s} deg={d}")
        break