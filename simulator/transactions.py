import random 
import math 
import pandas as pd

from datetime import datetime, timedelta
from create_users import create_user_profiles, UserProfile
from fraud import create_fraud, rapid_burst_fraud
from id_generators import generate_transaction_id

rng = random.Random(42)  # Set fixed seed for reproducibility
user_list = create_user_profiles(100, rng) 
fraud_probability = 0.02 
fraud_types = ['impossible travel', 'rapid burst', 'high amount', 'new device'] 

def generate_transaction(user: UserProfile , current_time: datetime, rng: random.Random) -> dict:
    '''Generates a single transaction for a given user at a specific timestamp.'''
    
    #Lognormal distribution used to simulate txn amounts based on average txn amount and spend_sigma.
    amount_mu = math.log(user.avg_transaction_amount)
    simulated_amount = rng.lognormvariate(amount_mu, user.spend_sigma)
    
    return {
        'transaction_id': generate_transaction_id(),
        'user_id': user.user_id,        
        'amount': round(simulated_amount, 2),  
        'timestamp': current_time.isoformat(timespec="microseconds"),
        'city': user.city['city'],
        'lat': user.city['lat'],
        'lon': user.city['lon'],
        'device_id': rng.choice(user.device_id),
        'card_id': user.card_id,
        'is_fraud': False,
        'fraud_type': None,
        'burst_id': None,
        'burst_index': None
    }

def generate_transactions(user_list: list[UserProfile], rng: random.Random) -> list[dict]:
    '''
    Generates a list of simulated user transactions over a selected time window.
    Creates random fraud events based on the fraud_probability, 
    transaction attributes altered to reflect fraud type .
    '''
    start_time = datetime(2026, 6, 1, 12, 0, 0) #Simulation start time
    end_time = start_time + timedelta(hours=24) #Simulation end time 
    
    transactions = []
    last_txn_by_user = {user.user_id: None for user in user_list} 
    current_time = start_time
    total_daily_txns = sum(user.transactions_per_day for user in user_list)
    avg_gap_seconds  = 86400 / total_daily_txns
    
    while current_time < end_time:
        
        user_weights = [user.transactions_per_day for user in user_list] #Weight users based on avg txns/day
        user = rng.choices(user_list, weights=user_weights, k=1)[0] 
        
        previous_txn = last_txn_by_user.get(user.user_id)
        transaction = generate_transaction(user, current_time, rng) 

        if rng.random() < fraud_probability: 
            fraud_type = rng.choice(fraud_types) 
            
            if fraud_type == "rapid burst":
                burst = rapid_burst_fraud(transaction, user, rng) 
                last_txn_by_user[user.user_id] = burst[-1]
                transactions.extend(burst)
                last_burst_time = transactions[-1]["timestamp"] 
                current_time = datetime.fromisoformat(last_burst_time) + timedelta(seconds = rng.expovariate(1/avg_gap_seconds))

                continue
            else:
                transaction = create_fraud(transaction, user, fraud_type, rng, previous_txn) #Alter txn attributes based on fraud type 

        transactions.append(transaction)
        last_txn_by_user[user.user_id] = transaction
        gap_seconds = rng.expovariate(1/avg_gap_seconds)
        current_time += timedelta(seconds=gap_seconds)

    return transactions

if __name__ == "__main__": 
    txns = generate_transactions(user_list, rng)
    for txn in txns:
        print(txn)
    
    # Export transactions to CSV 
    df = pd.DataFrame(txns)
    df.to_csv("results.csv", index=False)
    print("\nSuccessfully exported simulation results to results.csv")

    profile = pd.DataFrame([user.to_dict() for user in user_list])
    profile.to_csv("user_profiles.csv", index=False)
    print("\nSuccessfully exported user profiles to user_profiles.csv")











