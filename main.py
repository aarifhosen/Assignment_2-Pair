# =========================================================
# File: main.py
# Description: User Interface and Event Loop
# =========================================================

import functions

def main_app():
    customer_cart = []
    
    functions.show_header("WELCOME TO THE GRAND BISTRO MANAGEMENT SYSTEM")
    print("Please select your order fulfillment mode:")
    print("1. Dine-In / Takeaway")
    print("2. Doorstep Home Delivery (+$5.00 Flat Fee)")
    
    order_mode = "Dine-In/Takeaway"
    while True:
        mode_choice = input("\nSelect Mode (1 or 2): ").strip()
        if mode_choice == "1":
            order_mode = "Dine-In/Takeaway"
            break
        elif mode_choice == "2":
            order_mode = "Delivery"
            break
        else:
            print("❌ Invalid selection! Please enter 1 or 2.")

    # Main Application Loop
    while True:
        print("\n" + " SYSTEM MAIN MENU ".center(40, "*"))
        print("1. Browse Food & Beverage Menu")
        print("2. Add Item to Order Cart")
        print("3. View Shopping Cart")
        print("4. Remove Item from Cart")
        print("5. Proceed to Payment & Checkout")
        print("6. Exit System")
        print("*" * 40)

        user_choice = input("Enter your choice (1-6): ").strip()

        if user_choice == "1":
            functions.display_restaurant_menu()
        elif user_choice == "2":
            functions.add_item_to_cart(customer_cart)
        elif user_choice == "3":
            functions.view_current_cart(customer_cart)
        elif user_choice == "4":
            functions.remove_item_from_cart(customer_cart)
        elif user_choice == "5":
            if functions.process_checkout_and_billing(customer_cart, order_mode):
                print("\n🎉 Transaction Completed! Thank you.")
                break
        elif user_choice == "6":
            print("\nThank you for visiting The Grand Bistro. System closing...")
            break
        else:
            print("❌ Invalid option choice! Please pick a number from 1 to 6.")

if __name__ == "__main__":
    main_app()