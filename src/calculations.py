"""
Chemistry Calculations Module for the pH Calculator.
Contains functions for calculating pH values and other related calculations.
"""
import math

# ============================
# Constants
# ============================

# Water ion product
KW = 1e-14

# Acid dissociation constants (Ka)
KA_HC2H3O2 = 1.8e-5  # Acetic acid
KA_H2CO3 = 4.3e-7  # Carbonic acid
KA_HCO3 = 5.6e-11  # For NaHCO3 (basic salt of H2CO3)
KA_H2PO4 = 6.2e-8  # For NaH2PO4 (acidic salt)
KA_HSO4 = 1.2e-2  # For NaHSO4 (acidic salt of H2SO4)

# Base dissociation constant (Kb)
KB_NH3 = 1.8e-5  # For NH3 (as in ammonium hydroxide)

# pKa values
pKA_HC2H3O2 = 4.745
pKA_NH4Cl = 9.255
pKA_NaH2PO4 = 7.208
pKA_NaHCO3 = 10.252
pKA_H2CO3 = 6.367


# ============================
# Utility functions
# ============================

def ph_from_h_concentration(h_conc):
    """
    Calculate pH given [H+].
    pH = -log10([H+])
    """
    return -math.log10(h_conc)


# ============================
# pH Calculations for Acids and Bases
# ============================

def h_conc_baoh2(conc):
    """
    For Ba(OH)2 (Barium Hydroxide, a strong base):
    [H+] = KW / (2 * conc)
    """
    return KW / (2 * conc)


def h_conc_caoh2(conc):
    """
    For Ca(OH)2 (Calcium Hydroxide, a strong base):
    [H+] = KW / (2 * conc)
    """
    return KW / (2 * conc)


def h_conc_naoh(conc):
    """
    For NaOH (Sodium Hydroxide, a strong base):
    [H+] = KW / conc
    """
    return KW / conc


def h_conc_nhamoh(conc):
    """
    For NH4OH (Ammonium Hydroxide, a weak base with KB = 1.8e-5):
    [H+] = KW / sqrt(KB_NH3 * conc)
    """
    return KW / math.sqrt(KB_NH3 * conc)


def h_conc_hcl(conc):
    """
    For HCl (Hydrochloric Acid, a strong acid):
    [H+] = conc
    """
    return conc


def h_conc_hno3(conc):
    """
    For HNO3 (Nitric Acid, a strong acid):
    [H+] = conc
    """
    return conc


def h_conc_hc2h3o2(conc):
    """
    For HC2H3O2 (Acetic Acid, a weak acid with KA = 1.8e-5):
    [H+] = sqrt(KA_HC2H3O2 * conc)
    """
    return math.sqrt(KA_HC2H3O2 * conc)


def h_conc_h2co3(conc):
    """
    For H2CO3 (Carbonic Acid, a weak acid with KA = 4.3e-7):
    [H+] = sqrt(KA_H2CO3 * conc)
    """
    return math.sqrt(KA_H2CO3 * conc)


def ph_nacl():
    """
    For NaCl (Sodium Chloride, a neutral salt):
    pH = 7.00
    """
    return 7.00


def h_conc_nhg(conc):
    """
    For NH4G (Ammonium Chloride, an acidic salt of NH3):
    [H+] = sqrt((KW / KB_NH3) * conc)
    (Note: KW/KB_NH3 ≈ 5.56e-10)
    """
    return math.sqrt((KW / KB_NH3) * conc)


def h_conc_nac2h3o2(conc):
    """
    For NaC2H3O2 (Sodium Acetate, a basic salt of acetic acid):
    [H+] = KW / sqrt((KW / KA_HC2H3O2) * conc)
    """
    return KW / math.sqrt((KW / KA_HC2H3O2) * conc)


def h_conc_nahco3(conc):
    """
    For NaHCO3 (Sodium Bicarbonate, a basic salt of H2CO3):
    [H+] = KW / sqrt((KW / KA_H2CO3) * conc)
    (KW/KA_H2CO3 is approximately 2.33e-8)
    """
    return KW / math.sqrt((KW / KA_H2CO3) * conc)


def h_conc_na2co3(conc):
    """
    For Na2CO3 (Sodium Carbonate, a basic salt of HCO3-):
    [H+] = KW / sqrt((KW / KA_HCO3) * conc)
    (KW/KA_HCO3 is approximately 1.79e-4)
    """
    return KW / math.sqrt((KW / KA_HCO3) * conc)


def h_conc_nahso4(conc):
    """
    For NaHSO4 (Sodium Bisulfate, an acidic salt of H2SO4):
    [H+] = sqrt(KA_HSO4 * conc)
    """
    return math.sqrt(KA_HSO4 * conc)


# ============================
# Water and Titration Calculations
# ============================

# Constant for drop volume (assumed units consistent with volume used, e.g. mL)
DROP_VOLUME = 0.036


def total_volume(initial_volume, drops):
    """
    Calculate total volume after adding a number of drops.

    total_volume = initial_volume + (drop_volume * drops)
    """
    return initial_volume + (DROP_VOLUME * drops)


def h_conc_titration_general(drop_molarity, drops, initial_volume=10.000, addition='acid'):
    if addition == 'acid':
        return h_conc_titration_hcl(drop_molarity, drops, initial_volume)
    if addition == 'base':
        return h_conc_titration_naoh(drop_molarity, drops, initial_volume)


def h_conc_titration_hcl(drop_molarity, drops, initial_volume=10.000):
    """
    For titrating water with HCl (.1 or .01 M):
    [H+] = (molarity * volume_added / total_volume) + 1e-7

    volume_added = DROP_VOLUME * drops
    total_volume = initial_volume + volume_added
    """
    volume_added = DROP_VOLUME * drops
    tot_volume = total_volume(initial_volume, drops)
    return (drop_molarity * volume_added) / tot_volume + 1e-7


def h_conc_titration_naoh(drop_molarity, drops, initial_volume=10.000):
    """
    For titrating water with NaOH (.1 or .01 M):
    First, calculate [OH-] = (molarity * volume_added / total_volume) + 1e-7,
    then [H+] = KW / [OH-]
    """
    volume_added = DROP_VOLUME * drops
    tot_volume = total_volume(initial_volume, drops)
    oh_conc = (drop_molarity * volume_added) / tot_volume + 1e-7
    return KW / oh_conc


# ============================
# Buffer System Calculations
# ============================

def buffer_ph_general(acid_init_conc, base_init_conc, pKa, drop_molarity, drops,
                      initial_volume=10.000, addition='acid'):
    """
    Calculates the pH for a general acid/base buffer system,
    using Henderson–Hasselbalch when buffer capacity is not exceeded,
    and switching to the overflow‐region calculation once you run out of conjugate partner.
    """
    # total volumes & moles
    volume_added = DROP_VOLUME * drops
    tot_volume = total_volume(initial_volume, drops)
    moles_HA0 = acid_init_conc * initial_volume
    moles_A0  = base_init_conc * initial_volume
    moles_titrant = drop_molarity * volume_added

    # within buffer region?
    if addition == 'acid':
        if moles_titrant <= moles_A0:
            # HA_final = HA0 + HCl moles, A-_final = A0 − HCl moles
            HA = (moles_HA0 + moles_titrant) / tot_volume
            A  = (moles_A0  - moles_titrant) / tot_volume
            return pKa + math.log10(A / HA)
        else:
            return False

    elif addition == 'base':
        if moles_titrant <= moles_HA0:
            # HA_final = HA0 − NaOH moles, A-_final = A0 + NaOH moles
            HA = (moles_HA0 - moles_titrant) / tot_volume
            A  = (moles_A0  + moles_titrant) / tot_volume
            return pKa + math.log10(A / HA)
        else:
            return False

    else:
        raise ValueError("addition must be 'acid' or 'base'")



def buffer_overflow_ph_general(acid_init_conc, base_init_conc, pKa,
                                drop_molarity, drops, initial_volume=10.000,
                                addition='acid'):
    """
    Once buffer capacity is exceeded, we
      – assume all of the limiting conjugate has been converted,
      – compute [H+] (or [OH–]) coming from that newly formed strong species,
      – add the excess from the titrant,
      – and get pH from total [H+].
    """
    volume_added = DROP_VOLUME * drops
    tot_volume = total_volume(initial_volume, drops)
    moles_HA0 = acid_init_conc * initial_volume
    moles_A0  = base_init_conc * initial_volume
    moles_titrant = drop_molarity * volume_added
    Ka = 10**(-pKa)

    if addition == 'acid':
        # everything A- → HA
        moles_HA = moles_HA0 + moles_A0
        conc_HA  = moles_HA / tot_volume
        # [H+] from HA dissociation
        h_from_HA = math.sqrt(Ka * conc_HA)
        # excess H+ from titrant
        excess_H  = moles_titrant - moles_A0
        h_excess  = excess_H / tot_volume
        return ph_from_h_concentration(h_from_HA + h_excess)

    elif addition == 'base':
        # everything HA → A-
        moles_A = moles_A0 + moles_HA0
        conc_A  = moles_A / tot_volume
        # [OH-] from A- hydrolysis
        oh_from_A = math.sqrt((KW * conc_A) / Ka)
        # excess OH- from titrant
        excess_OH = moles_titrant - moles_HA0
        oh_excess = excess_OH / tot_volume
        oh_total  = oh_from_A + oh_excess
        h_total   = KW / oh_total
        return ph_from_h_concentration(h_total)

    else:
        raise ValueError("addition must be 'acid' or 'base'")

