"""Canadian provincial/territorial tax configurations for 2025/2026.

Each province defines: tax brackets, basic personal amount (BPA),
lowest bracket rate, and optional surtax/health premium functions.
"""

from decimal import Decimal


def _build_brackets(rates_and_thresholds):
    """Convert (threshold, rate) pairs into (threshold, rate, constant) tuples.

    The constant K for each bracket is computed per T4127 formula:
    K_n = sum of (V_{i+1} - V_i) * T_i for all brackets below n.
    """
    brackets = []
    cumulative_k = Decimal('0')
    for i, (threshold, rate) in enumerate(rates_and_thresholds):
        brackets.append((Decimal(str(threshold)), Decimal(str(rate)), cumulative_k.quantize(Decimal('0.01'))))
        if i < len(rates_and_thresholds) - 1:
            next_rate = Decimal(str(rates_and_thresholds[i + 1][1]))
            cumulative_k += (next_rate - Decimal(str(rate))) * Decimal(str(threshold))
    return brackets


# Ontario
ONTARIO = {
    'name': 'Ontario',
    'code': 'ON',
    'bpa': Decimal('12989.00'),
    'lowest_rate': Decimal('0.0505'),
    'brackets': _build_brackets([
        (53359, '0.0505'),
        (106717, '0.0915'),
        (150000, '0.1116'),
        (220000, '0.1216'),
        (999999999, '0.1316'),
    ]),
    'has_health_premium': True,
    'has_surtax': True,
}

# British Columbia
BRITISH_COLUMBIA = {
    'name': 'British Columbia',
    'code': 'BC',
    'bpa': Decimal('12580.00'),
    'lowest_rate': Decimal('0.0506'),
    'brackets': _build_brackets([
        (47937, '0.0506'),
        (95875, '0.0770'),
        (110076, '0.1050'),
        (133664, '0.1229'),
        (181232, '0.1470'),
        (252752, '0.1680'),
        (999999999, '0.2050'),
    ]),
    'has_health_premium': False,
    'has_surtax': False,
}

# Alberta
ALBERTA = {
    'name': 'Alberta',
    'code': 'AB',
    'bpa': Decimal('21003.00'),
    'lowest_rate': Decimal('0.1000'),
    'brackets': _build_brackets([
        (148269, '0.1000'),
        (177922, '0.1200'),
        (237230, '0.1300'),
        (355845, '0.1400'),
        (999999999, '0.1500'),
    ]),
    'has_health_premium': False,
    'has_surtax': False,
}

# Manitoba
MANITOBA = {
    'name': 'Manitoba',
    'code': 'MB',
    'bpa': Decimal('15780.00'),
    'lowest_rate': Decimal('0.1080'),
    'brackets': _build_brackets([
        (47000, '0.1080'),
        (100000, '0.1275'),
        (999999999, '0.1740'),
    ]),
    'has_health_premium': False,
    'has_surtax': False,
}

# Saskatchewan
SASKATCHEWAN = {
    'name': 'Saskatchewan',
    'code': 'SK',
    'bpa': Decimal('18491.00'),
    'lowest_rate': Decimal('0.1050'),
    'brackets': _build_brackets([
        (52057, '0.1050'),
        (148734, '0.1250'),
        (999999999, '0.1450'),
    ]),
    'has_health_premium': False,
    'has_surtax': False,
}

# Quebec (note: Quebec has its own tax system with federal abatement)
QUEBEC = {
    'name': 'Quebec',
    'code': 'QC',
    'bpa': Decimal('18056.00'),
    'lowest_rate': Decimal('0.1400'),
    'brackets': _build_brackets([
        (51780, '0.1400'),
        (103545, '0.1900'),
        (126000, '0.2400'),
        (999999999, '0.2575'),
    ]),
    'has_health_premium': False,
    'has_surtax': False,
}

# New Brunswick
NEW_BRUNSWICK = {
    'name': 'New Brunswick',
    'code': 'NB',
    'bpa': Decimal('13044.00'),
    'lowest_rate': Decimal('0.0940'),
    'brackets': _build_brackets([
        (49958, '0.0940'),
        (99916, '0.1400'),
        (185064, '0.1600'),
        (999999999, '0.1950'),
    ]),
    'has_health_premium': False,
    'has_surtax': False,
}

# Nova Scotia
NOVA_SCOTIA = {
    'name': 'Nova Scotia',
    'code': 'NS',
    'bpa': Decimal('8481.00'),
    'lowest_rate': Decimal('0.0879'),
    'brackets': _build_brackets([
        (29590, '0.0879'),
        (59180, '0.1495'),
        (93000, '0.1667'),
        (150000, '0.1750'),
        (999999999, '0.2100'),
    ]),
    'has_health_premium': False,
    'has_surtax': True,
}

# Prince Edward Island
PEI = {
    'name': 'Prince Edward Island',
    'code': 'PE',
    'bpa': Decimal('13500.00'),
    'lowest_rate': Decimal('0.0965'),
    'brackets': _build_brackets([
        (32656, '0.0965'),
        (64313, '0.1363'),
        (105000, '0.1665'),
        (999999999, '0.1800'),
    ]),
    'has_health_premium': False,
    'has_surtax': True,
}

# Newfoundland and Labrador
NEWFOUNDLAND = {
    'name': 'Newfoundland and Labrador',
    'code': 'NL',
    'bpa': Decimal('10818.00'),
    'lowest_rate': Decimal('0.0870'),
    'brackets': _build_brackets([
        (43198, '0.0870'),
        (86395, '0.1450'),
        (154244, '0.1580'),
        (215943, '0.1780'),
        (275870, '0.1980'),
        (551739, '0.2080'),
        (999999999, '0.2180'),
    ]),
    'has_health_premium': False,
    'has_surtax': False,
}

# Yukon
YUKON = {
    'name': 'Yukon',
    'code': 'YT',
    'bpa': Decimal('16129.00'),
    'lowest_rate': Decimal('0.0640'),
    'brackets': _build_brackets([
        (57375, '0.0640'),
        (114750, '0.0900'),
        (177882, '0.1090'),
        (500000, '0.1280'),
        (999999999, '0.1500'),
    ]),
    'has_health_premium': False,
    'has_surtax': True,
}

# Northwest Territories
NWT = {
    'name': 'Northwest Territories',
    'code': 'NT',
    'bpa': Decimal('17373.00'),
    'lowest_rate': Decimal('0.0590'),
    'brackets': _build_brackets([
        (50597, '0.0590'),
        (101198, '0.0860'),
        (164525, '0.1220'),
        (999999999, '0.1405'),
    ]),
    'has_health_premium': False,
    'has_surtax': False,
}

# Nunavut
NUNAVUT = {
    'name': 'Nunavut',
    'code': 'NU',
    'bpa': Decimal('18767.00'),
    'lowest_rate': Decimal('0.0400'),
    'brackets': _build_brackets([
        (53268, '0.0400'),
        (106537, '0.0700'),
        (173205, '0.0900'),
        (999999999, '0.1150'),
    ]),
    'has_health_premium': False,
    'has_surtax': False,
}


# Province lookup by code
PROVINCES = {
    'ON': ONTARIO,
    'BC': BRITISH_COLUMBIA,
    'AB': ALBERTA,
    'MB': MANITOBA,
    'SK': SASKATCHEWAN,
    'QC': QUEBEC,
    'NB': NEW_BRUNSWICK,
    'NS': NOVA_SCOTIA,
    'PE': PEI,
    'NL': NEWFOUNDLAND,
    'YT': YUKON,
    'NT': NWT,
    'NU': NUNAVUT,
}

# Ordered list for UI dropdown
PROVINCE_LIST = [
    ('AB', 'Alberta'),
    ('BC', 'British Columbia'),
    ('MB', 'Manitoba'),
    ('NB', 'New Brunswick'),
    ('NL', 'Newfoundland and Labrador'),
    ('NS', 'Nova Scotia'),
    ('NT', 'Northwest Territories'),
    ('NU', 'Nunavut'),
    ('ON', 'Ontario'),
    ('PE', 'Prince Edward Island'),
    ('QC', 'Quebec'),
    ('SK', 'Saskatchewan'),
    ('YT', 'Yukon'),
]


def get_surtax(province_code, base_tax):
    """Calculate provincial surtax if applicable."""
    if province_code == 'ON':
        # Ontario surtax
        if base_tax <= Decimal('5818'):
            return Decimal('0')
        elif base_tax <= Decimal('7446'):
            return Decimal('0.20') * (base_tax - Decimal('5818'))
        else:
            return Decimal('0.20') * (base_tax - Decimal('5818')) + Decimal('0.36') * (base_tax - Decimal('7446'))

    elif province_code == 'NS':
        # Nova Scotia surtax: 10% of provincial tax over $10,000
        if base_tax <= Decimal('10000'):
            return Decimal('0')
        return Decimal('0.10') * (base_tax - Decimal('10000'))

    elif province_code == 'PE':
        # PEI surtax: 10% of provincial tax over $12,500
        if base_tax <= Decimal('12500'):
            return Decimal('0')
        return Decimal('0.10') * (base_tax - Decimal('12500'))

    elif province_code == 'YT':
        # Yukon surtax: 5% of territorial tax over $6,000
        if base_tax <= Decimal('6000'):
            return Decimal('0')
        return Decimal('0.05') * (base_tax - Decimal('6000'))

    return Decimal('0')


def get_health_premium(province_code, annual_income):
    """Calculate provincial health premium if applicable."""
    if province_code == 'ON':
        A = annual_income
        if A <= Decimal('20000'):
            return Decimal('0')
        elif A <= Decimal('36000'):
            return min(Decimal('300'), Decimal('0.06') * (A - Decimal('20000')))
        elif A <= Decimal('48000'):
            return min(Decimal('450'), Decimal('300') + Decimal('0.06') * (A - Decimal('36000')))
        elif A <= Decimal('72000'):
            return min(Decimal('600'), Decimal('450') + Decimal('0.25') * (A - Decimal('48000')))
        elif A <= Decimal('200000'):
            return min(Decimal('750'), Decimal('600') + Decimal('0.25') * (A - Decimal('72000')))
        else:
            return min(Decimal('900'), Decimal('750') + Decimal('0.25') * (A - Decimal('200000')))

    return Decimal('0')
