import math, random
from datetime import datetime
from create_users import CITIES, UserProfile

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


def impossible_travel_fraud(transaction: dict, rng: random.Random, last_user_transactions: list[dict]) -> dict:
    '''
    Change txn location to city that would require impossible 
    travel speed from city of last transaction city based on gap between times of transactions.
    '''

    if not last_user_transactions:  # No previous transactions for this user
        transaction["is_fraud"] = False
        transaction["fraud_type"] = None
        
        return transaction  # No previous transactions to compare against
    
    last_transaction = last_user_transactions[-1]
    last_city = last_transaction["city"]

    impossible_cities = []
    for city in CITIES:
        if city["city"] == last_city:
            continue
        
        speed_mph = required_speed_mph(last_transaction, city, datetime.fromisoformat(transaction["timestamp"]))
        
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

def required_speed_mph(last_transaction: dict, city: dict, current_time: datetime) -> float:
    '''
    Calculate required travel speed in mph between last transaction city 
    and current transaction city based on time gap between transactions.
    '''

    previous_time = datetime.fromisoformat(last_transaction["timestamp"])

    hours_elapsed = (current_time - previous_time).total_seconds() / 3600

    if hours_elapsed <= 0:
        return float("inf")

    distance = haversine_miles(
        last_transaction["lat"],
        last_transaction["lon"],
        city["lat"],
        city["lon"],
    )

    return distance / hours_elapsed

def create_fraud(transaction: dict, user: UserProfile, fraud_type: str, rng: random.Random, last_user_transactions: list[dict]) -> dict:
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
        transaction = impossible_travel_fraud(transaction, rng, last_user_transactions)
    elif fraud_type == "rapid burst":
        pass

    return transaction

