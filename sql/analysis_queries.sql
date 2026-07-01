-- ============================================================
-- Healthcare Claims Analysis - SQL Queries
-- Author: Varsha Reddy Gangasani
-- Database: SQLite / PostgreSQL compatible
-- ============================================================

-- ── SETUP: Load CSVs as tables (SQLite example) ──────────────
-- In SQLite CLI:
--   .mode csv
--   .import data/claims.csv claims
--   .import data/patients.csv patients
--   .import data/providers.csv providers


-- ── 1. OVERALL CLAIM SUMMARY KPIs ────────────────────────────
-- Key metrics at a glance
SELECT
    COUNT(*)                                          AS total_claims,
    ROUND(SUM(billed_amount), 2)                     AS total_billed,
    ROUND(SUM(paid_amount), 2)                        AS total_paid,
    ROUND(AVG(billed_amount), 2)                      AS avg_billed,
    ROUND(100.0 * SUM(CASE WHEN claim_status = 'Denied'
                           THEN 1 ELSE 0 END) / COUNT(*), 1)  AS denial_rate_pct,
    ROUND(AVG(length_of_stay), 1)                     AS avg_length_of_stay
FROM claims;


-- ── 2. DENIAL RATE BY DIAGNOSIS ──────────────────────────────
-- Identify which conditions are being denied most
SELECT
    diagnosis_name,
    COUNT(*)                                                      AS total_claims,
    SUM(CASE WHEN claim_status = 'Denied' THEN 1 ELSE 0 END)     AS denied_claims,
    ROUND(100.0 * SUM(CASE WHEN claim_status = 'Denied'
                           THEN 1 ELSE 0 END) / COUNT(*), 1)    AS denial_rate_pct,
    ROUND(SUM(billed_amount), 0)                                  AS total_billed,
    ROUND(SUM(paid_amount), 0)                                    AS total_paid
FROM claims
GROUP BY diagnosis_name
ORDER BY denial_rate_pct DESC;


-- ── 3. TOP DENIAL REASONS ─────────────────────────────────────
-- Understand WHY claims are being denied
SELECT
    denial_reason,
    COUNT(*)                                    AS denial_count,
    ROUND(100.0 * COUNT(*) / (
        SELECT COUNT(*) FROM claims
        WHERE claim_status = 'Denied'
    ), 1)                                       AS pct_of_denials,
    ROUND(SUM(billed_amount), 0)                AS billed_at_risk
FROM claims
WHERE claim_status = 'Denied'
  AND denial_reason IS NOT NULL
  AND denial_reason != 'N/A'
GROUP BY denial_reason
ORDER BY denial_count DESC;


-- ── 4. COST BY SPECIALTY ──────────────────────────────────────
-- Which specialties drive the most cost?
SELECT
    specialty,
    COUNT(*)                                    AS total_claims,
    ROUND(AVG(paid_amount), 0)                  AS avg_paid,
    ROUND(SUM(paid_amount), 0)                  AS total_paid,
    ROUND(AVG(length_of_stay), 1)               AS avg_los
FROM claims
WHERE claim_status = 'Approved'
GROUP BY specialty
ORDER BY total_paid DESC;


-- ── 5. IN-NETWORK VS OUT-OF-NETWORK COMPARISON ───────────────
-- Cost and denial impact of network status
SELECT
    network_status,
    COUNT(*)                                                    AS total_claims,
    ROUND(AVG(billed_amount), 0)                                AS avg_billed,
    ROUND(AVG(paid_amount), 0)                                  AS avg_paid,
    ROUND(100.0 * SUM(CASE WHEN claim_status = 'Denied'
                           THEN 1 ELSE 0 END) / COUNT(*), 1)  AS denial_rate_pct
FROM claims
GROUP BY network_status;


-- ── 6. MONTHLY CLAIMS TREND ──────────────────────────────────
-- Track claim volume and spend over time
SELECT
    SUBSTR(service_date, 1, 7)   AS year_month,
    COUNT(*)                     AS claim_count,
    ROUND(SUM(billed_amount), 0) AS total_billed,
    ROUND(SUM(paid_amount), 0)   AS total_paid,
    SUM(CASE WHEN claim_status = 'Denied' THEN 1 ELSE 0 END) AS denied_count
FROM claims
GROUP BY year_month
ORDER BY year_month;


-- ── 7. HIGH-RISK PATIENTS ─────────────────────────────────────
-- Patients with highest claim costs (top 10)
SELECT
    c.patient_id,
    p.age,
    p.gender,
    p.state,
    p.risk_score,
    COUNT(c.claim_id)               AS total_claims,
    ROUND(SUM(c.billed_amount), 0)  AS total_billed,
    ROUND(SUM(c.paid_amount), 0)    AS total_paid
FROM claims c
JOIN patients p ON c.patient_id = p.patient_id
WHERE c.claim_status = 'Approved'
GROUP BY c.patient_id, p.age, p.gender, p.state, p.risk_score
ORDER BY total_paid DESC
LIMIT 10;


-- ── 8. AGE BAND COST ANALYSIS ────────────────────────────────
-- Do older patients cost more?
SELECT
    CASE
        WHEN patient_age BETWEEN 18 AND 30 THEN '18–30'
        WHEN patient_age BETWEEN 31 AND 45 THEN '31–45'
        WHEN patient_age BETWEEN 46 AND 60 THEN '46–60'
        WHEN patient_age BETWEEN 61 AND 75 THEN '61–75'
        ELSE '75+'
    END                              AS age_band,
    COUNT(*)                         AS total_claims,
    ROUND(AVG(billed_amount), 0)     AS avg_billed,
    ROUND(AVG(paid_amount), 0)       AS avg_paid,
    ROUND(AVG(length_of_stay), 1)    AS avg_los
FROM claims
WHERE claim_status = 'Approved'
GROUP BY age_band
ORDER BY MIN(patient_age);


-- ── 9. READMISSION PROXY: REPEAT CLAIMS IN 30 DAYS ───────────
-- Patients with multiple claims within 30 days (potential readmission)
SELECT
    a.patient_id,
    a.claim_id           AS first_claim,
    b.claim_id           AS repeat_claim,
    a.diagnosis_name,
    a.service_date       AS first_visit,
    b.service_date       AS repeat_visit,
    JULIANDAY(b.service_date) - JULIANDAY(a.service_date) AS days_between
FROM claims a
JOIN claims b
  ON  a.patient_id = b.patient_id
  AND a.claim_id   < b.claim_id
  AND JULIANDAY(b.service_date) - JULIANDAY(a.service_date) BETWEEN 1 AND 30
ORDER BY days_between
LIMIT 20;


-- ── 10. PROVIDER PERFORMANCE SCORECARD ───────────────────────
-- Which providers have highest denial rates?
SELECT
    c.provider_id,
    pr.specialty,
    pr.network_status,
    COUNT(*)                                                    AS total_claims,
    ROUND(100.0 * SUM(CASE WHEN c.claim_status = 'Denied'
                           THEN 1 ELSE 0 END) / COUNT(*), 1)  AS denial_rate_pct,
    ROUND(AVG(c.billed_amount), 0)                              AS avg_billed,
    ROUND(AVG(c.length_of_stay), 1)                            AS avg_los
FROM claims c
JOIN providers pr ON c.provider_id = pr.provider_id
GROUP BY c.provider_id, pr.specialty, pr.network_status
HAVING total_claims >= 100
ORDER BY denial_rate_pct DESC
LIMIT 15;
