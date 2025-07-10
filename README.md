# Neonatal-Sepsis Cascade Model

Reproducible Monte-Carlo model (100 000 simulated births) that
quantifies how many neonates – and how many suspected sepsis episodes –
would be captured by point-of-care (POC) diagnostics placed at four
levels of the LMIC health system:

| Tier | Abbrev. | Description |
|------|---------|-------------|
| Birth risk-factor screen | `BIRTH_RF` | Experimental, done on all facility births |
| Hospital ward POC | `HOSP_POC` | Test used when symptoms start in post-natal ward |
| Primary-health-centre POC | `PHC_POC` | Test at public & private PHC (OPD + 10 % clinic in-patients) |
| Community POC | `COMM_POC` | CHW / pharmacy / self-test before any facility contact |

Two scenarios are modelled:

* **Scenario A** – today’s world (no risk-factor screen)  
* **Scenario B** – as A plus an imperfect risk-factor screen  
  (sensitivity 0.65 in hospitals, 0.55 in clinics)

The code reproduces **Table 1, Table 2, Figure 1 and Figure 2** in the
accompanying report.

## Quick start

```bash
git clone https://github.com/<your-handle>/neonatal-sepsis-cascade.git
cd neonatal-sepsis-cascade
pip install -r requirements.txt
python src/run_simulation.py
```

Outputs:

```
outputs/
├── table_first_assessment.csv
├── table_diagnostic_coverage.csv
├── figure_first_assessment.png
└── figure_cumulative_coverage.png
```

## References

* DHS Programme (2015‑22) – place of delivery  
* Campbell OMR et al. **PLoS Med** 2016 – post‑natal length‑of‑stay  
* Zaidi AKM & Thaver D. **Clin Microbiol Rev** 2020 – EOS review  
* Segun T et al. **BMC Pediatr** 2024 – PSBI incidence  
* Herbert HK et al. **PLoS Med** 2012 – care‑seeking review  
* Ngadaya E et al. **PLoS One** 2024 – referral acceptance

Licensed MIT – see `LICENSE`.
