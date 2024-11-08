import json
import random

with open("hotel_booking_history-3.json") as f:
    transaction_data = json.load(f)

with open("hotel_set.json") as f:
    hotel_data = json.load(f)

def generate_add_on_transactions(transaction_data, hotel_data):
    add_on_transactions = []

    for transaction in transaction_data:
        hotel_name = transaction["hotel_name"]
        adults = transaction["adults"]
        children = transaction["children"]
        night_stay = transaction["night_stay"]

        hotel = next((h for h in hotel_data if h["name"] == hotel_name), None)
        if hotel:
            add_ons = hotel["add_ons"]

            if random.choice([True, False]):
                selected_add_ons = []

                for add_on in add_ons:
                    qty = random.randint(0, adults + children) * night_stay
                    if qty > 0:
                        selected_add_ons.append({
                            "transaction_id": transaction["id"],
                            "hotel_name": hotel_name,
                            "add_on_name": add_on["name"],
                            "quantity": qty,
                            "total_price": add_on["price"] * qty
                        })

                add_on_transactions.extend(selected_add_ons)

    return add_on_transactions

add_on_transactions = generate_add_on_transactions(transaction_data, hotel_data)

with open("add_on_transactions.json", "w") as f:
    json.dump(add_on_transactions, f, indent=4)

print("Add-on transactions generated and saved to add_on_transactions.json")
