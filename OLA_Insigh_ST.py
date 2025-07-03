import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from st_files_connection import FilesConnection

# Page Config
st.set_page_config(page_title="OLA Ride Insights", layout="wide")

# Initial Landing Page
if "view_analysis" not in st.session_state:
    st.session_state.view_analysis = False

# Main Title
st.title("OLA Ride Insights")

if not st.session_state.view_analysis:
    st.header("Welcome to the OLA Ride Insights Dashboard")
    st.write("Click below to explore the analysis of bookings, revenue, and performance metrics.")
    if st.button("Click to View Analysis", use_container_width=True):
        st.session_state.view_analysis = True
    st.stop()

# Back Button
if st.button("Back to Dashboard"):
    st.session_state.view_analysis = False
    st.rerun()

# Connect to S3 with proper configuration
try:
    conn = st.connection(
        "s3",
        type=FilesConnection,
        config={
            "client_kwargs": {
                "aws_access_key_id": st.secrets["connections.s3"]["aws_access_key_id"],
                "aws_secret_access_key": st.secrets["connections.s3"]["aws_secret_access_key"],
                "region_name": st.secrets["connections.s3"]["region"]
            }
        }
    )
    
    df = conn.read("ashvinstreamlit/ola_name.csv", input_format="csv", ttl=600)
    
    # Data preprocessing
    df['Date'] = pd.to_datetime(df['Date'])
    df['Customer_ID'] = df['Customer_ID'].str.strip()
    
    # Analysis dropdown
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

    # Analysis 1
    if selected_analysis == analysis_options[1]:
        st.subheader("Successful Bookings Over Time")
        result_df = df[df['Booking_Status'] == 'SUCCESS']
        daily_counts = result_df.groupby('Date').size()
        fig, ax = plt.subplots(figsize=(12, 6))
        daily_counts.plot(ax=ax, marker='o', color='green')
        ax.set_xlabel("Date")
        ax.set_ylabel("Number of Bookings")
        st.pyplot(fig)

    # Analysis 2
    elif selected_analysis == analysis_options[2]:
        st.subheader("Average Ride Distance per Vehicle Type")
        result_df = df[df['Booking_Status'] == 'SUCCESS']
        avg_distance = result_df.groupby('Vehicle_Type')['Ride_Distance'].mean().sort_values()
        st.bar_chart(avg_distance)

    # Analysis 3
    elif selected_analysis == analysis_options[3]:
        st.subheader("Total Cancelled Rides by Customers")
        total_canceled = df[df['Canceled_Rides_by_Customer'] != 'Not Applicable'].shape[0]
        st.metric("Total Cancellations", total_canceled)

    # Analysis 4
    elif selected_analysis == analysis_options[4]:
        st.subheader("Top 5 Customers by Ride Count")
        result_df = df[df['Booking_Status'] == 'SUCCESS']
        top_customers = result_df['Customer_ID'].value_counts().head(5)
        st.dataframe(top_customers.rename("Ride Count"))

    # Analysis 5
    elif selected_analysis == analysis_options[5]:
        st.subheader("Driver Cancellations (Personal/Car Issue)")
        count = df[df['Canceled_Rides_by_Driver'] == 'Personal & Car related issue'].shape[0]
        st.metric("Total Cancellations", count)

    # Analysis 6
    elif selected_analysis == analysis_options[6]:
        st.subheader("Prime Sedan Ratings")
        result_df = df[(df['Vehicle_Type'] == 'Prime Sedan') & (df['Driver_Ratings'] >= 1)]
        col1, col2 = st.columns(2)
        col1.metric("Maximum Rating", result_df['Driver_Ratings'].max())
        col2.metric("Minimum Rating", result_df['Driver_Ratings'].min())

    # Analysis 7
    elif selected_analysis == analysis_options[7]:
        st.subheader("UPI Payment Ride Trend")
        upi_df = df[df['Payment_Method'] == 'UPI']
        upi_trend = upi_df.groupby('Date').size()
        st.line_chart(upi_trend)

    # Analysis 8
    elif selected_analysis == analysis_options[8]:
        st.subheader("Avg Customer Rating by Vehicle Type")
        avg_rating = df.groupby('Vehicle_Type')['Customer_Rating'].mean().sort_values()
        st.bar_chart(avg_rating)

    # Analysis 9
    elif selected_analysis == analysis_options[9]:
        st.subheader("Total Booking Value of Successful Rides")
        result_df = df[(df['Booking_Status'] == 'SUCCESS') & (df['Incomplete_Rides'] == 'No')]
        total_value = result_df['Booking_Value'].sum()
        st.metric("Total Revenue", f"₹{total_value:,.2f}")

    # Analysis 10
    elif selected_analysis == analysis_options[10]:
        st.subheader("Incomplete Rides by Reason & Vehicle Type")
        incomplete_df = df[(df['Incomplete_Rides'] == 'Yes') & (df['Incomplete_Rides_Reason'] != 'Not Applicable')]
        pivot = incomplete_df.pivot_table(
            index='Vehicle_Type',
            columns='Incomplete_Rides_Reason',
            aggfunc='size',
            fill_value=0
        )
        st.bar_chart(pivot)

except Exception as e:
    st.error(f"An error occurred: {str(e)}")
    st.info("Please check your data connection and try again")
