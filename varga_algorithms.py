# Vedic Divisional Chart (Varga) Algorithms
# Based on Parasara Hora Shastra (BPHS) — verified against Astro-Seek reference data.
#
# Sign numbering: 0 = Aries, 1 = Taurus, ..., 11 = Pisces

SIGN_NAMES = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]

def is_odd_sign(s): return s % 2 == 0
def is_even_sign(s): return s % 2 == 1
def is_movable_sign(s): return s in (0, 3, 6, 9)
def is_fixed_sign(s): return s in (1, 4, 7, 10)
def is_dual_sign(s): return s in (2, 5, 8, 11)

# ==============================================================
# D2 — Hora
# ==============================================================
def d2_hora(sign_num: int, deg_in_sign: float) -> tuple[int, float]:
    if is_odd_sign(sign_num):
        result_sign = 4 if deg_in_sign < 15 else 3
    else:
        result_sign = 3 if deg_in_sign < 15 else 4
    result_deg = (deg_in_sign % 15) * 2
    return (result_sign, result_deg)

# ==============================================================
# D3 — Drekkana
# ==============================================================
def d3_drekkana(sign_num: int, deg_in_sign: float) -> tuple[int, float]:
    part = int(deg_in_sign // 10)
    offsets = [0, 4, 8]
    result_sign = (sign_num + offsets[part]) % 12
    result_deg = (deg_in_sign % 10) * 3
    return (result_sign, result_deg)

# ==============================================================
# D4 — Chaturthamsa
# ==============================================================
def d4_chaturthamsa(sign_num: int, deg_in_sign: float) -> tuple[int, float]:
    part = int(deg_in_sign // 7.5)
    offsets = [0, 3, 6, 9]
    result_sign = (sign_num + offsets[part]) % 12
    result_deg = (deg_in_sign % 7.5) * 4
    return (result_sign, result_deg)

# ==============================================================
# D5 — Panchamsa (BPHS: odd→same sign, even→9th sign)
# ==============================================================
def d5_panchamsa(sign_num: int, deg_in_sign: float) -> tuple[int, float]:
    part_size = 30.0 / 5  # 6°
    part = int(deg_in_sign // part_size)
    if is_odd_sign(sign_num):
        rulers = [0, 10, 8, 2, 6]  # Aries→Aquarius→Sagittarius→Gemini→Libra
    else:
        rulers = [1, 5, 11, 9, 7]  # Taurus→Virgo→Pisces→Capricorn→Scorpio
    result_sign = rulers[part]
    result_deg = (deg_in_sign % part_size) * 5
    return (result_sign, result_deg)

# ==============================================================
# D7 — Saptamsa (sequential: abs*div % 360)
# ==============================================================
def d7_saptamsa(sign_num: int, deg_in_sign: float) -> tuple[int, float]:
    abs_pos = sign_num * 30 + deg_in_sign
    result_abs = (abs_pos * 7) % 360
    result_sign = int(result_abs // 30)
    result_deg = result_abs % 30
    return (result_sign, result_deg)

# ==============================================================
# D8 — Ashtamsa (sequential: abs*div % 360)
# ==============================================================
def d8_ashtamsa(sign_num: int, deg_in_sign: float) -> tuple[int, float]:
    abs_pos = sign_num * 30 + deg_in_sign
    result_abs = (abs_pos * 8) % 360
    result_sign = int(result_abs // 30)
    result_deg = result_abs % 30
    return (result_sign, result_deg)

# ==============================================================
# D9 — Navamsa (sequential: abs*div % 360)
# ==============================================================
def d9_navamsa(sign_num: int, deg_in_sign: float) -> tuple[int, float]:
    abs_pos = sign_num * 30 + deg_in_sign
    result_abs = (abs_pos * 9) % 360
    result_sign = int(result_abs // 30)
    result_deg = result_abs % 30
    return (result_sign, result_deg)

# ==============================================================
# D10 — Dasamsa (BPHS: odd→same sign, even→9th sign)
# ==============================================================
def d10_dasamsa(sign_num: int, deg_in_sign: float) -> tuple[int, float]:
    part_size = 30.0 / 10  # 3°
    part = int(deg_in_sign // part_size)
    if is_odd_sign(sign_num):
        start = sign_num
    else:
        start = (sign_num + 8) % 12  # 9th sign
    result_sign = (start + part) % 12
    result_deg = (deg_in_sign % part_size) * 10
    return (result_sign, result_deg)

# ==============================================================
# D12 — Dwadasamsa: (sign + part) % 12
# ==============================================================
def d12_dwadasamsa(sign_num: int, deg_in_sign: float) -> tuple[int, float]:
    part_size = 30.0 / 12  # 2.5°
    part = int(deg_in_sign // part_size)
    result_sign = (sign_num + part) % 12
    result_deg = (deg_in_sign % part_size) * 12
    return (result_sign, result_deg)

# ==============================================================
# D16 — Shodasamsa (sequential: abs*div % 360)
# ==============================================================
def d16_shodasamsa(sign_num: int, deg_in_sign: float) -> tuple[int, float]:
    abs_pos = sign_num * 30 + deg_in_sign
    result_abs = (abs_pos * 16) % 360
    result_sign = int(result_abs // 30)
    result_deg = result_abs % 30
    return (result_sign, result_deg)

# ==============================================================
# D20 — Vimsamsa (sequential: abs*div % 360)
# ==============================================================
def d20_vimsamsa(sign_num: int, deg_in_sign: float) -> tuple[int, float]:
    abs_pos = sign_num * 30 + deg_in_sign
    result_abs = (abs_pos * 20) % 360
    result_sign = int(result_abs // 30)
    result_deg = result_abs % 30
    return (result_sign, result_deg)

# ==============================================================
# D24 — Chaturvimsamsa (BPHS: odd→Leo, even→Cancer)
# ==============================================================
def d24_chaturvimsamsa(sign_num: int, deg_in_sign: float) -> tuple[int, float]:
    part_size = 30.0 / 24  # 1.25°
    part = int(deg_in_sign // part_size)
    if is_odd_sign(sign_num):
        start = 4  # Leo
    else:
        start = 3  # Cancer
    result_sign = (start + part) % 12
    result_deg = (deg_in_sign % part_size) * 24
    return (result_sign, result_deg)

# ==============================================================
# D27 — Saptavimsamsa (sequential: abs*div % 360)
# ==============================================================
def d27_saptavimsamsa(sign_num: int, deg_in_sign: float) -> tuple[int, float]:
    abs_pos = sign_num * 30 + deg_in_sign
    result_abs = (abs_pos * 27) % 360
    result_sign = int(result_abs // 30)
    result_deg = result_abs % 30
    return (result_sign, result_deg)

# ==============================================================
# D30 — Trimsamsa (BPHS: unequal segments, planetary rulers)
# ==============================================================
def d30_trimsamsa(sign_num: int, deg_in_sign: float) -> tuple[int, float]:
    if is_odd_sign(sign_num):
        # Odd signs: Mars(0-5), Saturn(5-10), Jupiter(10-18), Mercury(18-25), Venus(25-30)
        if deg_in_sign < 5: result_sign = 0   # Mars → Aries
        elif deg_in_sign < 10: result_sign = 10  # Saturn → Aquarius
        elif deg_in_sign < 18: result_sign = 8   # Jupiter → Sagittarius
        elif deg_in_sign < 25: result_sign = 2   # Mercury → Gemini
        else: result_sign = 6                     # Venus → Libra
        # Degree: map the segment to 0-30°
        seg_starts = [0, 5, 10, 18, 25]
        seg_lens = [5, 5, 8, 7, 5]
    else:
        # Even signs: Venus(0-5), Mercury(5-12), Jupiter(12-20), Saturn(20-25), Mars(25-30)
        if deg_in_sign < 5: result_sign = 1   # Venus → Taurus
        elif deg_in_sign < 12: result_sign = 5  # Mercury → Virgo
        elif deg_in_sign < 20: result_sign = 11  # Jupiter → Pisces
        elif deg_in_sign < 25: result_sign = 9   # Saturn → Capricorn
        else: result_sign = 7                     # Mars → Scorpio
        seg_starts = [0, 5, 12, 20, 25]
        seg_lens = [5, 7, 8, 5, 5]
    
    # Find which segment
    abs_pos = sign_num * 30 + deg_in_sign
    for i in range(5):
        if seg_starts[i] <= deg_in_sign < seg_starts[i] + seg_lens[i]:
            result_deg = (abs_pos * 30) % 30
            break
    else:
        result_deg = 0.0
    
    return (result_sign, result_deg)

# ==============================================================
# D40 — Khavedamsa (BPHS: odd→Aries, even→Libra)
# ==============================================================
def d40_khavedamsa(sign_num: int, deg_in_sign: float) -> tuple[int, float]:
    part_size = 30.0 / 40  # 0.75°
    part = int(deg_in_sign // part_size)
    if is_odd_sign(sign_num):
        start = 0  # Aries
    else:
        start = 6  # Libra
    result_sign = (start + part) % 12
    result_deg = (deg_in_sign % part_size) * 40
    return (result_sign, result_deg)

# ==============================================================
# D45 — Akshavedamsa (Navamsa-like)
# ==============================================================
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

# ==============================================================
# D60 — Shashtyamsa: (sign + part) % 12
# ==============================================================
def d60_shashtyamsa(sign_num: int, deg_in_sign: float) -> tuple[int, float]:
    part_size = 30.0 / 60  # 0.5°
    part = int(deg_in_sign // part_size)
    result_sign = (sign_num + part) % 12
    result_deg = (deg_in_sign % part_size) * 60
    return (result_sign, result_deg)

# ==============================================================
# Varga Router
# ==============================================================
def get_varga_function(divisor: int):
    funcs = {
        2: d2_hora,
        3: d3_drekkana,
        4: d4_chaturthamsa,
        5: d5_panchamsa,
        7: d7_saptamsa,
        8: d8_ashtamsa,
        9: d9_navamsa,
        10: d10_dasamsa,
        12: d12_dwadasamsa,
        16: d16_shodasamsa,
        20: d20_vimsamsa,
        24: d24_chaturvimsamsa,
        27: d27_saptavimsamsa,
        30: d30_trimsamsa,
        40: d40_khavedamsa,
        45: d45_akshavedamsa,
        60: d60_shashtyamsa,
    }
    return funcs.get(divisor)

def calculate_varga(divisor: int, abs_pos: float) -> tuple[int, float]:
    sign_num = int(abs_pos // 30)
    deg_in_sign = abs_pos % 30
    func = get_varga_function(divisor)
    if func is None:
        # Fallback: sequential
        result_abs = (abs_pos * divisor) % 360
        return (int(result_abs // 30), result_abs % 30)
    return func(sign_num, deg_in_sign)