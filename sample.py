import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import json

# Load guest identities from JSON
with open('dataset_user.json', 'r') as f:
    guest_data = json.load(f)

# Extract guest identity attributes for use in transaction records
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

# Hotel and room data
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

# Reservation types
reservation_types = ["OTA-Booking.com", "OTA-Traveloka", "OTA-Tiket.com", "Group Travel Agent", "Walk-in"]

# Define booking limits to ensure room availability and restrict repeated bookings within 21 days
daily_bookings = {hotel: {} for hotel in hotels}
guest_last_checkout = {}  # Tracks last checkout for each guest to enforce 21-day rule

# Generate transactions
num_transactions = 100000
transactions = []

for i in range(num_transactions):
    # Random hotel and room type
    hotel = random.choice(list(hotels.keys()))
    room_info = random.choice(hotels[hotel])

    # Ensure room availability on chosen date
    while True:
        date = datetime(2020, 1, 1) + timedelta(days=random.randint(0, (datetime(2024, 12, 31) - datetime(2020, 1, 1)).days))
        date_str = date.strftime('%Y-%m-%d')

        if date_str not in daily_bookings[hotel]:
            daily_bookings[hotel][date_str] = {room["room_type"]: 0 for room in hotels[hotel]}

        if daily_bookings[hotel][date_str][room_info["room_type"]] < room_info["rooms"]:
            daily_bookings[hotel][date_str][room_info["room_type"]] += 1
            break

    # Night stay and check-in/check-out times
    night_stay = random.randint(1, 10)
    
    # Randomized booking_time (any time during the day)
    booking_time = date - timedelta(days=random.randint(1, 30))
    booking_time = booking_time.replace(hour=random.randint(0, 23), minute=random.randint(0, 59))

    # Set check-in time to a random hour up to 14:00
    check_in_time = date.replace(hour=random.randint(8, 14), minute=random.randint(0, 59))
    
    # Set check-out time on the final day, up to a maximum of 12:00
    check_out_time = (check_in_time + timedelta(days=night_stay)).replace(hour=random.randint(8, 12), minute=random.randint(0, 59))

    # Randomly select a guest from the loaded guest data and enforce 21-day rule
    while True:
        guest_identity = extract_guest_info(random.choice(guest_data))
        guest_id = guest_identity['identity_number']
        
        # Check the last checkout date for this guest
        if guest_id not in guest_last_checkout or (guest_last_checkout[guest_id] + timedelta(days=21)) <= check_in_time:
            guest_last_checkout[guest_id] = check_out_time
            break

    # Create transaction entry
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

    # Convert to DataFrame and expand guest_identity into separate columns
    df = pd.DataFrame(transactions)
    guest_df = pd.json_normalize(df['guest_identity'])
    df = pd.concat([df.drop(columns=['guest_identity']), guest_df], axis=1)

    # Save as JSON file
    df.to_json("hotel_booking_history-2.json", orient="records", date_format="iso")

    print("Dataset created and saved as 'hotel_booking_history.json'", i)
