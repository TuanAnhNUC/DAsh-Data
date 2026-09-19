import pandas as pd
df = pd.read_csv("full_plane_data.csv")

print(df.head())
print(df.columns)
print(df.shape)

# Tách tạo thành table customers
customers = df[
    [
        'Passenger_ID',
        'Age',
        'Gender',
        'Income_Level',
        'Frequent_Flyer_Status',

    ]
].drop_duplicates("Passenger_ID")
print(customers.head())
customers.to_csv('customers.csv', index=False)
print(df['Departure_Time'].head())
print(df['Departure_Time'].dtype)

df['Departure_Time'] = pd.to_datetime(df['Departure_Time'], format = "%d/%m/%Y %H:%M")

df['Departure_Date'] = df['Departure_Time'].dt.date
df['Departure_Hour'] = df['Departure_Time'].dt.time

#print(df[["Departure_Time", 'Departure_Date', 'Departure_Hour']].head(30))



bookings = df[
    [
        'Passenger_ID',
        'Flight_ID',
        'Price_USD',
        'Travel_Purpose',
        'Seat_Class',
        'Bags_Checked',
        'Check_in_Method',
        'Seat_Selected',
        'Booking_Days_In_Advance',
        'No_Show'
        ]]

bookings.to_csv('bookings.csv', index = False)

flights = df[
    [
        'Flight_ID',
        'Airline',
        'Departure_Airport',
        'Arrival_Airport',
        'Departure_Time',
        'Departure_Date', 
        'Departure_Hour',
        'Flight_Duration_Minutes',
        'Flight_Status',
        'Distance_Miles',
        'Delay_Minutes',
        'Weather_Impact'        
        ]].drop_duplicates('Flight_ID')
flights.to_csv('flights.csv', index=False)

print(df["Departure_Airport"].unique())
print(df["Arrival_Airport"].unique())

print("From:", df["Departure_Date"].min())
print("To:", df["Departure_Date"].max())

stations = {
    "JFK": "74486",
    "ORD": "72530",
    "SEA": "72793",
    "LAX": "72295",
    "SFO": "72494",
    "ATL": "72219",
    "DFW": "72259",
    "DEN": "72565"
}

all_weather = []

all_weather = []

for airport, station in stations.items():

    print(f"Đang tải {airport}...")

    for year in [2023, 2024, 2025]:

        url = f"https://data.meteostat.net/daily/{year}/{station}.csv.gz"

        weather = pd.read_csv(url)

        weather["Airport"] = airport

        all_weather.append(weather)

weather = pd.concat(all_weather, ignore_index=True)

weather["date"] = pd.to_datetime(
    weather[["year", "month", "day"]]
)

weather = weather[
    (weather["date"] >= "2023-04-23") &
    (weather["date"] <= "2025-04-22")
]

weather = weather[
    [
        "date",
        "Airport",
        "temp",
        "tmin",
        "tmax",
        "prcp",
        "wspd"
    ]
]

print(weather.head())
print(weather.shape)

print(flights.head())
print(flights.columns)

flights["Departure_Date"] = pd.to_datetime(flights["Departure_Date"]).dt.normalize()
weather["date"] = pd.to_datetime(weather["date"]).dt.normalize()

print(flights["Departure_Date"].dtype)
print(weather["date"].dtype)

flights_weather = flights.merge(
    weather,
    left_on=["Departure_Airport", "Departure_Date"],
    right_on=["Airport", "date"],
    how="left"
)

print(flights_weather.head())
print(flights_weather.shape)

weather.to_csv('weather.csv', index=False)

print(flights_weather[["temp", "tmin", "tmax", "prcp", "wspd"]].isnull().sum())

print(
    flights_weather.groupby("Departure_Airport")["temp"]
    .apply(lambda x: x.isna().sum())
)

print(bookings.shape)
print(bookings.head)

final_data = bookings.merge(flights_weather, on='Flight_ID', how='left')

final_data['Route'] = (final_data['Departure_Airport']+'-'+final_data['Arrival_Airport'])

final_data.to_csv('final_booking_data.csv', index=False)

print("Bookings:", bookings.shape)
print("Flights weather:", flights_weather.shape)
print("Final:", final_data.shape)

print(final_data[
    [
        "Passenger_ID",
        "Flight_ID",
        "Departure_Date",
        "Route",
        "Price_USD",
        "Delay_Minutes",
        "temp",
        "prcp"
    ]
].head(10))
print(final_data.columns)

final_data.to_csv('final_booking_data.csv', index=False)

print("Shape:", final_data.shape)
print("Duplicate rows:", final_data.duplicated().sum())
print("\nMissing values:")
print(final_data.isnull().sum())