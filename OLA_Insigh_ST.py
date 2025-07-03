import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from st_files_connection import FilesConnection

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

# Connect to S3 CSV
conn = st.connection("s3", type=FilesConnection)
df = conn.read("ashvinstreamlit/ola_name.csv", input_format="csv", ttl=600)
df['Date'] = pd.to_datetime(df['Date'])  # Ensure Date column is parsed

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
    result_df = df[df['Booking_Status'] == 'SUCCESS']
    daily_counts = result_df.groupby('Date').size()
    fig, ax = plt.subplots(figsize=(12, 6))
    daily_counts.plot(ax=ax, marker='o', color='green')
    ax.set_title("Successful Bookings Over Time", fontsize=18)
    ax.set_xlabel("Date", fontsize=14)
    ax.set_ylabel("Number of Bookings", fontsize=14)
    st.pyplot(fig)

# 2. Average Ride Distance per Vehicle Type
elif selected_analysis == analysis_options[2]:
    result_df = df[df['Booking_Status'] == 'SUCCESS']
    avg_distance = result_df.groupby('Vehicle_Type')['Ride_Distance'].mean().reset_index()
    avg_distance.columns = ['Vehicle_Type', 'Avg_Ride_Distance']
    st.dataframe(avg_distance)

# 3. Total Cancelled Rides by Customers
elif selected_analysis == analysis_options[3]:
    total_canceled = df[df['Canceled_Rides_by_Customer'] != 'Not Applicable'].shape[0]
    st.markdown(f"<h3 style='font-size:22px;'>Total Cancelled Rides by Customers: <b>{total_canceled}</b></h3>", unsafe_allow_html=True)

# 4. Top 5 Customers by Ride Count
elif selected_analysis == analysis_options[4]:
    result_df = df[df['Booking_Status'] == 'SUCCESS']
    top_customers = result_df['Customer_ID'].str.strip().value_counts().head(5).reset_index()
    top_customers.columns = ['CUSTOMERS', 'TOTAL_RIDES']
    st.dataframe(top_customers)

# 5. Driver Cancellations (Personal/Car Issue)
elif selected_analysis == analysis_options[5]:
    count = df[df['Canceled_Rides_by_Driver'] == 'Personal & Car related issue'].shape[0]
    st.markdown(f"<h3 style='font-size:22px;'>Driver Cancellations (Personal & Car Issues): <b>{count}</b></h3>", unsafe_allow_html=True)

# 6. Max & Min Ratings for Prime Sedan
elif selected_analysis == analysis_options[6]:
    result_df = df[(df['Vehicle_Type'] == 'Prime Sedan') & (df['Driver_Ratings'] >= 1)]
    max_rating = result_df['Driver_Ratings'].max()
    min_rating = result_df['Driver_Ratings'].min()
    st.markdown(f"""
    <h4 style='font-size:22px;'>Prime Sedan Ratings</h4>
    <p style='font-size:18px;'>Maximum: <b>{max_rating}</b><br>Minimum: <b>{min_rating}</b></p>
    """, unsafe_allow_html=True)

# 7. UPI Payment Ride Trend
elif selected_analysis == analysis_options[7]:
    upi_df = df[df['Payment_Method'] == 'UPI']
    upi_trend = upi_df.groupby('Date').size()
    fig, ax = plt.subplots(figsize=(12, 6))
    upi_trend.plot(ax=ax, marker='o', color='blue')
    ax.set_title("UPI Payment Rides Over Time", fontsize=18)
    ax.set_xlabel("Date", fontsize=14)
    ax.set_ylabel("Number of Rides", fontsize=14)
    st.pyplot(fig)

# 8. Avg Customer Rating by Vehicle Type
elif selected_analysis == analysis_options[8]:
    avg_rating = df.groupby('Vehicle_Type')['Customer_Rating'].mean().reset_index()
    avg_rating.columns = ['Vehicle_Type', 'Average_Customer_Rating']
    st.dataframe(avg_rating)

# 9. Total Booking Value of Successful Rides
elif selected_analysis == analysis_options[9]:
    result_df = df[(df['Booking_Status'] == 'SUCCESS') & (df['Incomplete_Rides'] == 'No')]
    total_value = result_df['Booking_Value'].sum()
    st.markdown(f"""
    <h3 style='font-size:24px;'>Total Revenue from Successful Rides:</h3>
    <p style='font-size:30px; font-weight:bold;'>₹{total_value:,.2f}</p>
    """, unsafe_allow_html=True)

# 10. Incomplete Rides by Reason & Vehicle Type
elif selected_analysis == analysis_options[10]:
    incomplete_df = df[(df['Incomplete_Rides'] == 'Yes') & (df['Incomplete_Rides_Reason'] != 'Not Applicable')]
    grouped = incomplete_df.groupby(['Vehicle_Type', 'Incomplete_Rides_Reason']).size().unstack(fill_value=0)
    fig, ax = plt.subplots(figsize=(12, 6))
    grouped.plot(kind='bar', stacked=True, ax=ax, colormap='tab20')
    ax.set_title("Incomplete Rides by Reason and Vehicle Type", fontsize=18)
    ax.set_xlabel("Vehicle Type", fontsize=14)
    ax.set_ylabel("Number of Rides", fontsize=14)
    st.pyplot(fig)
