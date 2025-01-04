CREATE TABLE IF NOT EXISTS rewards_db.brands_staging (
    id VARCHAR(50),
    barcode VARCHAR(50),
    brand_code VARCHAR(50),
    category VARCHAR(100),
    category_code VARCHAR(50),
    cpg VARCHAR(50),
    top_brand BOOLEAN,
    name VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS rewards_db.dim_brands (
    id VARCHAR(50) PRIMARY KEY,
    barcode VARCHAR(50),
    brand_code VARCHAR(50),
    category VARCHAR(100),
    category_code VARCHAR(50),
    cpg VARCHAR(50),
    top_brand BOOLEAN,
    name VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS rewards_db.users_staging (
    id VARCHAR(50),
    state VARCHAR(5),
    created_date DATETIME,
    last_login DATETIME,
    role VARCHAR(20),
    active BOOLEAN
);

CREATE TABLE IF NOT EXISTS rewards_db.dim_users (
    id VARCHAR(255) PRIMARY KEY,
    state VARCHAR(2),
    created_date DATETIME,
    last_login DATETIME,
    role VARCHAR(50) DEFAULT 'CONSUMER',
    active BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS rewards_db.dim_date (
    date_key INT PRIMARY KEY,
    date DATE,
    year INT,
    month INT,
    day INT,
    day_of_week VARCHAR(10),
    week INT,
    quarter INT,
    is_weekend BOOLEAN
);

CREATE TABLE IF NOT EXISTS rewards_db.receipts_staging (
    id VARCHAR(255),
    bonus_points_earned INT,
    bonus_points_earned_reason VARCHAR(255),
    create_date_key INT,
    date_scanned_key INT,
    finished_date_key INT,
    modify_date_key INT,
    points_awarded_date_key INT,
    points_earned DECIMAL(10, 2),
    purchase_date_key INT,
    purchased_item_count INT,
    rewards_receipt_status VARCHAR(255),
    total_spent DECIMAL(10, 2),
    user_id VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS rewards_db.rewards_receipt_item_staging (
    id VARCHAR(255),
    receipt_id VARCHAR(255),
    brand_id VARCHAR(255),
    description VARCHAR(255),
    final_price DECIMAL(10, 2),
    item_price DECIMAL(10, 2),
    needs_fetch_review BOOLEAN,
    partner_item_id VARCHAR(255),
    prevent_target_gap_points BOOLEAN,
    quantity_purchased INT,
    user_flagged_barcode VARCHAR(255),
    user_flagged_new_item BOOLEAN,
    user_flagged_price DECIMAL(10, 2),
    user_flagged_quantity INT
);


CREATE TABLE IF NOT EXISTS rewards_db.fact_receipts (
    id VARCHAR(255) PRIMARY KEY,
    bonus_points_earned INT,
    bonus_points_earned_reason VARCHAR(255),
    create_date_key INT,
    date_scanned_key INT,
    finished_date_key INT,
    modify_date_key INT,
    points_awarded_date_key INT,
    points_earned INT,
    purchase_date_key INT,
    purchased_item_count INT,
    rewards_receipt_status VARCHAR(255),
    total_spent DECIMAL(10, 2),
    user_id VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES dim_users(id),
    FOREIGN KEY (create_date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (date_scanned_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (finished_date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (modify_date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (points_awarded_date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (purchase_date_key) REFERENCES dim_date(date_key)
);

CREATE TABLE IF NOT EXISTS rewards_db.fact_rewards_receipt_item (
    id VARCHAR(255) PRIMARY KEY,
    receipt_id VARCHAR(255),
    brand_id VARCHAR(255),
    description VARCHAR(255),
    final_price DECIMAL(10, 2),
    item_price DECIMAL(10, 2),
    needs_fetch_review BOOLEAN,
    partner_item_id VARCHAR(255),
    prevent_target_gap_points BOOLEAN,
    quantity_purchased INT,
    user_flagged_barcode VARCHAR(255),
    user_flagged_new_item BOOLEAN,
    user_flagged_price DECIMAL(10, 2),
    user_flagged_quantity INT,
    FOREIGN KEY (receipt_id) REFERENCES fact_receipts(id),
    FOREIGN KEY (brand_id) REFERENCES dim_brands(id)
);



show tables;
drop table receipts_staging;
drop table rewards_receipt_item_staging;
drop table dim_date;