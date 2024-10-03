import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

# Helper function yang dibutuhkan untuk menyiapkan berbagai dataframe

def create_daily_rentals(df):
    daily_rentals_df = df.resample(rule='D', on='dteday').agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    
    daily_rentals_df = daily_rentals_df.reset_index()
    
    daily_rentals_df.rename(columns={
        "casual": "total_casual",
        "registered": "total_registered",
        "cnt": "total_rentals"
    }, inplace=True)
    
    return daily_rentals_df

def create_weekly_rentals(df):
    weekly_rentals = df.groupby('weekday')['cnt'].mean().reset_index()
    weekly_rentals.columns = ['Weekday', 'Average Rentals']
    return weekly_rentals

def create_monthly_rentals(df):
    monthly_rentals = df.groupby('mnth')['cnt'].mean().reset_index()
    monthly_rentals.columns = ['Month', 'Average Rentals']
    return monthly_rentals

def create_weather_rentals(df):
    # Menghitung rata-rata penyewaan sepeda berdasarkan kondisi cuaca dengan kategori lengkap (1-4)
    complete_weather_categories = pd.DataFrame({
        'Weather': [1, 2, 3, 4],
        'Average Rentals': [0, 0, 0, 0]  # Default nilai untuk kategori tanpa data
    })

    weather_rentals = df.groupby('weathersit')['cnt'].mean().reset_index()
    weather_rentals.columns = ['Weather', 'Average Rentals']

    weather_rentals_complete = pd.merge(complete_weather_categories, weather_rentals, 
                                        on='Weather', how='left', suffixes=('_default', '_calculated'))

    weather_rentals_complete['Average Rentals_calculated'].fillna(0, inplace=True)
    weather_rentals_complete['Average Rentals'] = weather_rentals_complete['Average Rentals_calculated']

    return weather_rentals_complete

def create_season_rentals(df):
    season_rentals = df.groupby('season')['cnt'].mean().reset_index()
    season_rentals.columns = ['Season', 'Average Rentals']
    return season_rentals

def create_workingday_rentals(df):
    workingday_rentals = df.groupby('workingday')['cnt'].mean().reset_index()
    workingday_rentals.columns = ['Working Day', 'Average Rentals']
    return workingday_rentals

def create_holiday_rentals(df):
    holiday_rentals = df.groupby('holiday')['cnt'].mean().reset_index()
    holiday_rentals.columns = ['Holiday', 'Average Rentals']
    return holiday_rentals

def create_rental_distribution(df):
    rental_distribution = df['rental_group'].value_counts()
    return rental_distribution

# Load cleaned data
main_data = pd.read_csv("main_data.csv")

main_data.sort_values(by="dteday", inplace=True)
main_data.reset_index(inplace=True)

main_data["dteday"] = pd.to_datetime(main_data["dteday"])

# Filter data
min_date = main_data["dteday"].min()
max_date = main_data["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Date Range',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = main_data[(main_data["dteday"] >= str(start_date)) & (main_data["dteday"] <= str(end_date))]

# st.dataframe(main_df)

# Menyiapkan berbagai dataframe
daily_rentals_df = create_daily_rentals(main_df)
weekly_rentals_df = create_weekly_rentals(main_df)
monthly_rentals_df = create_monthly_rentals(main_df)
weather_rentals_complete_df = create_weather_rentals(main_df)
season_rentals_df = create_season_rentals(main_df)
workingday_rentals_df = create_workingday_rentals(main_df)
holiday_rentals_df = create_holiday_rentals(main_df)
rental_distribution_df = create_rental_distribution(main_df)

# Judul
st.header('Bike Sharing Dashboard :sparkles:')
st.subheader('Daily Rentals')

# Total casual users, registered users, dan total rental
col1, col2, col3 = st.columns(3)

with col1:
    total_casual = daily_rentals_df.total_casual.sum()
    st.metric("Total Casual Users", value=total_casual)

with col2:
    total_registered = daily_rentals_df.total_registered.sum() 
    st.metric("Total Registered Users", value=total_registered)

with col3:
    total_rentals = daily_rentals_df.total_rentals.sum() 
    st.metric("Total Rentals", value=total_rentals)

# Daily rentals
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_rentals_df["dteday"],
    daily_rentals_df["total_rentals"],
    marker='o', 
    linewidth=2,
    color="#4a91a5"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

# Weekly dan Monthly rentals

col1, col2 = st.columns(2)

with col1:
    colors = ["#FF6969", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#4a91a5","#D3D3D3"]
    weekly_labels = {1: 'Sunday', 2: 'Monday', 3: 'Tuesday', 4: 'Wednesday', 5: 'Thursday', 6: 'Friday', 7: 'Saturday'}

    st.subheader("Average Weekly Rentals")
    plt.figure(figsize=(8, 6))
    sns.barplot(x='Weekday', y='Average Rentals', data=weekly_rentals_df, palette=colors)
    plt.ylabel(None)
    plt.xlabel(None)
    plt.tick_params(axis='y', labelsize=10)
    plt.xticks(ticks=[0, 1, 2, 3, 4, 5, 6], labels=[weekly_labels[1], weekly_labels[2], weekly_labels[3], weekly_labels[4],
                                                    weekly_labels[5], weekly_labels[6], weekly_labels[7]])
    st.pyplot(plt)

with col2:
    colors = ["#FF6969", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#4a91a5","#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3","#D3D3D3"]
    monthly_labels = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'Mai', 6: 'Jun',
                    7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}

    st.subheader("Average Monthly Rentals")
    plt.figure(figsize=(8, 6))
    sns.barplot(x='Month', y='Average Rentals', data=monthly_rentals_df, palette=colors)
    plt.ylabel(None)
    plt.xlabel(None)
    plt.tick_params(axis='y', labelsize=10)
    plt.xticks(ticks=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], labels=[monthly_labels[1], monthly_labels[2], monthly_labels[3], monthly_labels[4], monthly_labels[5], monthly_labels[6],
                                                                 monthly_labels[7], monthly_labels[8], monthly_labels[9], monthly_labels[10], monthly_labels[11], monthly_labels[12]])
    st.pyplot(plt)

# Rata-rata penyewaan sepeda berdasarkan kondisi cuaca
colors = ["#4a91a5", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
weather_labels = {
    1: 'Clear, Few clouds, Partly cloudy',
    2: 'Mist, Cloudy, Broken clouds, Few clouds',
    3: 'Light Snow, Light Rain, Thunderstorm, Scattered clouds',
    4: 'Heavy Rain, Ice Pallets, Thunderstorm, Mist, Snow, Fog'
}

st.subheader("Average Rentals Based on Weather Condition")
plt.figure(figsize=(10, 6))
sns.barplot(x='Average Rentals', y='Weather', data=weather_rentals_complete_df, palette=colors, orient='h')
plt.ylabel(None)
plt.xlabel(None)
plt.tick_params(axis='y', labelsize=10)
plt.yticks(ticks=[0, 1, 2, 3], labels=[weather_labels[1], weather_labels[2], weather_labels[3], weather_labels[4]])
st.pyplot(plt)

# Rata-rata penyewaan sepeda berdasarkan kondisi musim, korelasi antara suhu dan penyewaan sepeda
colors = ["#D3D3D3", "#D3D3D3", "#4a91a5", "#D3D3D3"]
season_labels = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}

col1, col2 = st.columns(2)

with col1:
    st.subheader("Average Rentals Based on Season")
    plt.figure(figsize=(8, 5))
    sns.barplot(x='Season', y='Average Rentals', data=season_rentals_df, palette=colors)
    plt.ylabel(None)
    plt.xlabel(None)
    plt.tick_params(axis='y', labelsize=10)
    plt.xticks(ticks=[0, 1, 2, 3], labels=[season_labels[1], season_labels[2], season_labels[3], season_labels[4]])
    st.pyplot(plt)

with col2:
    st.subheader("Correlation between Temperature & Rentals")
    plt.figure(figsize=(8, 5))
    sns.regplot(x='temp', y='cnt', data=main_df, color='#4a91a5')
    plt.ylabel(None)
    plt.xlabel('Temperature (`C)')
    plt.tick_params(axis='y', labelsize=10)
    st.pyplot(plt)

# Rata-rata penyewaan sepeda berdasarkan hari kerja dan hari libur
col1, col2 = st.columns(2)

with col1:
    colors = ["#D3D3D3", "#4a91a5"]
    workingday_labels = {1: 'Not Working Day', 2: 'Working Day'}
    
    st.subheader("Average Rentals Based on Working Day")
    plt.figure(figsize=(8, 5))
    sns.barplot(x='Working Day', y='Average Rentals', data=workingday_rentals_df, estimator='mean', ci=None, palette=colors)
    plt.ylabel(None)
    plt.xlabel(None)
    plt.tick_params(axis='y', labelsize=10)
    plt.xticks(ticks=[0, 1], labels=[workingday_labels[1], workingday_labels[2]])
    st.pyplot(plt)

with col2:
    colors = ["#4a91a5", "#D3D3D3"]
    holiday_labels = {1: 'Not Holiday', 2: 'Holiday'}

    st.subheader("Average Rentals Based on Holiday")
    plt.figure(figsize=(8, 5))
    sns.barplot(x='Holiday', y='Average Rentals', data=holiday_rentals_df, estimator='mean', ci=None, palette=colors)
    plt.ylabel(None)
    plt.xlabel(None)
    plt.tick_params(axis='y', labelsize=10)
    plt.xticks(ticks=[0, 1], labels=[holiday_labels[1], holiday_labels[2]])
    st.pyplot(plt)

# Kategori jumlah penyewaan sepeda
labels = rental_distribution_df.index
colors = ["#4a91a5", "#FCDE70", "#FF6969"]

st.subheader('Category Distribution of Total Rentals')
plt.figure(figsize=(8, 6))
plt.pie(rental_distribution_df, labels=labels, autopct='%1.1f%%', colors=colors)
plt.axis('equal')
st.pyplot(plt)