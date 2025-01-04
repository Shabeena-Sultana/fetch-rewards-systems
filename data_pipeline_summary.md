### Data Pipeline Summary  

This ETL pipeline processes raw data into a structured relational format using **Python and SQL**.  

#### **Pipeline Overview**  
1. **Staging Tables**:  
   - Raw data is loaded into staging(raw) tables (`brands_staging`, `users_staging`, etc.) for validation and transformation.  

2. **Transformation**:  
   - Data is cleansed using Python (e.g., removing duplicates, resolving null values, verifying foreign key relationships).  

3. **Loading**:  
   - Cleaned data is moved into actual tables which can be used for data analytics:  
     - **Dimension Tables**: `dim_brands`, `dim_users`, `dim_date`.  
     - **Fact Tables**: `fact_receipts`, `fact_rewards_receipt_item`.  

#### **Tools & Technologies**  
- **Python**: Automates data ingestion into staging tables.  
- **SQL**: Performs data analysis and transformations