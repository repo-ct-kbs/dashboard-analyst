import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import json

with open('dataset_user.json', 'r') as f:
    guest_data = json.load(f)

def extract_guest_info(guest):
    first_name = guest['name']['firstname']['name']
    last_name = guest['name']['lastname']['name']
    country_code = guest['country']['country_code']
    email = guest['email']
    
    return {
        "name": f"{first_name} {last_name}",
        "country_code": country_code,
        "identity_number": f"{random.randint(10000000, 99999999)}",
        "age": random.randint(18, 65),
        "gender": guest['name']['firstname']['gender_formatted'].capitalize(),
        "phone": f"+62-{random.randint(1000000, 9999999)}",
        "email": email
    }

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

reservation_types = ["OTA-Booking.com", "OTA-Traveloka", "OTA-Tiket.com", "Group Travel Agent", "Walk-in"]

daily_bookings = {hotel: {} for hotel in hotels}
guest_last_checkout = {}

num_transactions = 100000
transactions = []

for i in range(num_transactions):
    hotel = random.choice(list(hotels.keys()))
    room_info = random.choice(hotels[hotel])

    while True:
        date = datetime(2020, 1, 1) + timedelta(days=random.randint(0, (datetime(2024, 12, 31) - datetime(2020, 1, 1)).days))
        date_str = date.strftime('%Y-%m-%d')

        if date_str not in daily_bookings[hotel]:
            daily_bookings[hotel][date_str] = {room["room_type"]: 0 for room in hotels[hotel]}

        if daily_bookings[hotel][date_str][room_info["room_type"]] < room_info["rooms"]:
            daily_bookings[hotel][date_str][room_info["room_type"]] += 1
            break

    night_stay = random.randint(1, 10)
    
    booking_time = date - timedelta(days=random.randint(1, 30))
    booking_time = booking_time.replace(hour=random.randint(0, 23), minute=random.randint(0, 59))

    check_in_time = date.replace(hour=random.randint(8, 14), minute=random.randint(0, 59))
    
    check_out_time = (check_in_time + timedelta(days=night_stay)).replace(hour=random.randint(8, 12), minute=random.randint(0, 59))

    while True:
        guest_identity = extract_guest_info(random.choice(guest_data))
        guest_id = guest_identity['identity_number']
        
        if guest_id not in guest_last_checkout or (guest_last_checkout[guest_id] + timedelta(days=21)) <= check_in_time:
            guest_last_checkout[guest_id] = check_out_time
            break

    transaction = {
        "id": i + 1,
        "booking_time": booking_time,
        "hotel_name": hotel,
        "room_type": room_info["room_type"],
        "price": room_info["price"],
        "reservation_type": random.choice(reservation_types),
        "check_in_time": check_in_time,
        "check_out_time": check_out_time,
        "adults": random.randint(1, 4),
        "children": random.randint(0, 2),
        "night_stay": night_stay,
        "guest_identity": guest_identity
    }

    transactions.append(transaction)

    df = pd.DataFrame(transactions)
    guest_df = pd.json_normalize(df['guest_identity'])
    df = pd.concat([df.drop(columns=['guest_identity']), guest_df], axis=1)

    df.to_json("hotel_booking_history-2.json", orient="records", date_format="iso")

    print("Dataset created and saved as 'hotel_booking_history.json'", i)
