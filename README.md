# fetch-rewards-systems

#### **Overview**  
This repository contains my solutions for the coding exercise. Below are the details for each task, including my approach and any assumptions made.  

---

#### **1. Review Unstructured JSON Data and Diagram a New Structured Relational Data Model**  
**Analysis**:  
- Reviewed the unstructured JSON data provided.  
- Designed a relational data model to organize the data into normalized tables for scalability, consistency, and ease of querying.  

**Deliverables**:  
- [Data Model Diagram](data_model_diagram.png) .
- [SQL Scripts](tables-creation/create_statements.sql) to create the tables. 

---

#### **2. Generate a Query to Answer a Predetermined Business Question**  

**Process**  
- The data is loaded into MySQL on my local system using Python scripts.  
- The queries can be executed on the MySQL system through SQL Connector.

**Deliverables**:  
- Data Loader [Python Scripts](data-loader).
- Table Creation [SQL Scripts](tables-creation/create_statements.sql)
- [SQL Queries](queries.sql)  
- Explanation of the query logic (included in comments within the SQL script).

**Assumptions**:  
- Dates are stored in epoch format and have been converted to a readable format.  
- Duplicate records were found in the user data, so those duplicates were removed.

---

#### **3. Generate a Query to Capture Data Quality Issues Against the New Structured Relational Data Model**  
**Analysis**:  
- Analyzed the new data model for potential data quality issues (e.g., missing values,specific values ,duplicate records, invalid relationships).  
- Wrote a query to identify these issues for better monitoring and resolution.  

**Deliverables**:  
- [Detailed Summary](data_quality_issues.md) of Data Quality Issues.
- SQL Queries included in the detailed summary

**Assumptions**:  
- Focused on key fields critical for analytics (e.g., primary keys, foreign keys, required fields). 

---

#### **4. Write a Short Email or Slack Message to the Business Stakeholder**  

**Deliverables**:  
- [Email draft](data_questions_email.md) 

---

#### **How to Run**  

1. **Setup**:  
   - Ensure that a MySQL database is available on the system where these scripts will be executed.  
   - Load the table schema by running `create_statements.sql`.  
   - Load the data by executing the Python scripts located in the `fetch-rewards-systems/data-loader` folder, one after the other.  

2. **Run Queries**:  
   - Execute the queries in `queries.sql` using a SQL client to retrieve the results.
   
---

Thank you!