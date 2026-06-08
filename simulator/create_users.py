import random, uuid

CITIES = [
    {"city": "New York",     "lat": 40.71, "lon": -74.01, "weight": 20},
    {"city": "Los Angeles",  "lat": 34.05, "lon": -118.24, "weight": 15},
    {"city": "Chicago",      "lat": 41.88, "lon": -87.63,  "weight": 12},
    {"city": "Houston",      "lat": 29.76, "lon": -95.37,  "weight": 10},
    {"city": "Phoenix",      "lat": 33.45, "lon": -112.07, "weight": 8},
    {"city": "Philadelphia", "lat": 39.95, "lon": -75.17,  "weight": 7},
    {"city": "San Antonio",  "lat": 29.42, "lon": -98.49,  "weight": 6},
    {"city": "San Diego",    "lat": 32.72, "lon": -117.16, "weight": 6},
    {"city": "Dallas",       "lat": 32.78, "lon": -96.80,  "weight": 8},
    {"city": "Miami",        "lat": 25.76, "lon": -80.19,  "weight": 7},
    {"city": "Seattle",      "lat": 47.61, "lon": -122.33, "weight": 6},
    {"city": "Denver",       "lat": 39.74, "lon": -104.98, "weight": 5},
    {"city": "Tokyo",       "lat": 35.68, "lon": 139.65, "weight": 25},
    {"city": "Kingston",       "lat": 17.97, "lon": -76.79, "weight": 7},
    {"city": "Brisbane",       "lat": -27.47, "lon": 153.03, "weight": 13},
]

weights = [c["weight"] for c in CITIES]



class UserProfile:
    def __init__(self, user_id):
        self.user_id = user_id
        self.city = random.choices(CITIES, weights=weights, k=1)[0] #choose cities proportional to their weights
        self.card_id = str(uuid.uuid4()) 
        self.avg_daily_spend = random.uniform(10, 2000)  
        device_count = random.choice([1, 2])  # Randomly assign 1 or 2 devices per user
        self.device_id = [str(uuid.uuid4()) for _ in range(device_count)]
        self.transactions_per_day = int(random.uniform(1, 20))
        self.avg_transaction_amount = random.uniform(0, 1500)

    def __repr__(self):
        return f"User ID: {self.user_id}\n\n City: {self.city['city']}\n Card ID: {self.card_id}\n Average Daily Spend: {self.avg_daily_spend:.2f}\n Device ID: {self.device_id}\n Transactions/day: {self.transactions_per_day}\n Average Transaction Amount: {self.avg_transaction_amount:.2f}\n\n"

num_users = 10
def create_user_profiles(num_users):
    users = []
    for i in range(num_users):
        user_id = f"user_{i+1}"
        users.append(UserProfile(user_id))
    print(users)

create_user_profiles(num_users)
