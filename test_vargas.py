"""
Comprehensive test suite for Varga (Divisional Chart) calculations.
Tests against Astro-Seek reference data for:
  Date: 30.12.1995, 14:30, Novosibirsk
  Lahiri ayanamsha, Sidereal, Placidus houses

Planet abbreviations:
  AS = Lagna (Ascendant)
  SU = Sun    MO = Moon    ME = Mercury
  VE = Venus  MA = Mars    JU = Jupiter
  SA = Saturn RA = Rahu    KE = Ketu

Sign numbers: 0=Aries, 1=Taurus, 2=Gemini, 3=Cancer, 4=Leo, 5=Virgo,
              6=Libra, 7=Scorpio, 8=Sagittarius, 9=Capricorn, 10=Aquarius, 11=Pisces
"""

# Reference data from Astro-Seek: sign_number and degree for each planet in each varga
# Format: (sign, degree)

REFERENCE_SIGNS = {
    "D1": {
        "AS": (1, 23), "SU": (8, 14), "MO": (0, 2), "ME": (9, 3), "VE": (9, 16),
        "MA": (8, 29), "JU": (8, 5), "SA": (10, 25), "RA": (5, 28), "KE": (11, 28),
    },
    "D2": {
        "AS": (4, 16), "SU": (4, 28), "MO": (4, 5), "ME": (3, 6), "VE": (4, 3),
        "MA": (3, 28), "JU": (4, 10), "SA": (3, 20), "RA": (4, 27), "KE": (4, 27),
    },
    "D3": {
        "AS": (9, 9), "SU": (0, 13), "MO": (0, 7), "ME": (9, 9), "VE": (1, 20),
        "MA": (4, 27), "JU": (8, 15), "SA": (6, 16), "RA": (1, 26), "KE": (7, 26),
    },
    "D4": {
        "AS": (10, 2), "SU": (11, 27), "MO": (0, 10), "ME": (9, 13), "VE": (3, 7),
        "MA": (5, 26), "JU": (8, 21), "SA": (7, 11), "RA": (2, 24), "KE": (8, 24),
    },
    "D5": {
        "AS": (9, 25), "SU": (8, 11), "MO": (0, 13), "ME": (1, 16), "VE": (11, 23),
        "MA": (6, 25), "JU": (0, 26), "SA": (6, 7), "RA": (7, 23), "KE": (7, 23),
    },
    # D6 — shashtamsa (not in our list, skip)
    "D7": {
        "AS": (0, 11), "SU": (11, 10), "MO": (0, 18), "ME": (3, 23), "VE": (6, 27),
        "MA": (2, 23), "JU": (9, 7), "SA": (3, 28), "RA": (5, 21), "KE": (11, 21),
    },
    "D8": {
        "AS": (2, 4), "SU": (7, 24), "MO": (0, 21), "ME": (0, 26), "VE": (4, 14),
        "MA": (11, 22), "JU": (5, 12), "SA": (2, 23), "RA": (11, 19), "KE": (11, 19),
    },
    "D9": {
        "AS": (3, 27), "SU": (4, 9), "MO": (0, 23), "ME": (9, 29), "VE": (2, 1),
        "MA": (8, 21), "JU": (1, 17), "SA": (1, 19), "RA": (5, 18), "KE": (11, 18),
    },
    "D10": {
        "AS": (4, 20), "SU": (0, 23), "MO": (0, 26), "ME": (6, 3), "VE": (10, 17),
        "MA": (5, 20), "JU": (9, 23), "SA": (6, 14), "RA": (10, 17), "KE": (4, 17),
    },
    # D11 — not in our list
    "D12": {
        "AS": (10, 6), "SU": (1, 22), "MO": (1, 1), "ME": (10, 9), "VE": (3, 21),
        "MA": (7, 19), "JU": (10, 3), "SA": (8, 5), "RA": (4, 14), "KE": (10, 14),
    },
    # D16
    "D16": {
        "AS": (4, 8), "SU": (3, 19), "MO": (1, 12), "ME": (1, 23), "VE": (8, 28),
        "MA": (11, 15), "JU": (10, 24), "SA": (5, 17), "RA": (11, 9), "KE": (11, 9),
    },
    # D20
    "D20": {
        "AS": (11, 10), "SU": (1, 17), "MO": (1, 22), "ME": (2, 6), "VE": (11, 5),
        "MA": (11, 11), "JU": (7, 16), "SA": (0, 29), "RA": (11, 4), "KE": (11, 4),
    },
    # D24
    "D24": {
        "AS": (9, 12), "SU": (3, 14), "MO": (6, 3), "ME": (5, 19), "VE": (4, 13),
        "MA": (3, 8), "JU": (8, 7), "SA": (0, 11), "RA": (1, 29), "KE": (1, 29),
    },
    # D27
    "D27": {
        "AS": (11, 21), "SU": (0, 27), "MO": (2, 11), "ME": (5, 29), "VE": (6, 3),
        "MA": (2, 5), "JU": (4, 23), "SA": (4, 28), "RA": (4, 25), "KE": (10, 25),
    },
    # D30
    "D30": {
        "AS": (9, 0), "SU": (8, 10), "MO": (0, 19), "ME": (1, 9), "VE": (11, 23),
        "MA": (6, 2), "JU": (10, 9), "SA": (6, 14), "RA": (7, 21), "KE": (7, 21),
    },
    # D40
    "D40": {
        "AS": (0, 20), "SU": (7, 4), "MO": (3, 15), "ME": (10, 13), "VE": (4, 11),
        "MA": (2, 23), "JU": (7, 2), "SA": (9, 29), "RA": (8, 8), "KE": (8, 8),
    },
    # D45
    "D45": {
        "AS": (2, 15), "SU": (5, 16), "MO": (3, 28), "ME": (4, 29), "VE": (1, 5),
        "MA": (3, 18), "JU": (3, 28), "SA": (6, 6), "RA": (3, 2), "KE": (3, 2),
    },
    # D60
    "D60": {
        "AS": (11, 0), "SU": (0, 21), "MO": (5, 8), "ME": (3, 19), "VE": (6, 17),
        "MA": (6, 5), "JU": (6, 18), "SA": (0, 29), "RA": (2, 13), "KE": (8, 13),
    },
}

# Astro-Seek reference: house number (1-based) for each planet in each varga
REFERENCE_HOUSES = {
    "D1":  {"AS": 1, "SU": 8, "MO": 12, "ME": 9, "VE": 9, "MA": 8, "JU": 8, "SA": 10, "RA": 5, "KE": 11},
    "D2":  {"AS": 1, "SU": 1, "MO": 1,  "ME": 12, "VE": 1, "MA": 12, "JU": 1, "SA": 12, "RA": 1, "KE": 1},
    "D3":  {"AS": 1, "SU": 4, "MO": 4,  "ME": 1, "VE": 5, "MA": 8,  "JU": 12, "SA": 10, "RA": 5, "KE": 11},
    "D4":  {"AS": 1, "SU": 2, "MO": 3,  "ME": 12, "VE": 6, "MA": 8,  "JU": 11, "SA": 10, "RA": 5, "KE": 11},
    "D5":  {"AS": 1, "SU": 12, "MO": 4, "ME": 5, "VE": 3, "MA": 10, "JU": 4, "SA": 10, "RA": 11, "KE": 11},
    "D7":  {"AS": 1, "SU": 12, "MO": 1, "ME": 4, "VE": 7, "MA": 3,  "JU": 10, "SA": 4,  "RA": 6,  "KE": 12},
    "D8":  {"AS": 1, "SU": 6, "MO": 11, "ME": 11, "VE": 3, "MA": 10, "JU": 4, "SA": 1,  "RA": 10, "KE": 10},
    "D9":  {"AS": 1, "SU": 2, "MO": 10, "ME": 7, "VE": 12, "MA": 6,  "JU": 11, "SA": 11, "RA": 3,  "KE": 9},
    "D10": {"AS": 1, "SU": 9, "MO": 9, "ME": 3, "VE": 7,  "MA": 2,  "JU": 6,  "SA": 3,  "RA": 7,  "KE": 1},
    "D12": {"AS": 1, "SU": 4, "MO": 4, "ME": 1, "VE": 6,  "MA": 10, "JU": 1, "SA": 11, "RA": 7,  "KE": 1},
    "D16": {"AS": 1, "SU": 12, "MO": 10, "ME": 10, "VE": 5, "MA": 8,  "JU": 7, "SA": 2,  "RA": 8,  "KE": 8},
    "D20": {"AS": 1, "SU": 3, "MO": 3, "ME": 4, "VE": 1, "MA": 1,  "JU": 9, "SA": 2,  "RA": 1,  "KE": 1},
    "D24": {"AS": 1, "SU": 7, "MO": 10, "ME": 9, "VE": 8, "MA": 7,  "JU": 12, "SA": 4,  "RA": 5,  "KE": 5},
    "D27": {"AS": 1, "SU": 2, "MO": 4, "ME": 7, "VE": 8, "MA": 4,  "JU": 6, "SA": 6,  "RA": 6,  "KE": 12},
    "D30": {"AS": 1, "SU": 12, "MO": 4, "ME": 5, "VE": 3, "MA": 10, "JU": 2, "SA": 10, "RA": 11, "KE": 11},
    "D40": {"AS": 1, "SU": 8, "MO": 4, "ME": 11, "VE": 5, "MA": 3,  "JU": 8, "SA": 10, "RA": 9,  "KE": 9},
    "D45": {"AS": 1, "SU": 4, "MO": 2, "ME": 3, "VE": 12, "MA": 2, "JU": 2, "SA": 5,  "RA": 2,  "KE": 2},
    "D60": {"AS": 1, "SU": 2, "MO": 7, "ME": 5, "VE": 8, "MA": 8,  "JU": 8, "SA": 2,  "RA": 4,  "KE": 10},
}

PLANET_MAP = {
    "AS": "Lagna",
    "SU": "Sun",
    "MO": "Moon",
    "ME": "Mercury",
    "VE": "Venus",
    "MA": "Mars",
    "JU": "Jupiter",
    "SA": "Saturn",
    "RA": "Rahu",
    "KE": "Ketu",
}

# Reverse mapping
PLANET_RMAP = {v: k for k, v in PLANET_MAP.items()}


def test_varga(result, varga_divisor, tolerance=2.0):
    """Test a single varga against reference data.
    Returns (passed, total, failures) where failures is a list of messages."""
    varga_name = f"D{varga_divisor}"
    if varga_name not in REFERENCE_SIGNS:
        return None, 0, []
    
    ref = REFERENCE_SIGNS[varga_name]
    houses_ref = REFERENCE_HOUSES.get(varga_name, {})
    
    # Find the varga in our result
    varga_result = None
    for v in result["vargas"]:
        if v["divisor"] == varga_divisor:
            varga_result = v
            break
    
    if varga_result is None:
        return False, len(ref), [f"{varga_name}: varga not found in result"]
    
    chart = varga_result["chart"]
    lagna_sign = result["lagna_sign"]
    lagna_abs = result["lagna_abs"]
    
    failures = []
    passed = 0
    
    for ref_key, (ref_sign, ref_deg) in ref.items():
        planet = PLANET_MAP[ref_key]
        if planet not in chart:
            failures.append(f"{varga_name} {ref_key}: planet not in chart")
            continue
        
        d = chart[planet]
        our_sign = d["sign_num"]
        our_deg = d["degree"]
        
        # Check sign match
        sign_ok = our_sign == ref_sign
        
        # Check degree match (within tolerance)
        # Reference degrees are rounded to integers, so compare with tolerance
        deg_diff = abs(our_deg - ref_deg)
        deg_ok = deg_diff <= tolerance or (deg_diff > 30 - tolerance and abs(our_deg - ref_deg - 360) <= tolerance)
        
        if sign_ok and deg_ok:
            passed += 1
        elif not sign_ok:
            failures.append(
                f"{varga_name} {ref_key}: sign mismatch — got {our_sign} ({our_deg:.1f}°), "
                f"expected {ref_sign} ({ref_deg}°)"
            )
        else:
            failures.append(
                f"{varga_name} {ref_key}: degree mismatch — got {our_deg:.1f}°, "
                f"expected {ref_deg}° (diff={deg_diff:.1f})"
            )
    
    return passed, len(ref), failures


def run_all_tests(verbose=False):
    """Run tests for all vargas."""
    from natal import calculate
    
    result = calculate("Новосибирск", "30.12.1995", "14:30", lat=55.0288, lon=82.9227)
    
    print(f"Лагна: Taurus {result['lagna_degree']:.2f}°")
    print(f"Планеты D1:")
    for name in ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Rahu", "Ketu"]:
        pos = result["d1_positions"][name]
        s = int(pos // 30)
        d = pos % 30
        print(f"  {name:8s}: sign={s} deg={d:.2f}")
    print()
    
    # Test all vargas that have reference data
    varga_divisors = [1, 2, 3, 4, 5, 7, 8, 9, 10, 12, 16, 20, 24, 27, 30, 40, 45, 60]
    
    total_passed = 0
    total_tests = 0
    all_failures = []
    
    for div in varga_divisors:
        vn = f"D{div}"
        if vn not in REFERENCE_SIGNS:
            continue
        
        passed, total, failures = test_varga(result, div)
        if passed is None:
            continue
        
        total_passed += passed
        total_tests += total
        
        status = "✅" if passed == total else "❌"
        print(f"{status} {vn}: {passed}/{total} passed")
        
        if failures and verbose:
            for f in failures:
                print(f"       {f}")
        elif failures:
            all_failures.extend(failures)
    
    print(f"\n{'='*50}")
    print(f"Итого: {total_passed}/{total_tests} тестов пройдено")
    
    if all_failures and not verbose:
        print(f"\nПервые 10 ошибок:")
        for f in all_failures[:10]:
            print(f"  {f}")
    
    if total_passed == total_tests:
        print("\n🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ!")
    else:
        print(f"\n❌ ПРОВАЛЕНО: {total_tests - total_passed} тестов")
    
    return total_passed == total_tests


if __name__ == "__main__":
    run_all_tests(verbose=True)