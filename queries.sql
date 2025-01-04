#--What are the top 5 brands by receipts scanned for most recent month?
WITH recent_month AS (
    SELECT year,month
    FROM rewards_db.dim_date
    WHERE date=(SELECT MAX(date) FROM rewards_db.dim_date)
)
SELECT b.name AS brand_name,COUNT(DISTINCT r.id) AS receipts_count
    FROM
        rewards_db.fact_receipts r JOIN rewards_db.fact_rewards_receipt_item ri
            ON r.id=ri.receipt_id
        JOIN rewards_db.dim_brands b
            ON ri.brand_id=b.id
        JOIN rewards_db.dim_date d
            ON r.date_scanned_key=d.date_key
    WHERE
        d.year=(SELECT year FROM recent_month) AND d.month=(SELECT month FROM recent_month)
    GROUP BY b.name
    ORDER BY receipts_count DESC
    LIMIT 5;

#--When considering average spend from receipts with 'rewardsReceiptStatus’ of ‘Accepted’ or ‘Rejected’, which is greater?
SELECT
    CASE
		WHEN AVG(CASE WHEN lower(rewards_receipt_status)='accepted' THEN total_spent END) > AVG(CASE WHEN lower(rewards_receipt_status)='rejected' THEN total_spent END)
			THEN 'Accepted'
        ELSE 'Rejected'
    END AS higher_avg_spend_rewards_receipt_status,
    AVG(CASE WHEN lower(rewards_receipt_status)='accepted' THEN total_spent END) AS avg_spend_accepted,
    AVG(CASE WHEN lower(rewards_receipt_status)='rejected' THEN total_spent END) AS avg_spend_rejected
FROM
    rewards_db.fact_receipts
WHERE
    lower(rewards_receipt_status) IN ('accepted','rejected');

--When considering total number of items purchased from receipts with 'rewardsReceiptStatus’ of ‘Accepted’ or ‘Rejected’, which is greater?
SELECT
    CASE
		WHEN SUM(CASE WHEN lower(rewards_receipt_status)='accepted' THEN purchased_item_count END)>SUM(CASE WHEN lower(rewards_receipt_status)='rejected' THEN purchased_item_count END)
			THEN 'Accepted'
        ELSE 'Rejected'
    END AS higher_total_item_count_receipt_status,
    SUM(CASE WHEN lower(rewards_receipt_status)='accepted' THEN purchased_item_count END) AS total_purchased_item_count_accepted,
    SUM(CASE WHEN lower(rewards_receipt_status)='rejected' THEN purchased_item_count END) AS total_purchased_item_count_rejected
FROM
    rewards_db.fact_receipts
WHERE
    lower(rewards_receipt_status) IN ('accepted','rejected');


#--Which brand has the most spend among users who were created within the past 6 months?
WITH users_created_in_past_6months AS (
    SELECT id AS user_id FROM rewards_db.dim_users WHERE created_date>=DATE_SUB(CURRENT_DATE(), INTERVAL 6 MONTH)
)
SELECT b.name AS brand_name,SUM(r.total_spent) AS total_spend
    FROM rewards_db.fact_receipts r JOIN rewards_db.fact_rewards_receipt_item ri
        ON ri.receipt_id=r.id
    JOIN users_created_in_past_6months u
        ON r.user_id=u.user_id
    JOIN rewards_db.dim_brands b
        ON ri.brand_id=b.id
    GROUP BY b.name
    ORDER BY 2 DESC LIMIT 1;


#--Which brand has the most transactions among users who were created within the past 6 months?
WITH users_created_in_past_6months AS (
    SELECT id AS user_id FROM rewards_db.dim_users WHERE created_date>=DATE_SUB(CURRENT_DATE(), INTERVAL 6 MONTH)
)
SELECT b.name AS brand_name,COUNT(DISTINCT r.id) AS transaction_count
    FROM rewards_db.fact_receipts r JOIN rewards_db.fact_rewards_receipt_item ri
        ON r.id=ri.receipt_id
    JOIN users_created_in_past_6months u
        ON r.user_id=u.user_id
    JOIN rewards_db.dim_brands b
        ON ri.brand_id=b.id
    GROUP BY b.name
    ORDER BY 2 DESC LIMIT 1;

