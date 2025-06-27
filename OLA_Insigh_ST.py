import streamlit as st
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt

# Page Config
st.set_page_config(page_title="OLA Ride Insights", layout="wide")

# Initial Landing Page
if "view_analysis" not in st.session_state:
    st.session_state.view_analysis = False

# Main Centered Title
st.markdown("""
    <h1 style='text-align: center; font-size: 35px;'>OLA Ride Insights</h1>
""", unsafe_allow_html=True)

if not st.session_state.view_analysis:
    st.markdown("""
        <h2 style='font-size: 28px; text-align:center;'>Welcome to the OLA Ride Insights Dashboard</h2>
        <p style='font-size: 20px; text-align:center;'>Click below to explore the analysis of bookings, revenue, and performance metrics.</p>
    """, unsafe_allow_html=True)
    if st.button("Click to View Analysis", use_container_width=True):
        st.session_state.view_analysis = True
    st.stop()

# Back to Dashboard Button
if st.button("Back to Dashboard"):
    st.session_state.view_analysis = False
    st.rerun()

# MySQL connection
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345678",
        database="ola_db"
    )

connection = get_connection()
cursor = connection.cursor(buffered=True)
# Dropdown
analysis_options = [
    "Select Analysis",
    "1. Successful Bookings Over Time",
    "2. Average Ride Distance per Vehicle Type",
    "3. Total Cancelled Rides by Customers",
    "4. Top 5 Customers by Ride Count",
    "5. Driver Cancellations (Personal/Car Issue)",
    "6. Max & Min Ratings for Prime Sedan",
    "7. UPI Payment Ride Trend",
    "8. Avg Customer Rating by Vehicle Type",
    "9. Total Booking Value of Successful Rides",
    "10. Incomplete Rides by Reason & Vehicle"
]

selected_analysis = st.selectbox("Choose an Analysis:", analysis_options)

# 1. Successful Bookings Over Time
if selected_analysis == analysis_options[1]:
    query = """ 
    SELECT * 
    FROM ola_rides 
    WHERE Booking_Status = 'SUCCESS'
    """
    cursor.execute(query)
    results = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(results, columns=columns)
    df['Date'] = pd.to_datetime(df['Date'])
    daily_counts = df.groupby('Date').size()
    fig, ax = plt.subplots(figsize=(12, 6))
    daily_counts.plot(ax=ax, marker='o', color='green')
    ax.set_title("Successful Bookings Over Time", fontsize=18)
    ax.set_xlabel("Date", fontsize=14)
    ax.set_ylabel("Number of Bookings", fontsize=14)
    st.pyplot(fig)

# 2. Average Ride Distance per Vehicle Type
elif selected_analysis == analysis_options[2]:
    query = """
    SELECT Vehicle_Type, AVG(Ride_Distance) AS Avg_Ride_Distance
    FROM ola_rides
    WHERE Booking_Status = 'SUCCESS'
    GROUP BY Vehicle_Type;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(results, columns=columns)
    st.dataframe(df)

# 3. Total Cancelled Rides by Customers
elif selected_analysis == analysis_options[3]:
    query = """
    SELECT COUNT(*) AS Total_Customer_Cancelled_Rides
    FROM ola_rides
    WHERE Canceled_Rides_by_Customer != 'Not Applicable';
    """
    cursor.execute(query)
    results = cursor.fetchone()
    st.markdown(f"<h3 style='font-size:22px;'>Total Cancelled Rides by Customers: <b>{results[0]}</b></h3>", unsafe_allow_html=True)

# 4. Top 5 Customers by Ride Count
elif selected_analysis == analysis_options[4]:
    query = """
    SELECT 
        TRIM(Customer_ID) AS CUSTOMERS,
        COUNT(*) AS TOTAL_RIDES
    FROM ola_rides
    WHERE Booking_Status = 'SUCCESS'
    GROUP BY TRIM(Customer_ID)
    ORDER BY TOTAL_RIDES DESC, TRIM(Customer_ID) ASC
    LIMIT 5;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(results, columns=columns)
    st.dataframe(df)

# 5. Driver Cancellations (Personal/Car Issue)
elif selected_analysis == analysis_options[5]:
    query = """
    SELECT COUNT(*) AS Canceled_Rides_by_Driver
    FROM ola_rides
    WHERE Canceled_Rides_by_Driver = 'Personal & Car related issue';
    """
    cursor.execute(query)
    results = cursor.fetchone()
    st.markdown(f"<h3 style='font-size:22px;'>Driver Cancellations (Personal & Car Issues): <b>{results[0]}</b></h3>", unsafe_allow_html=True)

# 6. Max & Min Ratings for Prime Sedan
elif selected_analysis == analysis_options[6]:
    query = """
    SELECT 
        MAX(Driver_Ratings),
        MIN(Driver_Ratings)
    FROM ola_rides
    WHERE Vehicle_Type = 'Prime Sedan' AND Driver_Ratings >= 1
    """
    cursor.execute(query)
    results = cursor.fetchone()
    st.markdown(f"""
    <h4 style='font-size:22px;'>Prime Sedan Ratings</h4>
    <p style='font-size:18px;'>Maximum: <b>{results[0]}</b><br>Minimum: <b>{results[1]}</b></p>
    """, unsafe_allow_html=True)

# 7. UPI Payment Ride Trend
elif selected_analysis == analysis_options[7]:
    query = """
    SELECT *
    FROM ola_rides
    WHERE Payment_Method = 'UPI'
    """
    cursor.execute(query)
    results = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(results, columns=columns)
    df['Date'] = pd.to_datetime(df['Date'])
    trend = df.groupby('Date').size()
    fig, ax = plt.subplots(figsize=(12, 6))
    trend.plot(ax=ax, marker='o', color='blue')
    ax.set_title("UPI Payment Rides Over Time", fontsize=18)
    ax.set_xlabel("Date", fontsize=14)
    ax.set_ylabel("Number of Rides", fontsize=14)
    st.pyplot(fig)

# 8. Avg Customer Rating by Vehicle Type
elif selected_analysis == analysis_options[8]:
    query = """
    SELECT Vehicle_Type, AVG(Customer_Rating)
    FROM ola_rides
    GROUP BY Vehicle_Type
    ORDER BY AVG(Customer_Rating)
    """
    cursor.execute(query)
    results = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(results, columns=columns)
    st.dataframe(df)

# 9. Total Booking Value of Successful Rides
elif selected_analysis == analysis_options[9]:
    query ="""
    SELECT SUM(Booking_Value)
    FROM ola_rides
    WHERE Booking_Status = 'SUCCESS' AND Incomplete_Rides = 'No'
    """
    cursor.execute(query)
    results = cursor.fetchone()
    st.markdown(f"""
    <h3 style='font-size:24px;'>Total Revenue from Successful Rides:</h3>
    <p style='font-size:30px; font-weight:bold;'>₹{results[0]:,.2f}</p>
    """, unsafe_allow_html=True)

# 10. Incomplete Rides by Reason & Vehicle Type
elif selected_analysis == analysis_options[10]:
    query = """
    SELECT * FROM ola_rides
    WHERE Incomplete_Rides = 'Yes' AND Incomplete_Rides_Reason != 'Not Applicable'
    """
    cursor.execute(query)
    results = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(results, columns=columns)
    grouped = df.groupby(['Vehicle_Type', 'Incomplete_Rides_Reason']).size().unstack(fill_value=0)
    fig, ax = plt.subplots(figsize=(12, 6))
    grouped.plot(kind='bar', stacked=True, ax=ax, colormap='tab20')
    ax.set_title("Incomplete Rides by Reason and Vehicle Type", fontsize=18)
    ax.set_xlabel("Vehicle Type", fontsize=14)
    ax.set_ylabel("Number of Rides", fontsize=14)
    st.pyplot(fig)
