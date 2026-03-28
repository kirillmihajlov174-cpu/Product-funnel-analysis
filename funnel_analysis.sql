WITH funnel AS (
    SELECT
        user_id,
        MAX(CASE WHEN event_name = 'view_landing' THEN 1 ELSE 0 END) AS landed,
        MAX(CASE WHEN event_name = 'sign_up' THEN 1 ELSE 0 END) AS signed_up,
        MAX(CASE WHEN event_name = 'kyc_completed' THEN 1 ELSE 0 END) AS kyc_completed,
        MAX(CASE WHEN event_name = 'deposit_success' THEN 1 ELSE 0 END) AS deposited,
        MAX(CASE WHEN event_name = 'first_trade' THEN 1 ELSE 0 END) AS traded
    FROM events
    GROUP BY 1
)

SELECT 'Landing viewed' AS stage, SUM(landed) AS users FROM funnel
UNION ALL
SELECT 'Signed up', SUM(signed_up) FROM funnel
UNION ALL
SELECT 'KYC completed', SUM(kyc_completed) FROM funnel
UNION ALL
SELECT 'Deposit made', SUM(deposited) FROM funnel
UNION ALL
SELECT 'First trade', SUM(traded) FROM funnel;
