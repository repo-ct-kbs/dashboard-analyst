import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

np.random.seed(0)

hotels = {
    "Haris Hotel": [
        {"room_type": "Family", "rooms": 30, "price": 1000000},
        {"room_type": "Deluxe", "rooms": 20, "price": 1500000},
        {"room_type": "Suite", "rooms": 15, "price": 2500000},
        {"room_type": "Standard", "rooms": 45, "price": 500000}
    ],
    "Cakra Hotel": [
        {"room_type": "Regular", "rooms": 25, "price": 1000000},
        {"room_type": "Fancy", "rooms": 10, "price": 2000000},
        {"room_type": "Presidential", "rooms": 5, "price": 3000000}
    ],
    "Aston Hotel": [
        {"room_type": "Standard", "rooms": 50, "price": 1500000},
        {"room_type": "Double", "rooms": 20, "price": 1750000},
        {"room_type": "Deluxe", "rooms": 10, "price": 2750000},
    ]
}

guest_identity = {
    "name",
    "country_code",
    "identity_number",
    "age",
    "gender",
    "phone",
    "email"
}

booking_time = ""

reservation_types = [
    "OTA-Booking.com", 
    "OTA-Traveloka", 
    "OTA-Tiket.com", 
    "OTA-Booking.com", 
    "Group Travel Agent",
    "Walk-in"
]
adults_range = (1, 4)
children_range = (0, 2)
night_stay_range = (1, 14)

num_transactions = 100000
transactions = []

for i in range(num_transactions):
    hotel = random.choice(list(hotels.keys()))
    room_info = random.choice(hotels[hotel])
    
    start_date = datetime(2020, 1, 1)
    end_date = datetime(2024, 12, 31)
    date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
    
    night_stay = random.randint(*night_stay_range)
    check_in_time = date + timedelta(hours=random.randint(14, 18))
    check_out_time = check_in_time + timedelta(days=night_stay, hours=random.randint(7, 11))

    price = room_info["price"] * night_stay

    transaction = {
        "id": i + 1,
        "date": date,
        "room_type": room_info["room_type"],
        "price": price,
        "reservation_type": random.choice(reservation_types),
        "check_in_time": check_in_time,
        "check_out_time": check_out_time,
        "adults": random.randint(*adults_range),
        "children": random.randint(*children_range),
        "night_stay": night_stay
    }
    transactions.append(transaction)

df = pd.DataFrame(transactions)

df.to_csv("hotel_booking_history.csv", index=False)

print("Dataset created and saved as 'hotel_booking_history.csv'")
