import random


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

user_archetype = ['predictable spender', 'average spender', 'highly volatile spender']

class UserProfile:
    '''
    Class representing a user profile with attributes that 
    define their spending behavior and transaction patterns
    '''

    def __init__(self, user_id, rng):
        self.user_id = user_id
        self.archetype = rng.choices(user_archetype, weights = [0.3, 0.5, 0.2], k = 1)[0] #assign archetype with weighted probabilities
        
        #spend_sigma set based on archetype to control variability in transaction amounts
        match self.archetype:
            case 'predictable spender':
                self.spend_sigma = 0.1 #low spend_sigma means transaction amounts will be close to avg_transaction_amount
            case 'average spender':
                self.spend_sigma = 0.5
            case 'highly volatile spender':
                self.spend_sigma = 1.5 #high spend_sigma means transaction amounts will vary widely around avg_transaction_amount
        
        self.city = rng.choices(CITIES, weights = weights, k = 1)[0] #choose cities proportional to their weights
        self.card_id = f"card_{user_id}_001" 
        self.avg_daily_spend = rng.uniform(10, 2000)  
        device_count = rng.choice([1, 2])  # Randomly assign 1 or 2 devices per user
        self.device_id = [f"device_{user_id}_{j+1:02d}" for j in range(device_count)]
        self.transactions_per_day = int(rng.uniform(1, 20))
        self.avg_transaction_amount = self.avg_daily_spend / self.transactions_per_day

    def __repr__(self):
        return f"user_id: {self.user_id}, archetype: {self.archetype}, city: {self.city['city']}, card_id: {self.card_id}, avg_daily_spend: {self.avg_daily_spend:.2f}, device_id: {self.device_id}, transactions_per_day: {self.transactions_per_day}, avg_transaction_amount: {self.avg_transaction_amount:.2f}"

def create_user_profiles(num_users: int, rng: random.Random) -> list[UserProfile]:
    ''' 
    Creates and returns list of user profiles. 
    Each user profile is an instance of the UserProfile class, 
    which includes attributes that define user spending behavior
    '''
    users = []
    for i in range(num_users):
        user_id = f"user_{i+1}"
        users.append(UserProfile(user_id, rng))
    return(users)

if __name__ == "__main__":
    users = create_user_profiles(10, random.Random(42))
    for user in users:
        print(user)