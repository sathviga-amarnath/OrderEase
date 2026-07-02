# User Memory & Preferences for OrderEase

class UserMemory:
    def __init__(self):
        self.users = {}
    
    def get_user(self, user_id):
        if user_id not in self.users:
            self.users[user_id] = {
                "name": "",
                "favourite_cuisines": [],
                "favourite_restaurants": [],
                "order_history": [],
                "preferred_price_range": "",
                "location": "",
                "dietary_preference": ""  # veg, non-veg, vegan
            }
        return self.users[user_id]
    
    def update_preference(self, user_id, key, value):
        user = self.get_user(user_id)
        if key in ["favourite_cuisines", "favourite_restaurants", "order_history"]:
            if value not in user[key]:
                user[key].append(value)
        else:
            user[key] = value
        return user
    
    def add_order(self, user_id, order):
        user = self.get_user(user_id)
        user["order_history"].append(order)
        return user
    
    def get_recommendations(self, user_id):
        user = self.get_user(user_id)
        return {
            "favourite_cuisines": user["favourite_cuisines"],
            "favourite_restaurants": user["favourite_restaurants"],
            "dietary_preference": user["dietary_preference"]
        }

# Global memory instance
memory = UserMemory()
