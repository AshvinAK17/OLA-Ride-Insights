## OLA-Ride-Insights
An end-to-end data analysis and visualization project using OLA ride datasets. This project utilizes **SQL**, **Python**, **Power BI**, and **Streamlit** to extract and present insights from ride-sharing trends in **Bangalore for July 2024**.

---

## Project Objectives

- Analyze ride volume, booking behavior, cancellation reasons, and payment trends.
- Visualize patterns using Power BI and build an interactive Streamlit dashboard.
- Provide actionable business insights for OLA's operational strategy.

---

## Data Source
- Actual Dataset: `OLA_DataSet.csv`
- Pre-Processed Dataset: `ola_name.csv` (exported from MySQL `ola_db.ola_rides`)
- Domain: Ride-Sharing / Mobility Analytics
- Location: Bangalore, India
- Period: July 2024

---

## Data Processing

- Cleaned nulls in `customer_ratings`, `driver_ratings`,`V_TAT`,`C_TAT` and converted null values in `Canceled_Rides_by_Customer`, `Canceled_Rides_by_Driver`,`Incomplete_Rides_Reason`
- Standardized categorical values (e.g., `Booking_Status`, `Payment_Method`).
- Converted `Date` and `Time` into appropriate formats for analysis.

---

## Technologies Used

- **Python**  (Pandas, Matplotlib, MySQL Connector)
- **SQL**  (MySQL for querying)
- **Power BI**  (Interactive dashboards)
- **Streamlit**  (Web-based dashboard interface)
- **Git**  for version control

---

## Key Analyses Performed

1. Ride Volume Over Time  
2. Booking Status Breakdown  
3. Top 5 Vehicle Types by Ride Distance  
4. Average Customer Ratings by Vehicle Type  
5. Cancellation Reasons (Drivers & Customers)  
6. Revenue by Payment Method  
7. Top 5 Customers by Total Booking Value  
8. Ride Distance Distribution  
9. Ratings Distribution (Driver vs. Customer)  
10. Incomplete Rides & Root Causes

---

## Dashboards

### Power BI
- Interactive reports segmented by:  
  - Overall  
  - Vehicle Type  
  - Revenue  
  - Cancellation  
  - Ratings  

### Streamlit
- Homepage: Project title + button to view insights  
- Dynamic dropdown for 10 SQL-based visual analyses  
- interactive visualizations via matplotlib and pandas

Streamlit Server: https://ola-ride-insights-bc3apsuqxhwu8htgxsjyeq.streamlit.app/
---

## Setup Instructions

1. Download the data
2. Install dependencies:

       pip install pandas
       pip install mysql-connector-python
       pip install -r requirements.txt
       pip install streamlit
   
3. Configure MySQL database (see `ola_db` schema)
4. Run Streamlit App:  

