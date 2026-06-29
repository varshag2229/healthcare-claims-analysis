"""
generate_data.py
Generates a synthetic Medicare-style healthcare claims dataset for analysis.
Run this once to create: claims.csv, patients.csv, providers.csv
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

np.random.seed(42)
random.seed(42)

N_PATIENTS   = 2000
N_PROVIDERS  = 80
N_CLAIMS     = 15000

# ── PATIENTS ──────────────────────────────────────────────────────────────────
ages   = np.random.randint(18, 90, N_PATIENTS)
states = random.choices(
    ["OH", "KY", "IN", "TX", "CA", "NY", "FL", "PA", "IL", "MI"],
    k=N_PATIENTS
)
genders = random.choices(["M", "F"], k=N_PATIENTS)

patients = pd.DataFrame({
    "patient_id":  [f"P{str(i).zfill(5)}" for i in range(1, N_PATIENTS + 1)],
    "age":         ages,
    "gender":      genders,
    "state":       states,
    "risk_score":  np.round(np.random.uniform(0.5, 5.0, N_PATIENTS), 2),
})
patients.to_csv("patients.csv", index=False)
print(f"✅ patients.csv  → {len(patients)} rows")

# ── PROVIDERS ─────────────────────────────────────────────────────────────────
specialties = [
    "Cardiology", "Orthopedics", "General Practice",
    "Oncology", "Neurology", "Pediatrics", "Dermatology", "Radiology"
]
providers = pd.DataFrame({
    "provider_id":  [f"PR{str(i).zfill(4)}" for i in range(1, N_PROVIDERS + 1)],
    "specialty":    random.choices(specialties, k=N_PROVIDERS),
    "state":        random.choices(["OH", "KY", "IN", "TX", "CA", "NY"], k=N_PROVIDERS),
    "network_status": random.choices(["In-Network", "Out-of-Network"], weights=[80, 20], k=N_PROVIDERS),
})
providers.to_csv("providers.csv", index=False)
print(f"✅ providers.csv → {len(providers)} rows")

# ── CLAIMS ────────────────────────────────────────────────────────────────────
diagnoses = {
    "Heart Disease":      "I25.10",
    "Diabetes Type 2":    "E11.9",
    "Hypertension":       "I10",
    "COPD":               "J44.1",
    "Knee Replacement":   "Z96.651",
    "Pneumonia":          "J18.9",
    "Appendectomy":       "K35.89",
    "Stroke":             "I63.9",
    "Cancer - Lung":      "C34.10",
    "Fracture - Hip":     "S72.001A",
}
diag_names = list(diagnoses.keys())
diag_codes = list(diagnoses.values())

start_date = datetime(2022, 1, 1)
end_date   = datetime(2024, 12, 31)

def rand_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))

claim_statuses = random.choices(
    ["Approved", "Denied", "Pending"],
    weights=[70, 20, 10],
    k=N_CLAIMS
)
denial_reasons = [
    "Not Medically Necessary", "Missing Documentation",
    "Out-of-Network Provider", "Duplicate Claim",
    "Exceeded Coverage Limit", None
]

rows = []
for i in range(1, N_CLAIMS + 1):
    patient   = patients.sample(1).iloc[0]
    provider  = providers.sample(1).iloc[0]
    diag_idx  = random.randint(0, len(diag_names) - 1)
    status    = claim_statuses[i - 1]
    svc_date  = rand_date(start_date, end_date)
    los       = random.randint(0, 14)           # length of stay (days)
    billed    = round(random.uniform(500, 85000), 2)
    paid      = round(billed * random.uniform(0.0, 0.9), 2) if status == "Approved" else 0.0

    rows.append({
        "claim_id":        f"C{str(i).zfill(6)}",
        "patient_id":      patient["patient_id"],
        "provider_id":     provider["provider_id"],
        "service_date":    svc_date.strftime("%Y-%m-%d"),
        "diagnosis_name":  diag_names[diag_idx],
        "diagnosis_code":  diag_codes[diag_idx],
        "specialty":       provider["specialty"],
        "claim_status":    status,
        "denial_reason":   random.choice(denial_reasons) if status == "Denied" else None,
        "billed_amount":   billed,
        "paid_amount":     paid,
        "length_of_stay":  los,
        "network_status":  provider["network_status"],
        "patient_age":     patient["age"],
        "patient_gender":  patient["gender"],
        "patient_state":   patient["state"],
        "risk_score":      patient["risk_score"],
    })

claims = pd.DataFrame(rows)
claims.to_csv("claims.csv", index=False)
print(f"✅ claims.csv    → {len(claims)} rows")
print("\nDone! Three CSV files created in /data/")
