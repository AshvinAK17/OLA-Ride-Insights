import streamlit as st
import pandas as pd
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

# Load data from GitHub
@st.cache_data(ttl=600)
def load_data():
    url = "https://raw.githubusercontent.com/AshvinAK17/OLA-Ride-Insights/main/ola_name.csv"
    try:
        df = pd.read_csv(url, encoding='utf-8', on_bad_lines='skip')
        return df
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return pd.DataFrame()

df = load_data()
if df.empty:
    st.stop()

# Convert columns
if 'Date' in df.columns:
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df['Customer_ID'] = df['Customer_ID'].astype(str).str.strip()

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

if selected_analysis == analysis_options[1]:
    st.subheader("Successful Bookings Over Time")
    result_df = df[df['Booking_Status'] == 'SUCCESS']
    daily_counts = result_df.groupby('Date').size()
    fig, ax = plt.subplots(figsize=(12, 6))
    daily_counts.plot(ax=ax, marker='o', color='green')
    ax.set_title("Successful Bookings Over Time", fontsize=18)
    st.pyplot(fig)

elif selected_analysis == analysis_options[2]:
    st.subheader("Average Ride Distance per Vehicle Type")
    result_df = df[df['Booking_Status'] == 'SUCCESS']
    avg_distance = result_df.groupby('Vehicle_Type')['Ride_Distance'].mean().reset_index()
    st.dataframe(avg_distance)

elif selected_analysis == analysis_options[3]:
    st.subheader("Total Cancelled Rides by Customers")
    total_canceled = df[df['Canceled_Rides_by_Customer'] != 'Not Applicable'].shape[0]
    st.markdown(f"<h3 style='font-size:22px;'>Total Cancelled Rides by Customers: <b>{total_canceled}</b></h3>", unsafe_allow_html=True)

elif selected_analysis == analysis_options[4]:
    st.subheader("Top 5 Customers by Ride Count")
    result_df = df[df['Booking_Status'] == 'SUCCESS']
    top_customers = result_df['Customer_ID'].value_counts().head(5).reset_index()
    top_customers.columns = ['CUSTOMERS', 'TOTAL_RIDES']
    st.dataframe(top_customers)

elif selected_analysis == analysis_options[5]:
    st.subheader("Driver Cancellations (Personal/Car Issue)")
    count = df[df['Canceled_Rides_by_Driver'] == 'Personal & Car related issue'].shape[0]
    st.markdown(f"<h3 style='font-size:22px;'>Driver Cancellations (Personal & Car Issues): <b>{count}</b></h3>", unsafe_allow_html=True)

elif selected_analysis == analysis_options[6]:
    st.subheader("Max & Min Ratings for Prime Sedan")
    sedan_df = df[(df['Vehicle_Type'] == 'Prime Sedan') & (df['Driver_Ratings'] >= 1)]
    max_rating = sedan_df['Driver_Ratings'].max()
    min_rating = sedan_df['Driver_Ratings'].min()
    st.markdown(f"""
    <h4 style='font-size:22px;'>Prime Sedan Ratings</h4>
    <p style='font-size:18px;'>Maximum: <b>{max_rating}</b><br>Minimum: <b>{min_rating}</b></p>
    """, unsafe_allow_html=True)

elif selected_analysis == analysis_options[7]:
    st.subheader("UPI Payment Ride Trend")
    upi_df = df[df['Payment_Method'] == 'UPI']
    upi_df['Date'] = pd.to_datetime(upi_df['Date'], errors='coerce')
    upi_trend = upi_df.groupby('Date').size()
    fig, ax = plt.subplots(figsize=(12, 6))
    upi_trend.plot(ax=ax, marker='o', color='blue')
    ax.set_title("UPI Payment Rides Over Time", fontsize=18)
    st.pyplot(fig)

elif selected_analysis == analysis_options[8]:
    st.subheader("Avg Customer Rating by Vehicle Type")
    avg_rating = df.groupby('Vehicle_Type')['Customer_Rating'].mean().reset_index()
    st.dataframe(avg_rating.sort_values(by='Customer_Rating'))

elif selected_analysis == analysis_options[9]:
    st.subheader("Total Booking Value of Successful Rides")
    result_df = df[(df['Booking_Status'] == 'SUCCESS') & (df['Incomplete_Rides'] == 'No')]
    total_value = result_df['Booking_Value'].sum()
    st.markdown(f"""
    <h3 style='font-size:24px;'>Total Revenue from Successful Rides:</h3>
    <p style='font-size:30px; font-weight:bold;'>₹{total_value:,.2f}</p>
    """, unsafe_allow_html=True)

elif selected_analysis == analysis_options[10]:
    st.subheader("Incomplete Rides by Reason & Vehicle Type")
    incomplete_df = df[(df['Incomplete_Rides'] == 'Yes') & (df['Incomplete_Rides_Reason'] != 'Not Applicable')]
    grouped = incomplete_df.groupby(['Vehicle_Type', 'Incomplete_Rides_Reason']).size().unstack(fill_value=0)
    fig, ax = plt.subplots(figsize=(12, 6))
    grouped.plot(kind='bar', stacked=True, ax=ax, colormap='tab20')
    ax.set_title("Incomplete Rides by Reason and Vehicle Type", fontsize=18)
    ax.set_xlabel("Vehicle Type", fontsize=14)
    ax.set_ylabel("Number of Rides", fontsize=14)
    st.pyplot(fig)
