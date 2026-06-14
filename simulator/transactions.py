import random 
import time 
import uuid 
import math 
import csv
import pandas as pd

from datetime import datetime, timedelta
from create_users import create_user_profiles, UserProfile
from fraud import create_fraud


rng = random.Random(42)  # Set fixed seed for reproducibility
user_list = create_user_profiles(10, rng) 
fraud_probability = 0.20 
fraud_types = ['impossible travel', 'rapid burst', 'high amount', 'new device'] 

def generate_transaction(user: UserProfile , timestamp: datetime, rng: random.Random, txn_number: int) -> dict:
    '''
    Generates a single transaction for a given user at a specific timestamp.
    '''
    
    #Lognormal distribution used to simulate txn amounts based on average txn amount and spend_sigma.
    amount_mu = math.log(user.avg_transaction_amount)
    simulated_amount = rng.lognormvariate(amount_mu, user.spend_sigma)
    
    return {
        'transaction_id': f"txn_{txn_number:08d}",
        'user_id': user.user_id,        
        'amount': round(simulated_amount, 2),  
        'timestamp': timestamp.isoformat(),
        'city': user.city['city'],
        'lat': user.city['lat'],
        'lon': user.city['lon'],
        'device_id': rng.choice(user.device_id),
        'card_id': user.card_id,
        'is_fraud': False,
        'fraud_type': None
    }

def generate_transactions(user_list: list[UserProfile], rng: random.Random) -> list[dict]:
    '''
    Generates a list of simulated user transactions over a selected time window.
    Creates random fraud events based on the fraud_probability, 
    transaction attributes altered to reflect fraud type .
    '''
    start_time = datetime(2026, 6, 1, 12, 0, 0) #Simulation start time
    end_time = start_time + timedelta(hours=5) #Simulation end time 
    transactions = []
    current_time = start_time
    
    while current_time < end_time:
        user_weights = [user.transactions_per_day for user in user_list] #Weight users based on avg txns/day
        user = rng.choices(user_list, weights=user_weights, k=1)[0] 
        
        last_user_transactions = [t for t in transactions if t['user_id'] == user.user_id] 
        txn_number = len(transactions)+1
        
        transaction = generate_transaction(user, current_time, rng, txn_number) 

        if rng.random() < fraud_probability: 
            fraud_type = rng.choice(["high amount", "new device", "impossible travel"]) 
            transaction = create_fraud(transaction, user, fraud_type, rng, last_user_transactions) #Alter txn attributes based on fraud type 

        transactions.append(transaction)
        gap_seconds = rng.randint(30, 300)
        current_time = current_time + timedelta(seconds=gap_seconds)

    return transactions

if __name__ == "__main__": 
    txns = generate_transactions(user_list, rng)
    for txn in txns:
        print(txn)
    
    # Export transactions to CSV 
    df = pd.DataFrame(txns)
    df.to_csv("results.csv", index=False)
    print("\nSuccessfully exported simulation results to results.csv")











