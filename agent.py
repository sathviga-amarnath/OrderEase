# OrderEase - AI Personal Concierge Agent


import google.generativeai as genai
from tools import (
    search_restaurants,
    get_restaurant_menu,
    place_order,
    track_order,
    search_products
)
from memory import memory

# Configure Gemini API
GEMINI_API_KEY = "your-gemini-api-key-here"
genai.configure(api_key=GEMINI_API_KEY)


SYSTEM_PROMPT = """
You are OrderEase, a friendly and intelligent personal concierge agent 
for food ordering and shopping in Chennai, India.

Your capabilities:
1. Search for restaurants based on cuisine, area, and preferences
2. Show restaurant menus and popular items
3. Place food orders and generate order confirmation
4. Track existing orders
5. Search for products across categories
6. Remember user preferences and give personalized recommendations

Personality:
- Friendly and helpful
- Use casual but professional tone
- Add relevant emojis to make responses fun
- Always confirm before placing orders
- Remember what users like and suggest accordingly

When user asks for food:
1. Ask for cuisine preference if not specified
2. Search and show top 3 restaurants
3. Ask which restaurant they prefer
4. Show menu
5. Confirm order details
6. Place order and share confirmation

When user asks for products:
1. Ask for category or specific item
2. Search and show top options
3. Compare prices
4. Help user decide

Always greet users by name if you know them!
"""

class OrderEaseAgent:
    def __init__(self):
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=SYSTEM_PROMPT
        )
        self.chat = self.model.start_chat(history=[])
        self.current_user = "user_1"
        self.current_order = None
    
    def process_message(self, user_message):
        """Process user message and return response"""
        
       
        user = memory.get_user(self.current_user)
        
     
        context = f"""
User message: {user_message}
User preferences: {memory.get_recommendations(self.current_user)}
"""
        
        message_lower = user_message.lower()
        

        if any(word in message_lower for word in 
               ["food", "eat", "hungry", "restaurant", 
                "biryani", "dosa", "pizza", "order food"]):
            
            
            cuisine = None
            cuisines = ["biryani", "dosa", "pizza", "south indian", 
                       "north indian", "chinese", "chettinad"]
            for c in cuisines:
                if c in message_lower:
                    cuisine = c
                    break
            
            restaurants = search_restaurants(cuisine=cuisine)
            
            restaurant_info = "\n".join([
                f"{i+1}. {r['name']} - {r['area']} "
                f"| Rating: {r['rating']}⭐ "
                f"| {r['price_range']} "
                f"| Delivery: {r['delivery_time']}"
                for i, r in enumerate(restaurants[:3])
            ])
            
            context += f"\nAvailable restaurants:\n{restaurant_info}"
        
    
        elif "track" in message_lower and "OE-" in user_message:
            order_id = [word for word in user_message.split() 
                       if word.startswith("OE-")]
            if order_id:
                tracking = track_order(order_id[0])
                context += f"\nOrder tracking info: {tracking}"
        
   
        elif any(word in message_lower for word in 
                ["buy", "shop", "product", "earphone", 
                 "phone", "clothes", "grocery"]):
            products = search_products(query=user_message)
            product_info = "\n".join([
                f"{i+1}. {p['name']} - {p['price']} "
                f"| Rating: {p['rating']}⭐ "
                f"| {p['platform']}"
                for i, p in enumerate(products)
            ])
            context += f"\nAvailable products:\n{product_info}"
        

        response = self.chat.send_message(context)
        

        if cuisine:
            memory.update_preference(
                self.current_user, 
                "favourite_cuisines", 
                cuisine
            )
        
        return response.text
    
    def run(self):
        """Run the OrderEase agent"""
        print("=" * 50)
        print("🍽️  Welcome to OrderEase!")
        print("Your Personal AI Concierge for Chennai")
        print("=" * 50)
        print("Type 'quit' to exit\n")
   
        name = input("What's your name? ")
        memory.update_preference(self.current_user, "name", name)
        print(f"\nHello {name}! 👋 How can I help you today?")
        print("I can help you order food, shop online, or track your orders!\n")
        
        while True:
            user_input = input("You: ").strip()
            
            if user_input.lower() == "quit":
                print("\nThank you for using OrderEase! 🙏 Goodbye!")
                break
            
            if not user_input:
                continue
            
            print("\nOrderEase: ", end="")
            response = self.process_message(user_input)
            print(response)
            print()


if __name__ == "__main__":
    agent = OrderEaseAgent()
    agent.run()
