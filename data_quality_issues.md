**1.There are records in brands.json where same barcode is assigned to different brand ids.**

Query:`select barcode,count(id) from rewards_db.dim_brands group by 1 having count(id) >1;`

**2.Reciept created without bonus points.**

Query:`select * from receipts_staging where bonus_points_earned  is null`

**3.Reciept created without bonusPointsEarnedReason.**

Query:`select * from receipts_staging where bonus_points_earned_reason is null`

**4. There are records in the receipts table where the user is not found in the users table.**

Query:`select user_id from receipts_staging where user_id not in ( select id from users_staging)`

**5.Null value observed in state column of user table.**

Query:`select * from users_staging where state is null`

**6.Data contains values other than constant "consumer" for "role" column in User table.**

Query: `select distinct role from users_staging`

**7.Null values observed in the top brand.**

Query:`select top_brand, count(*) from rewards_db.dim_brands group by top_brand`

**8.Barcode is null or not found in the brands table.**

Query:`select distinct brand_id from rewards_receipt_item_staging;`
