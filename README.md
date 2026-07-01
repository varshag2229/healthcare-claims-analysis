# 🏥 Healthcare Claims & Patient Analytics

**End-to-end data analytics project** analyzing 15,000+ Medicare-style medical claims to uncover denial patterns, cost drivers, and patient risk insights — supporting data-driven decisions for healthcare payers and providers.

---

## 📌 Project Overview

| Item | Detail |
|---|---|
| **Domain** | Healthcare / Insurance Analytics |
| **Dataset** | 15,000 claims · 2,000 patients · 80 providers (2022–2024) |
| **Tools** | Python · SQL · Excel · Tableau / Power BI |
| **Skills** | Data Cleaning · EDA · Statistical Analysis · Dashboard Design |
| **Role** | End-to-end Analyst (solo project) |

---

## 🎯 Business Questions Answered

1. What is the overall claim **denial rate**, and which diagnoses drive it?
2. Which **specialties** generate the highest costs?
3. How do **in-network vs out-of-network** providers differ in cost and denial?
4. What are the **top denial reasons** — and what revenue is at risk?
5. Do **older patients** incur significantly higher claim costs?
6. Which **providers** have the highest denial rates (performance scorecard)?
7. Are there **repeat claims within 30 days** signaling potential readmissions?

---

## 📊 Key Findings

| Metric | Value |
|---|---|
| Total Claims Analyzed | 15,000 |
| Total Billed Amount | $642.5 Million |
| Total Paid Amount | $201.8 Million |
| Overall Denial Rate | **20.2%** |
| Average Length of Stay | 7.1 days |

- 🔴 **Hypertension** and **Fracture - Hip** had the highest denial rates (~21%)
- 💸 **Out-of-network** claims were denied at nearly **2× the rate** of in-network
- 📋 **"Not Medically Necessary"** was the #1 denial reason, representing the largest revenue at risk
- 👴 Patients aged **75+** had the highest average approved claim cost
- 🏥 **Oncology** and **Cardiology** specialties drove the most total paid spend

---

## 📁 Project Structure

```
healthcare-claims-analysis/
│
├── data/
│   ├── generate_data.py      # Script to generate synthetic dataset
│   ├── claims.csv            # 15,000 claim records
│   ├── patients.csv          # 2,000 patient profiles
│   └── providers.csv         # 80 provider records
│
├── notebooks/
│   └── healthcare_analysis.py  # Full EDA + visualizations (Python)
│
├── sql/
│   └── analysis_queries.sql    # 10 business SQL queries
│
├── visuals/
│   ├── 01_claim_status.png
│   ├── 02_denial_by_diagnosis.png
│   ├── 03_monthly_trend.png
│   ├── 04_cost_by_specialty.png
│   ├── 05_denial_reasons.png
│   └── 06_cost_by_age.png
│
├── reports/
│   └── claims_summary.csv      # Summary table by diagnosis
│
└── README.md
```

---

## 📈 Visualizations

### Claim Status Distribution & Billed Amount
![Claim Status](visuals/01_claim_status.png)

### Denial Rate by Diagnosis
![Denial by Diagnosis](visuals/02_denial_by_diagnosis.png)

### Monthly Claims Volume & Paid Amount Trend
![Monthly Trend](visuals/03_monthly_trend.png)

### Average Approved Cost by Specialty
![Cost by Specialty](visuals/04_cost_by_specialty.png)

### Top Denial Reasons
![Denial Reasons](visuals/05_denial_reasons.png)

### Average Cost by Patient Age Band
![Cost by Age](visuals/06_cost_by_age.png)

---

## 🛠️ How to Run

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/healthcare-claims-analysis.git
cd healthcare-claims-analysis
```

### 2. Install Dependencies
```bash
pip install pandas numpy matplotlib seaborn
```

### 3. Generate the Dataset
```bash
python data/generate_data.py
```

### 4. Run the Analysis
```bash
python notebooks/healthcare_analysis.py
```

### 5. Run SQL Queries
```bash
# Using SQLite
sqlite3 healthcare.db
.mode csv
.import data/claims.csv claims
.import data/patients.csv patients
.import data/providers.csv providers
.read sql/analysis_queries.sql
```

---

## 💡 Business Recommendations

Based on the analysis:

1. **Target "Not Medically Necessary" denials** — implement pre-authorization checklists for Hypertension and Hip Fracture claims to reduce the 21%+ denial rate
2. **Incentivize in-network provider use** — out-of-network denials are nearly 2× higher; patient education campaigns could reduce this
3. **Flag high-risk patients early** — patients aged 75+ with risk scores > 4.0 account for disproportionate costs; proactive care management could reduce spend
4. **Audit providers with denial rates > 25%** — provider scorecards reveal outliers requiring documentation training
5. **30-day readmission monitoring** — implement alerts for repeat claims within 30 days, especially for Pneumonia and COPD patients

---

## 🧰 Tools & Libraries

| Tool | Usage |
|---|---|
| Python (Pandas, NumPy) | Data cleaning, transformation, EDA |
| Matplotlib, Seaborn | Data visualization (6 charts) |
| SQL (SQLite) | Business queries, KPI analysis |
| Excel | Summary tables, pivot-ready exports |
| Tableau / Power BI | Interactive dashboard *(in progress)* |

---

## 👩‍💻 Author

**Varsha Reddy Gangasani**  
MS Information Technology · University of Cincinnati  
📧 varshag2229@gmail.com  
🔗 [LinkedIn](https://linkedin.com/in/varsha-gangasani-121408215) · [GitHub](https://github.com/varshag2229)

---

## 📄 License

This project uses a **synthetic dataset** generated for educational purposes. No real patient data was used.  
Feel free to fork, learn from, and build upon this project.
