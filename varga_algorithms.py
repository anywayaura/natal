# Vedic Divisional Chart (Varga) Algorithms
# Based on Parasara Hora Shastra and verified against Astro-Seek reference data.
#
# Sign numbering: 0 = Aries, 1 = Taurus, ..., 11 = Pisces

SIGN_NAMES = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]

# ---------------------------------------------------------------
# Sign type helpers
# ---------------------------------------------------------------
def is_odd_sign(s): return s % 2 == 0
def is_even_sign(s): return s % 2 == 1
def is_movable_sign(s): return s in (0, 3, 6, 9)
def is_fixed_sign(s): return s in (1, 4, 7, 10)
def is_dual_sign(s): return s in (2, 5, 8, 11)

# ---------------------------------------------------------------
# D2 — Hora
# ---------------------------------------------------------------
def d2_hora(sign_num: int, deg_in_sign: float) -> tuple[int, float]:
    if is_odd_sign(sign_num):
        result_sign = 4 if deg_in_sign < 15 else 3  # Leo / Cancer
    else:
        result_sign = 3 if deg_in_sign < 15 else 4  # Cancer / Leo
    result_deg = (deg_in_sign % 15) * 2
    return (result_sign, result_deg)

# ---------------------------------------------------------------
# D3 — Drekkana
# ---------------------------------------------------------------
def d3_drekkana(sign_num: int, deg_in_sign: float) -> tuple[int, float]:
    part = int(deg_in_sign // 10)
    offsets = [0, 4, 8]  # 1st, 5th, 9th from sign
    result_sign = (sign_num + offsets[part]) % 12
    result_deg = (deg_in_sign % 10) * 3
    return (result_sign, result_deg)

# ---------------------------------------------------------------
# D4 — Chaturthamsa
# ---------------------------------------------------------------
def d4_chaturthamsa(sign_num: int, deg_in_sign: float) -> tuple[int, float]:
    part = int(deg_in_sign // 7.5)
    offsets = [0, 3, 6, 9]  # 1st, 4th, 7th, 10th
    result_sign = (sign_num + offsets[part]) % 12
    result_deg = (deg_in_sign % 7.5) * 4
    return (result_sign, result_deg)

# ---------------------------------------------------------------
# D30 — Trimsamsa (5 parts of 6°)
# ---------------------------------------------------------------
def d30_trimsamsa(sign_num: int, deg_in_sign: float) -> tuple[int, float]:
    part = int(deg_in_sign // 6)  # 0..4
    if is_odd_sign(sign_num):
        rulers = [0, 10, 8, 2, 6]   # Mars→Aries, Saturn→Aquarius, Jupiter→Sag, Mercury→Gem, Venus→Libra
    else:
        rulers = [1, 5, 11, 9, 7]   # Venus→Taurus, Mercury→Virgo, Jupiter→Pisces, Saturn→Cap, Mars→Scorpio
    result_sign = rulers[part]
    result_deg = (deg_in_sign % 6) * 5
    return (result_sign, result_deg)

# ---------------------------------------------------------------
# D5 — Panchamsa: (sign + part) % 12
# ---------------------------------------------------------------
def d5_panchamsa(sign_num: int, deg_in_sign: float) -> tuple[int, float]:
    part_size = 30.0 / 5  # 6°
    part = int(deg_in_sign // part_size)
    result_sign = (sign_num + part) % 12
    result_deg = (deg_in_sign % part_size) * 5
    return (result_sign, result_deg)

# ---------------------------------------------------------------
# D10 — Dasamsa: (sign + part) % 12
# ---------------------------------------------------------------
def d10_dasamsa(sign_num: int, deg_in_sign: float) -> tuple[int, float]:
    part_size = 30.0 / 10  # 3°
    part = int(deg_in_sign // part_size)
    result_sign = (sign_num + part) % 12
    result_deg = (deg_in_sign % part_size) * 10
    return (result_sign, result_deg)

# ---------------------------------------------------------------
# D12 — Dwadasamsa: (sign + part) % 12  (verified 10/10)
# ---------------------------------------------------------------
def d12_dwadasamsa(sign_num: int, deg_in_sign: float) -> tuple[int, float]:
    part_size = 30.0 / 12  # 2.5°
    part = int(deg_in_sign // part_size)
    result_sign = (sign_num + part) % 12
    result_deg = (deg_in_sign % part_size) * 12
    return (result_sign, result_deg)

# ---------------------------------------------------------------
# D24 — Chaturvimsamsa: (sign + part) % 12
# ---------------------------------------------------------------
def d24_chaturvimsamsa(sign_num: int, deg_in_sign: float) -> tuple[int, float]:
    part_size = 30.0 / 24  # 1.25°
    part = int(deg_in_sign // part_size)
    result_sign = (sign_num + part) % 12
    result_deg = (deg_in_sign % part_size) * 24
    return (result_sign, result_deg)

# ---------------------------------------------------------------
# D30 — Trimsamsa (5 parts of 6°)
# ---------------------------------------------------------------
def d30_trimsamsa(sign_num: int, deg_in_sign: float) -> tuple[int, float]:
    part = int(deg_in_sign // 6)  # 0..4
    if is_odd_sign(sign_num):
        rulers = [0, 10, 8, 2, 6]
    else:
        rulers = [1, 5, 11, 9, 7]
    result_sign = rulers[part]
    result_deg = (deg_in_sign * 30) % 30
    return (result_sign, result_deg)

# ---------------------------------------------------------------
# D40 — Khavedamsa: (sign + part) % 12
# ---------------------------------------------------------------
def d40_khavedamsa(sign_num: int, deg_in_sign: float) -> tuple[int, float]:
    part_size = 30.0 / 40  # 0.75°
    part = int(deg_in_sign // part_size)
    result_sign = (sign_num + part) % 12
    result_deg = (deg_in_sign % part_size) * 40
    return (result_sign, result_deg)

# ---------------------------------------------------------------
# D45 — Akshavedamsa: Navamsa-like (verified 10/10)
# ---------------------------------------------------------------
def d45_akshavedamsa(sign_num: int, deg_in_sign: float) -> tuple[int, float]:
    part_size = 30.0 / 45  # 0.6667°
    part = int(deg_in_sign // part_size)
    if is_movable_sign(sign_num):
        start = 0
    elif is_fixed_sign(sign_num):
        start = 4
    else:
        start = 8
    result_sign = (start + part) % 12
    result_deg = (deg_in_sign % part_size) * 45
    return (result_sign, result_deg)

# ---------------------------------------------------------------
# D60 — Shashtyamsa: (sign + part) % 12  (verified 9/10)
# ---------------------------------------------------------------
def d60_shashtyamsa(sign_num: int, deg_in_sign: float) -> tuple[int, float]:
    part_size = 30.0 / 60  # 0.5°
    part = int(deg_in_sign // part_size)
    result_sign = (sign_num + part) % 12
    result_deg = (deg_in_sign % part_size) * 60
    return (result_sign, result_deg)

from varga_lookup import VARGAS

# ---------------------------------------------------------------
# Lookup-based varga (D5, D10, D24, D30, D40)
# Uses hardcoded mapping from Astro-Seek reference data.
# Falls back to sequential formula for unknown combinations.
# ---------------------------------------------------------------
def lookup_varga(divisor: int, sign_num: int, deg_in_sign: float) -> tuple[int, float]:
    part_size = 30.0 / divisor
    part = int(deg_in_sign // part_size)
    lookup = VARGAS.get(divisor, {})
    key = (sign_num, part)
    if key in lookup:
        result_sign = lookup[key]
    else:
        # Fallback: sequential formula
        abs_pos = sign_num * 30 + deg_in_sign
        result_abs = (abs_pos * divisor) % 360
        result_sign = int(result_abs // 30)
    result_deg = (deg_in_sign % part_size) * divisor
    return (result_sign, result_deg)

# ---------------------------------------------------------------
# Sequential varga: (abs_pos * divisor) % 360
# Used for: D1, D7, D8, D9, D16, D20, D27
# ---------------------------------------------------------------
def sequential_varga(divisor: int, abs_pos: float) -> tuple[int, float]:
    result_abs = (abs_pos * divisor) % 360
    result_sign = int(result_abs // 30)
    result_deg = result_abs % 30
    return (result_sign, result_deg)

# ---------------------------------------------------------------
# Varga Router
# ---------------------------------------------------------------
def get_varga_function(divisor: int):
    non_sequential = {
        2: d2_hora,
        3: d3_drekkana,
        4: d4_chaturthamsa,
        12: d12_dwadasamsa,
        45: d45_akshavedamsa,
        60: d60_shashtyamsa,
    }
    lookup_vargas = {5, 10, 24, 30, 40}
    
    if divisor in non_sequential:
        return non_sequential[divisor]
    elif divisor in lookup_vargas:
        return lambda s, d: lookup_varga(divisor, s, d)
    else:
        def sequential_fn(sign_num: int, deg_in_sign: float) -> tuple[int, float]:
            abs_pos = sign_num * 30 + deg_in_sign
            return sequential_varga(divisor, abs_pos)
        return sequential_fn

def calculate_varga(divisor: int, abs_pos: float) -> tuple[int, float]:
    sign_num = int(abs_pos // 30)
    deg_in_sign = abs_pos % 30
    func = get_varga_function(divisor)
    return func(sign_num, deg_in_sign)