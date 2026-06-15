import math, random
from datetime import datetime, timedelta
from create_users import CITIES, UserProfile
from id_generators import generate_transaction_id, generate_burst_id

def high_amount_fraud(transaction: dict, user: UserProfile, rng: random.Random) -> dict:
    '''
    Txn amount made significantly higher than average txn amount based on user archetype.
    '''
    if user.archetype == "predictable spender":
        multiplier = rng.uniform(4, 8)
    elif user.archetype == "average spender":
        multiplier = rng.uniform(6, 12)
    elif user.archetype == "highly volatile spender":
        multiplier = rng.uniform(10, 25)
    transaction["amount"] = round(user.avg_transaction_amount * multiplier, 2)
    
    return transaction


def impossible_travel_fraud(transaction: dict, rng: random.Random, previous_txn: dict) -> dict:
    '''
    Change txn location to city that would require impossible 
    travel speed from city of last transaction city based on gap between times of transactions.
    '''

    if previous_txn is None:  # No previous transactions for this user
        transaction["is_fraud"] = False
        transaction["fraud_type"] = None
        
        return transaction  # No previous transactions to compare against
    
    last_city = previous_txn["city"]

    impossible_cities = []
    for city in CITIES:
        if city["city"] == last_city:
            continue
        
        speed_mph = required_speed_mph(previous_txn, city, datetime.fromisoformat(transaction["timestamp"]))
        
        if speed_mph > 600:  # Threshold for impossible travel
            impossible_cities.append(city)
    
    if not impossible_cities:
        transaction["is_fraud"] = False
        transaction["fraud_type"] = None
        
        return transaction
    
    fraud_city = rng.choice(impossible_cities)

    # Update transaction location to the selected impossible city
    transaction["city"] = fraud_city["city"]
    transaction["lat"] = fraud_city["lat"]
    transaction["lon"] = fraud_city["lon"]
    transaction["is_fraud"] = True
    transaction["fraud_type"] = "impossible travel"
    
    
    return transaction


def haversine_miles(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    '''
    Calculate distance between two cities using Haversine formula
    '''
      
    earth_radius_miles = 3958.8
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = (math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2)
    c = 2 * math.asin(math.sqrt(a))

    return earth_radius_miles * c

def required_speed_mph(previous_txn: dict, city: dict, current_time: datetime) -> float:
    '''
    Calculate required travel speed in mph between last transaction city 
    and current transaction city based on time gap between transactions.
    '''

    previous_time = datetime.fromisoformat(previous_txn["timestamp"])

    hours_elapsed = (current_time - previous_time).total_seconds() / 3600

    if hours_elapsed <= 0:
        return float("inf")

    distance = haversine_miles(
        previous_txn["lat"],
        previous_txn["lon"],
        city["lat"],
        city["lon"],
    )

    return distance / hours_elapsed

def rapid_burst_fraud(transaction: dict, user: UserProfile, rng: random.Random) -> dict:
    '''
    Simulate rapid burst fraud by creating multiple transactions in a short time frame.
    '''
    burst_transactions = []
    burst_id = generate_burst_id()
    
    # Determine burst size based on user transaction frequency
    if user.transactions_per_day <= 5:
        burst_size = rng.randint(3, 5)
    elif user.transactions_per_day <= 15:
        burst_size = rng.randint(4, 7)
    else:
        burst_size = rng.randint(6, 10)
    
    current_time = datetime.fromisoformat(transaction["timestamp"])
    for i in range(burst_size):  
        burst_txn = transaction.copy()
        burst_txn["transaction_id"] = generate_transaction_id()
        burst_txn["timestamp"] = (current_time).isoformat()
        burst_txn["amount"] = round(rng.lognormvariate(math.log(user.avg_transaction_amount), user.spend_sigma), 2)
        burst_txn["is_fraud"] = True
        burst_txn["fraud_type"] = "rapid burst"
        burst_txn["burst_id"] = burst_id
        burst_txn["burst_index"] = i+1
        burst_transactions.append(burst_txn)
        current_time += timedelta(seconds=rng.randint(0, 60))
    return burst_transactions

def create_fraud(transaction: dict, user: UserProfile, fraud_type: str, rng: random.Random, previous_txn: dict) -> dict:
    '''
    Alters txn attributes based on the specified fraud type.
    '''
    
    transaction["is_fraud"] = True
    transaction["fraud_type"] = fraud_type

    if fraud_type == "high amount":
        transaction = high_amount_fraud(transaction, user, rng)
    elif fraud_type == "new device":
        transaction["device_id"] = f"unknown_device_{user.user_id}_{rng.randint(1000, 9999)}"
    elif fraud_type == "impossible travel":
        transaction = impossible_travel_fraud(transaction, rng, previous_txn)
    elif fraud_type == "rapid burst":
        pass

    return transaction

