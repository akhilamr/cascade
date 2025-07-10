import pandas as pd, matplotlib.pyplot as plt
from pathlib import Path
from cascade_model import simulate, PARAMS

OUT = Path("outputs"); OUT.mkdir(exist_ok=True)

resA = simulate("A"); resB = simulate("B")
def per1000(x): return round(x*1000/PARAMS["N"])
assess_counts = __import__("collections").Counter(resA["assess"])
df_first = pd.DataFrame({
    "Site":["hospital","clinic_inpatient","phc_public","phc_private","community_noformal"],
    "Cases_per_1000":[per1000(assess_counts[s]) for s in
                      ["hospital","clinic_inpatient","phc_public","phc_private","community_noformal"]]
})
df_first.to_csv(OUT/"table_first_assessment.csv",index=False)
print("Saved outputs to", OUT)
