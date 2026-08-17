# =========================================================
# File: functions.py
# Description: Helper functions and logic for Restaurant System
# =========================================================

import datetime

# Master Data Store for Restaurant Menu
MENU_DATA = {
    101: {"name": "Gourmet Beef Burger", "category": "Mains", "price": 14.50, "stock": 15},
    102: {"name": "Crispy Chicken Wrap", "category": "Mains", "price": 10.00, "stock": 20},
    103: {"name": "Creamy Carbonara Pasta", "category": "Mains", "price": 16.80, "stock": 10},
    104: {"name": "Pepperoni Feast Pizza", "category": "Mains", "price": 24.00, "stock": 6},
    201: {"name": "French Fries (Large)", "category": "Sides", "price": 5.50, "stock": 25},
    202: {"name": "Garlic Cheese Bread", "category": "Sides", "price": 6.50, "stock": 12},
    301: {"name": "Iced Peach Tea", "category": "Drinks", "price": 4.50, "stock": 30},
    302: {"name": "Fresh Mango Smoothie", "category": "Drinks", "price": 7.00, "stock": 15},
    401: {"name": "Chocolate Lava Cake", "category": "Desserts", "price": 8.50, "stock": 10}
}

# Discount Vouchers Structure
VOUCHERS = {
    "WELCOME10": 0.10,
    "FOODIE15": 0.15,
    "SUPER20": 0.20
}

def show_header(title):
    """Prints a styled UI header."""
    print("\n" + "=" * 60)
    print(f"{title.center(60)}")
    print("=" * 60)

def display_restaurant_menu():
    """Displays menu categorized cleanly with formatted prices and stock."""
    show_header("THE GRAND BISTRO - MENU")
    print(f"{'ID':<6} | {'Item Name':<25} | {'Category':<10} | {'Price ($)':<9} | {'Stock':<5}")
    print("-" * 60)
    
    for item_id, info in MENU_DATA.items():
        stock_status = str(info["stock"]) if info["stock"] > 0 else "OUT"
        print(f"{item_id:<6} | {info['name']:<25} | {info['category']:<10} | ${info['price']:<8.2f} | {stock_status:<5}")
    print("=" * 60)

def add_item_to_cart(cart_list):
    """Validates inputs and handles adding/updating items in customer's cart."""
    display_restaurant_menu()
    try:
        item_id = int(input("\nEnter Product ID to add to cart: "))
        if item_id not in MENU_DATA:
            print("❌ Invalid Product ID! Please select from the menu.")
            return

        selected_item = MENU_DATA[item_id]
        if selected_item["stock"] <= 0:
            print(f"❌ Sorry! '{selected_item['name']}' is currently out of stock.")
            return

        qty = int(input(f"Enter quantity for '{selected_item['name']}': "))
        if qty <= 0:
            print("❌ Quantity must be at least 1.")
            return

        if qty > selected_item["stock"]:
            print(f"❌ Insufficient stock! Only {selected_item['stock']} items available.")
            return

        # Deduct Stock
        selected_item["stock"] -= qty

        # Check if already in cart
        for cart_item in cart_list:
            if cart_item["id"] == item_id:
                cart_item["qty"] += qty
                print(f"✅ Updated quantity for '{selected_item['name']}' in cart.")
                return

        cart_list.append({
            "id": item_id,
            "name": selected_item["name"],
            "price": selected_item["price"],
            "qty": qty
        })
        print(f"✅ Added {qty}x '{selected_item['name']}' to cart successfully!")

    except ValueError:
        print("❌ Invalid input! Please enter numeric values only.")

def remove_item_from_cart(cart_list):
    """Allows customer to remove items and restore inventory stock."""
    if not cart_list:
        print("\n🛒 Cart is empty! Nothing to remove.")
        return

    show_header("REMOVE ITEM FROM CART")
    for idx, item in enumerate(cart_list, start=1):
        print(f"{idx}. {item['name']} (x{item['qty']})")
    
    try:
        choice = int(input("\nEnter the number of the item to remove: "))
        if 1 <= choice <= len(cart_list):
            removed = cart_list.pop(choice - 1)
            # Restore Stock
            MENU_DATA[removed["id"]]["stock"] += removed["qty"]
            print(f"✅ Removed '{removed['name']}' from cart and restored stock.")
        else:
            print("❌ Invalid item selection number.")
    except ValueError:
        print("❌ Please enter a valid number.")

def view_current_cart(cart_list):
    """Prints the current cart items with itemized cost."""
    show_header("YOUR SHOPPING CART")
    if not cart_list:
        print("Your cart is currently empty.")
        print("=" * 60)
        return False

    subtotal = 0
    print(f"{'Item Name':<28} | {'Price':<8} | {'Qty':<4} | {'Total ($)':<10}")
    print("-" * 60)
    for item in cart_list:
        item_total = item["price"] * item["qty"]
        subtotal += item_total
        print(f"{item['name']:<28} | ${item['price']:<7.2f} | {item['qty']:<4} | ${item_total:<10.2f}")
    
    print("-" * 60)
    print(f"{'Current Subtotal:':<44} ${subtotal:.2f}")
    print("=" * 60)
    return True

def process_checkout_and_billing(cart_list, order_type):
    """Calculates final tax, discount, payment and exports text invoice."""
    if not view_current_cart(cart_list):
        print("❌ Cannot proceed to checkout with an empty cart.")
        return False

    subtotal = sum(item["price"] * item["qty"] for item in cart_list)
    
    # Voucher Validation
    voucher_code = input("\nEnter Voucher Code (Press ENTER to skip): ").strip().upper()
    discount_rate = VOUCHERS.get(voucher_code, 0.0)
    
    if voucher_code and discount_rate > 0:
        print(f"✅ Promo Applied! You got a {int(discount_rate * 100)}% discount.")
    elif voucher_code:
        print("⚠️ Invalid voucher code. Proceeding without discount.")

    discount_amount = subtotal * discount_rate
    tax_amount = (subtotal - discount_amount) * 0.06  # 6% Service Tax
    delivery_charge = 5.00 if order_type == "Delivery" else 0.0
    final_amount = (subtotal - discount_amount) + tax_amount + delivery_charge

    show_header("PAYMENT & RECEIPT SUMMARY")
    print(f"Order Type      : {order_type}")
    print(f"Subtotal        : ${subtotal:.2f}")
    print(f"Discount        : -${discount_amount:.2f}")
    print(f"Service Tax (6%): ${tax_amount:.2f}")
    print(f"Delivery Fee    : ${delivery_charge:.2f}")
    print("-" * 60)
    print(f"TOTAL PAYABLE   : ${final_amount:.2f}")
    print("=" * 60)

    # Payment Simulation
    while True:
        try:
            cash_given = float(input(f"\nEnter Cash/Payment Amount (${final_amount:.2f} required): $"))
            if cash_given >= final_amount:
                change = cash_given - final_amount
                print(f"✅ Payment successful! Your change: ${change:.2f}")
                break
            else:
                print(f"❌ Insufficient payment! You still owe ${final_amount - cash_given:.2f}")
        except ValueError:
            print("❌ Please enter a valid payment amount.")

    # Save Digital Receipt File
    receipt_filename = f"Receipt_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(receipt_filename, "w") as file:
        file.write("=" * 45 + "\n")
        file.write("           THE GRAND BISTRO RECEIPT\n")
        file.write("=" * 45 + "\n")
        file.write(f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        file.write(f"Order Type: {order_type}\n")
        file.write("-" * 45 + "\n")
        for item in cart_list:
            file.write(f"{item['name']:<25} x{item['qty']:<3} ${item['price']*item['qty']:.2f}\n")
        file.write("-" * 45 + "\n")
        file.write(f"Subtotal        : ${subtotal:.2f}\n")
        file.write(f"Discount        : -${discount_amount:.2f}\n")
        file.write(f"Tax (6%)        : ${tax_amount:.2f}\n")
        file.write(f"Delivery Fee    : ${delivery_charge:.2f}\n")
        file.write(f"TOTAL PAID      : ${final_amount:.2f}\n")
        file.write(f"Change Given    : ${change:.2f}\n")
        file.write("=" * 45 + "\n")
        file.write("      Thank you for your order!\n")

    print(f"\n📄 Digital receipt generated and saved as '{receipt_filename}'")
    return True