class Product:
    def __init__(self, name, category, price, stock_quantity):
        self.name = name
        self.category = category
        self.price = price
        self.stock_quantity = stock_quantity

    def change_price(self, new_price):
        if new_price < 0:
            print("Price cannot be less then 0!!!")
            return
        self.price = new_price

    def change_stock(self, new_quantity):
        if new_quantity < 0:
            print("Amound cannot be less then 0!!!")
            return
        self.stock_quantity = new_quantity

    def __str__(self):
        return f"{self.name} | Category: {self.category} | Price: {self.price} UAH | In stock: {self.stock_quantity}"


class Order:
    def __init__(self):
        self.products = []
        self.total_amount = 0

    def add_product(self, product, quantity):
        if quantity <= 0:
            print("Amount cannot be less then 0!!!.")
            return

        if product.stock_quantity >= quantity:
            self.products.append((product, quantity))
            product.stock_quantity -= quantity
            self.calculate_total()
        else:
            print(f" Not enough '{product.name}' in stock.")

    def calculate_total(self):
        self.total_amount = sum(product.price * quantity for product, quantity in self.products)
        return self.total_amount

    def __str__(self):
        if not self.products:
            return "Order is empty."

        result = "Order:\n"
        for product, quantity in self.products:
            result += f"- {product.name} x {quantity} = {product.price * quantity} UAH\n"
        result += f"Total price: {self.total_amount} UAH"
        return result


class Customer:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.orders = []

    def add_order(self, order):
        self.orders.append(order)

    def __str__(self):
        return f"{self.name} | Email: {self.email} | Amound of orders: {len(self.orders)}"


class Store:
    def __init__(self):
        self.products = []
        self.customers = []

    def add_product(self, product):
        self.products.append(product)

    def add_customer(self, customer):
        self.customers.append(customer)

    def find_product_by_name(self, product_name):
        for product in self.products:
            if product.name.lower() == product_name.lower():
                return product
        return None

    def find_customer_by_email(self, email):
        for customer in self.customers:
            if customer.email.lower() == email.lower():
                return customer
        return None

    def load_from_txt(self, filename):
        section = None

        try:
            with open(filename, "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()

                    if not line or line.startswith("#"):
                        continue

                    if line.upper() == "[PRODUCTS]":
                        section = "products"
                        continue
                    elif line.upper() == "[CUSTOMERS]":
                        section = "customers"
                        continue

                    parts = line.split(";")

                    if section == "products":
                        if len(parts) == 4:
                            name = parts[0]
                            category = parts[1]
                            price = float(parts[2])
                            stock_quantity = int(parts[3])

                            product = Product(name, category, price, stock_quantity)
                            self.add_product(product)

                    elif section == "customers":
                        if len(parts) == 2:
                            name = parts[0]
                            email = parts[1]

                            customer = Customer(name, email)
                            self.add_customer(customer)

        except FileNotFoundError:
            print(f" File {filename} not found.")

    def show_products(self):
        print("\nList of products:")
        for product in self.products:
            print(product)

    def show_customers(self):
        print("\nList of customers:")
        for customer in self.customers:
            print(customer)

store = Store()
store.load_from_txt("store_data.txt")

print("=== Initial store data ===")
store.show_products()
print()
store.show_customers()

print("\n=== Creating an order ===")

customer = store.add_customer("ivan@gmail.com")
product1 = store.add_product("Ведмедик")
product2 = store.add_product("LEGO City")

if customer and product1 and product2:
    order = Order()
    order.add_product(product1, 2)
    order.add_product(product2, 1)
    order.calculate_total()

    customer.add_order(order)

    print(customer)
    print(order)
else:
    print("Failed to create order")

print("\n=== Remaining products after order ===")
store.show_products()