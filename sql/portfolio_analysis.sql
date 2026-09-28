-- Motor Insurance Pricing & Risk Analytics
-- DuckDB SQL examples using freMTPL2 raw CSV files.

CREATE OR REPLACE VIEW freq AS
SELECT * FROM read_csv_auto('data/raw/freMTPL2freq.csv', header=true);

CREATE OR REPLACE VIEW sev AS
SELECT * FROM read_csv_auto('data/raw/freMTPL2sev.csv', header=true);

-- 1) Core frequency KPIs
SELECT
    COUNT(*) AS policies,
    SUM(Exposure) AS total_exposure,
    SUM(ClaimNb) AS total_claims,
    SUM(ClaimNb) / SUM(Exposure) AS annual_claim_frequency,
    100.0 * SUM(ClaimNb) / SUM(Exposure) AS claims_per_100_policy_years
FROM freq;

-- 2) Severity KPIs
SELECT
    COUNT(*) AS claim_rows,
    AVG(ClaimAmount) AS average_claim_severity,
    SUM(ClaimAmount) AS total_claim_amount
FROM sev;

-- 3) Bonus-Malus pricing segments
WITH f AS (
    SELECT *,
        CASE
            WHEN BonusMalus <= 50 THEN '<=50'
            WHEN BonusMalus <= 75 THEN '51-75'
            WHEN BonusMalus <= 100 THEN '76-100'
            ELSE '>100'
        END AS bonus_band
    FROM freq
),
s AS (
    SELECT IDpol, SUM(ClaimAmount) AS claim_amount, COUNT(*) AS severity_claims
    FROM sev GROUP BY IDpol
)
SELECT
    f.bonus_band,
    COUNT(*) AS policies,
    SUM(f.Exposure) AS exposure,
    SUM(f.ClaimNb) AS claims,
    SUM(f.ClaimNb) / SUM(f.Exposure) AS claim_frequency,
    SUM(COALESCE(s.claim_amount,0)) / NULLIF(SUM(COALESCE(s.severity_claims,0)),0) AS average_severity
FROM f
LEFT JOIN s USING (IDpol)
GROUP BY 1
ORDER BY 1;

-- 4) Area-level claim frequency
SELECT
    Area,
    COUNT(*) AS policies,
    SUM(Exposure) AS exposure,
    SUM(ClaimNb) AS claims,
    100.0 * SUM(ClaimNb) / SUM(Exposure) AS claim_rate_per_100
FROM freq
GROUP BY Area
ORDER BY claim_rate_per_100 DESC;
