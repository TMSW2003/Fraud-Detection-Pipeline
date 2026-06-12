import random, time, uuid, math
from datetime import datetime, timedelta
from create_users import create_user_profiles


rng = random.Random(42)  # Set a fixed seed for reproducibility
user_list = create_user_profiles(10, rng) 
def generate_transaction(user, timestamp, rng, txn_number):
    return {
        'transaction_id': f"txn_{txn_number:08d}",
        'user_id': user.user_id,
        'amount': round(rng.lognormvariate(math.log(user.avg_transaction_amount), user.spend_sigma), 2),  
        'timestamp': timestamp.isoformat(),
        'city': user.city['city'],
        'lat': user.city['lat'],
        'lon': user.city['lon'],
        'device_id': rng.choice(user.device_id),
        'card_id': user.card_id,
        'is_fraud': False,
        'fraud_type': None
    }
def generate_transactions(user_list, rng):
    start_time = datetime(2026, 6, 1, 12, 0, 0)
    end_time = start_time + timedelta(hours=2)
    transactions = []

    current_time = start_time
    while current_time < end_time:
        user_weights = [user.transactions_per_day for user in user_list]
        user = rng.choices(user_list, weights=user_weights, k=1)[0]
        txn_number = len(transactions)+1
        transaction = generate_transaction(user, current_time, rng, txn_number)
        transactions.append(transaction)

        gap_seconds = rng.randint(30, 300)
        current_time = current_time + timedelta(seconds=gap_seconds)

    return transactions

if __name__ == "__main__": 
    txns = generate_transactions(user_list, rng)
    for txn in txns:
        print(txn)












