"""
run_simulation.py — CLI wrapper to reproduce tables & figures.
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from cascade_model import simulate, PARAMS

OUT = Path("outputs")
OUT.mkdir(exist_ok=True)

res_A = simulate("A")
res_B = simulate("B")

def per1000(x): return round(x * 1000 / PARAMS["N"])

# First‑assessment table
assess_counts = Counter(res_A["assess"])
table1 = pd.DataFrame({
    "Site": ["Hospital ward", "Clinic inpatient", "PHC public OPD",
             "PHC private OPD", "Community – no provider"],
    "Cases_per_1000": [per1000(assess_counts["hospital"]),
                       per1000(assess_counts["clinic_inpatient"]),
                       per1000(assess_counts["phc_public"]),
                       per1000(assess_counts["phc_private"]),
                       per1000(assess_counts["community_noformal"])]
})
table1.to_csv(OUT / "table_first_assessment.csv", index=False)

# Diagnostic coverage table
TIERS = ["BIRTH_RF", "HOSP_POC", "PHC_POC", "COMM_POC"]
def build(res, label):
    rows = []
    for tier in TIERS:
        rows.append({
            "Scenario": label,
            "Tier": tier,
            "Babies_tested_per_1000": per1000(res["tested"].get(tier, 0)),
            "Sepsis_detected_per_1000": per1000(res["detected"].get(tier, 0))
        })
    return pd.DataFrame(rows)
table2 = pd.concat([
    build(res_A, "A – no screen"),
    build(res_B, "B – birth screen")
])
table2.to_csv(OUT / "table_diagnostic_coverage.csv", index=False)

# Figures
plt.figure(figsize=(6,4))
plt.bar(table1["Site"], table1["Cases_per_1000"])
plt.ylabel("Suspected sepsis / 1 000 births")
plt.title("First assessment site")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(OUT / "figure_first_assessment.png", dpi=300)
plt.close()

tiers_order = ["HOSP_POC", "PHC_POC", "COMM_POC"]
for res, lab in [(res_A, "Scenario A"), (res_B, "Scenario B")]:
    cum, xs, ys = 0, [], []
    for tier in tiers_order:
        cum += per1000(res["detected"].get(tier, 0))
        xs.append(tier)
        ys.append(cum)
    plt.plot(xs, ys, marker="o", label=lab)
plt.ylabel("Sepsis detected / 1 000 births")
plt.title("Cumulative detection by tier")
plt.legend()
plt.tight_layout()
plt.savefig(OUT / "figure_cumulative_coverage.png", dpi=300)
plt.close()

print("Outputs saved in ./outputs/")
