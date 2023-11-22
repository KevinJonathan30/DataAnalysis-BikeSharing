import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

def create_daily_rentals_df(df):
    daily_rentals_df = df.resample(rule='D', on='dteday').agg({
        "cnt_hourly": "sum"
    })
    daily_rentals_df = daily_rentals_df.reset_index()
    daily_rentals_df.rename(columns={
        "cnt_hourly": "rentals"
    }, inplace=True)
    
    return daily_rentals_df


all_df = pd.read_csv("all_data.csv")

datetime_columns = ["dteday"]
all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(inplace=True)

for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

# Filter data
min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()

with st.sidebar:
    st.header('Bike Sharing Dashboard :sparkles:')
    
    try:
        start_date, end_date = st.date_input(
            label='Date Range',min_value=min_date,
            max_value=max_date,
            value=[min_date, max_date]
        )
        
    except (ValueError):
        print(ValueError)
    
try:
    main_df = all_df[(all_df["dteday"] >= str(start_date)) & 
                    (all_df["dteday"] <= str(end_date))]
    
    # st.dataframe(main_df)
    
    daily_rentals_df = create_daily_rentals_df(main_df)
    
    
    # plot number of daily rentals
    st.header('Bike Sharing Dashboard :sparkles:')
    st.subheader('Daily Rental Usage')
    
    total_rentals = daily_rentals_df.rentals.sum()
    st.metric("Total rentals", value=total_rentals)
    
    
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.plot(
        daily_rentals_df["dteday"],
        daily_rentals_df["rentals"],
        marker='o', 
        linewidth=2,
        color="#90CAF9"
    )
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=15)
    
    st.pyplot(fig)
    
    col1, col2 = st.columns(2)
    with col1:
        # Rental By Season
        st.subheader("Rental By Season")
        if main_df['season_daily'].nunique() >= 4:
            seasonal_data = main_df.groupby('season_daily')['cnt_daily'].mean()
            season_labels = ['Springer', 'Summer', 'Fall', 'Winter']
        
            fig, ax = plt.subplots(figsize=(20, 10))
        
            cols = ['grey' if (x < max(seasonal_data)) else 'orange' for x in seasonal_data]
        
            sns.barplot(x=seasonal_data, y=season_labels, palette=cols)
            ax.set_ylabel("Season")
            ax.set_xlabel("Daily Rental Average", fontsize=30)
            ax.set_title("How Season Affects Daily Rental Average", loc="center", fontsize=50)
            ax.tick_params(axis='y', labelsize=35)
            ax.tick_params(axis='x', labelsize=30)
        
            st.pyplot(fig)
        else:
            st.text("N/A (Try widening the date range)")
     
    with col2:
        # Rentals Based on Workday
        st.subheader("Rental Based on Workday")
    
        fig, ax = plt.subplots(figsize=(30, 15))
    
        sns.boxplot(x="workingday_daily", y="cnt_daily", data=main_df)
        ax.set_ylabel("Daily Rental Count")
        ax.set_xlabel("Working Day Status", fontsize=30)
        ax.set_title("Difference between Working Day and Non-Working Day in Daily Rental Count", loc="center", fontsize=50)
        ax.tick_params(axis='y', labelsize=35)
        ax.tick_params(axis='x', labelsize=30)
        ax.set_xticklabels(["Non-Working Day", "Working Day"])
    
        st.pyplot(fig)
except NameError:
    st.header('Bike Sharing Dashboard :sparkles:')
    st.subheader('Daily Rental Usage')
    st.text("Please enter the start and end date to show results.")
    


st.caption('Copyright © Kevin Jonathan 2023')
