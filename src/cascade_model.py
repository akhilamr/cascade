"""cascade_model.py

Core Monte‑Carlo engine for neonatal‑sepsis cascade.
"""
import numpy as np
from collections import Counter, defaultdict

PARAMS = {
    "N": 100_000,
    "birth_place_probs": [0.35, 0.45, 0.20],
    "sepsis_incidence": 0.15,
    "hosp_disch_times": [12, 36],
    "hosp_disch_probs": [0.28, 0.72],
    "clin_disch_times": [12, 24],
    "clin_disch_probs": [0.90, 0.10],
    "onset_seg_probs": [0.5, 0.3, 0.2],
    "onset_seg_bounds": [(0, 24), (24, 72), (72, 672)],
    "seek_help_prob": 0.59,
    "public_phc_frac": 0.65,
    "private_phc_frac": 0.35,
    "rf_sens_hosp": 0.65,
    "rf_sens_clinic": 0.55
}

TIERS = ["BIRTH_RF", "HOSP_POC", "PHC_POC", "COMM_POC"]

def simulate(scenario="A", seed=42, params=PARAMS):
    rng = np.random.default_rng(seed)
    N = params["N"]
    birth_loc = rng.choice(["hospital","clinic","home"],
                           p=params["birth_place_probs"], size=N)
    sepsis = rng.random(N) < params["sepsis_incidence"]
    rf_positive = np.zeros(N, dtype=bool)
    if scenario.upper() == "B":
        mask = (birth_loc == "hospital") & sepsis
        rf_positive[mask] = rng.random(mask.sum()) < params["rf_sens_hosp"]
        mask = (birth_loc == "clinic") & sepsis
        rf_positive[mask] = rng.random(mask.sum()) < params["rf_sens_clinic"]
    discharge = np.zeros(N)
    mask_h = birth_loc == "hospital"
    discharge[mask_h] = rng.choice(params["hosp_disch_times"],
                                   p=params["hosp_disch_probs"],
                                   size=mask_h.sum())
    mask_c = birth_loc == "clinic"
    discharge[mask_c] = rng.choice(params["clin_disch_times"],
                                   p=params["clin_disch_probs"],
                                   size=mask_c.sum())
    onset = np.full(N, np.nan)
    segments = rng.choice(len(params["onset_seg_probs"]),
                          p=params["onset_seg_probs"], size=sepsis.sum())
    idx = 0
    for k,(lo,hi) in enumerate(params["onset_seg_bounds"]):
        seg = segments == k
        cnt = seg.sum()
        onset[np.where(sepsis)[0][idx:idx+cnt]] = lo + rng.random(cnt)*(hi-lo)
        idx += cnt
    assess = np.array([""]*N)
    for i in np.where(sepsis)[0]:
        if birth_loc[i]=="hospital" and onset[i] < discharge[i]:
            assess[i] = "hospital"
        elif birth_loc[i]=="clinic" and onset[i] < discharge[i]:
            assess[i] = "clinic_inpatient"
        else:
            if rng.random() < params["seek_help_prob"]:
                assess[i] = "phc_public" if rng.random() < params["public_phc_frac"] else "phc_private"
            else:
                assess[i] = "community_noformal"
    from collections import Counter, defaultdict
    counts = Counter(assess)
    tested = defaultdict(int); detected = defaultdict(int)
    if scenario.upper() == "B":
        tested["BIRTH_RF"] = np.count_nonzero(birth_loc != "home")
        detected["BIRTH_RF"] = rf_positive.sum()
    tested["HOSP_POC"] = counts["hospital"]; detected["HOSP_POC"] = counts["hospital"]
    tested["PHC_POC"] = counts["clinic_inpatient"] + counts["phc_public"] + counts["phc_private"]
    detected["PHC_POC"] = tested["PHC_POC"]
    tested["COMM_POC"] = counts["community_noformal"]; detected["COMM_POC"] = tested["COMM_POC"]
    return dict(sepsis=sepsis, assess=assess, tested=dict(tested), detected=dict(detected))
