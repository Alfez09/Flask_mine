from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

class CoffeeRestaurant:
    def __init__(self):
        self.menu = {
            'Coffee': {
                'Espresso': 60,
                'Americano': 70,
                'Cappuccino': 90,
                'Latte': 100,
                'Mocha': 110
            },
            'Tea': {
                'Green Tea': 40,
                'Black Tea': 35,
                'Herbal Tea': 50,
                'Masala Chai': 30
            },
            'Snacks': {
                'Sandwich': 80,
                'Muffin': 50,
                'Croissant': 70,
                'Cookie': 30
            }
        }
        self.current_order = {}
        self.greeting_displayed = False

    def greet_customer(self):
        self.greeting_displayed = True
        return "Welcome to Hamster Coffee Shop!"

    def show_menu(self):
        return self.menu

    def add_to_order(self, category, item, quantity=1):
        if category in self.menu and item in self.menu[category]:
            if item in self.current_order:
                self.current_order[item]['quantity'] += quantity
            else:
                self.current_order[item] = {
                    'category': category,
                    'price': self.menu[category][item],
                    'quantity': quantity
                }
            return f"Added {quantity} {item} to your order."
        return "Item not found in menu."

    def remove_from_order(self, item):
        if item in self.current_order:
            del self.current_order[item]
            return f"Removed {item} from your order."
        return "Item not found in your current order."

    def update_order_item(self, item, new_quantity):
        if item in self.current_order:
            if new_quantity > 0:
                self.current_order[item]['quantity'] = new_quantity
                return f"Updated {item} quantity to {new_quantity}."
            else:
                return self.remove_from_order(item)
        return "Item not found in your current order."

    def get_current_order(self):
        return self.current_order

    def calculate_total(self):
        total = 0
        for item, details in self.current_order.items():
            total += details['price'] * details['quantity']
        return total

    def confirm_order(self):
        if not self.current_order:
            return "Your order is empty. Please add some items."
        
        order_summary = {
            'items': self.current_order,
            'total': self.calculate_total(),
            'message': "Order placed successfully! Thank you for visiting Brew Haven."
        }
        self.current_order = {}  # Clear the order after confirmation
        return order_summary

# Create an instance of the coffee restaurant
coffee_shop = CoffeeRestaurant()

@app.route('/')
def home():
    greeting = coffee_shop.greet_customer() if not coffee_shop.greeting_displayed else None
    menu = coffee_shop.show_menu()
    return render_template('index.html', greeting=greeting, menu=menu, order=None)

@app.route('/add_to_order', methods=['POST'])
def add_to_order():
    category = request.form.get('category')
    item = request.form.get('item')
    quantity = int(request.form.get('quantity', 1))
    coffee_shop.add_to_order(category, item, quantity)
    return redirect(url_for('show_order'))

@app.route('/order')
def show_order():
    menu = coffee_shop.show_menu()
    order = coffee_shop.get_current_order()
    total = coffee_shop.calculate_total()
    return render_template('index.html', menu=menu, order=order, total=total)

@app.route('/update_item', methods=['POST'])
def update_item():
    item = request.form.get('item')
    action = request.form.get('action')
    
    if action == 'remove':
        coffee_shop.remove_from_order(item)
    elif action == 'update':
        new_quantity = int(request.form.get('quantity', 1))
        coffee_shop.update_order_item(item, new_quantity)
    
    return redirect(url_for('show_order'))

@app.route('/confirm_order')
def confirm_order():
    order_summary = coffee_shop.confirm_order()
    menu = coffee_shop.show_menu()
    return render_template('index.html', menu=menu, order_summary=order_summary)

if __name__ == '__main__':
    app.run(debug=True)