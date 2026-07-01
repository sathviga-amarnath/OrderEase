# OrderEase Tools - Search and Order Functions

import random
import string
from datetime import datetime
from data.restaurants import RESTAURANTS, PRODUCT_CATEGORIES

def search_restaurants(cuisine=None, area=None, max_price=None):
    """Search for restaurants based on filters"""
    results = []
    
    for restaurant in RESTAURANTS:
        # Filter by cuisine
        if cuisine:
            cuisine_match = any(
                cuisine.lower() in c.lower() 
                for c in restaurant["cuisine"]
            )
            if not cuisine_match:
                continue
        
        # Filter by area
        if area:
            if area.lower() not in restaurant["area"].lower():
                continue
        
        if restaurant["open"]:
            results.append(restaurant)
    
    return results if results else RESTAURANTS[:3]

def get_restaurant_menu(restaurant_id):
    """Get menu for a specific restaurant"""
    for r in RESTAURANTS:
        if r["id"] == restaurant_id:
            return {
                "restaurant": r["name"],
                "popular_items": r["popular_items"],
                "price_range": r["price_range"]
            }
    return None

def generate_order_id():
    """Generate unique order ID"""
    letters = string.ascii_uppercase
    random_str = ''.join(random.choices(letters, k=4))
    random_num = random.randint(1000, 9999)
    return f"OE-{random_str}-{random_num}"

def place_order(user_name, restaurant_name, items, address):
    """Simulate placing an order"""
    order_id = generate_order_id()
    order_time = datetime.now().strftime("%I:%M %p")
    
    return {
        "success": True,
        "order_id": order_id,
        "user": user_name,
        "restaurant": restaurant_name,
        "items": items,
        "address": address,
        "order_time": order_time,
        "estimated_delivery": "30-45 minutes",
        "status": "Confirmed ✅",
        "payment": "Cash on Delivery"
    }

def track_order(order_id):
    """Simulate order tracking"""
    statuses = [
        "Order Confirmed ✅",
        "Restaurant is preparing your food 👨‍🍳",
        "Order picked up by delivery partner 🛵",
        "Out for delivery 📍",
        "Delivered! Enjoy your meal 🎉"
    ]
    # Randomly return a status for demo
    return {
        "order_id": order_id,
        "status": random.choice(statuses),
        "estimated_time": "20-30 minutes"
    }

def search_products(category=None, max_price=None, query=None):
    """Simulate product search"""
    # Sample products for demo
    products = [
        {
            "name": "boAt Rockerz 450 Bluetooth Headphones",
            "category": "Electronics",
            "price": "₹899",
            "rating": 4.1,
            "platform": "Amazon"
        },
        {
            "name": "Noise ColorFit Pro 4 Smartwatch",
            "category": "Electronics", 
            "price": "₹1,999",
            "rating": 4.3,
            "platform": "Flipkart"
        },
        {
            "name": "Cotton Casual T-Shirt",
            "category": "Fashion",
            "price": "₹399",
            "rating": 4.0,
            "platform": "Myntra"
        },
        {
            "name": "Tata Salt 1kg",
            "category": "Groceries",
            "price": "₹24",
            "rating": 4.5,
            "platform": "BigBasket"
        }
    ]
    
    if query:
        results = [p for p in products 
                  if query.lower() in p["name"].lower()]
        return results if results else products[:2]
    
    if category:
        results = [p for p in products 
                  if category.lower() in p["category"].lower()]
        return results if results else products[:2]
    
    return products[:3]
