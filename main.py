# creating all the necessary classes with their respective functions
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

# creating child classes for an admin and ordinary viewer/user
class Admin(User):
    def __init__(self, username, password):
        super().__init__(username, password)

    def add_product(self, inventory, name, category, stock, threshold):
        inventory.add_product(name, category, stock, threshold)

    def update_product(self, inventory, name, stock, threshold):  
        inventory.update_product(name, stock, threshold)

    def delete_product(self, inventory, name):
        return inventory.delete_product(name)

class Viewer(User):
    def __init__(self, username, password):
        super().__init__(username, password)

# creating a class for products
class Product:
    def __init__(self, name, category, stock, threshold):
        self.name = name
        self.category = category
        self.stock = stock
        self.threshold = threshold

# a class for inventory including logging in users
class Inventory:
    def __init__(self):
        self.products = {}
        self.users = {}

    def add_user(self, user):
        self.users[user.username] = user

    def add_product(self, name, category, stock, threshold):
        self.products[name] = Product(name, category, stock, threshold)

    def get_product_by_name(self, name):  
        return self.products.get(name)

    def search_product(self, name=None, category=None): # method to search for a specific product
        results = []
        for product in self.products.values():
            if (name and name in product.name) or (category and category == product.category):
                results.append(product.__dict__)
        return results

    def update_product(self, name, stock, threshold):  
        if name in self.products:
            self.products[name].stock = stock
            self.products[name].threshold = threshold  
            return True
        return False

    def view_products(self):  # method to view all products
        return [product.__dict__ for product in self.products.values()]
    
    def delete_product(self, name):  
        if name in self.products:
            del self.products[name]
            return True
        return False

class InventoryManagementSystem:
    def __init__(self):
        self.inventory = Inventory()
        self.logged_in_user = None

    def login(self, username, password):
        user = self.inventory.users.get(username)
        if user and user.password == password:
            self.logged_in_user = user
            return True
        return False

    def display_menu(self):
        if isinstance(self.logged_in_user, Admin):
            print(
                "1. Add Product\n"
                "2. Update Product\n"
                "3. Delete Product\n"
                "4. View Products\n"
                "5. Search for a Product\n"
                "6. Logout"
            )
        elif isinstance(self.logged_in_user, Viewer):
            print(
                "1. Enter 1 or 4 to view all our products.\n"
                "2. Enter 2 or 5 to search for a specific product.\n"
                "3. Enter 6 to logout.\n")

    def restock_alert(self):
        for product in self.inventory.products.values():
            if product.stock <= product.threshold:
                print(f"Restock Alert: {product.name} is below the threshold!")

# creating the main function

def main():
    system = InventoryManagementSystem()
    # Example users
    admin = Admin('admin', 'admin123')
    viewer = Viewer('viewer', 'viewer123')  
    system.inventory.add_user(admin)
    system.inventory.add_user(viewer)

    while True:
        username = input("Enter username: ")
        password = input("Enter password: ")

        if system.login(username, password):
            print(f"Welcome, {username}!")
            while True:
                system.display_menu()
                choice = input("Type the index of your choice: ")

                if choice == '1':
                    if isinstance(system.logged_in_user, Admin):
                        name = input("Product Name: ")
                        category = input("Category: ")
                        while True:
                            try:
                               stock = int(input("Stock Level: "))
                               break
                            except ValueError:
                                print("Error: Please enter a valid integer for stock level.")
                        while True:
                            try:
                                threshold= int(input("Please enter a low stock threshold: "))
                                break
                            except ValueError:
                                print("Error: Please enter a valid integer for low stock threshold.")
                        admin.add_product(system.inventory, name, category, stock, threshold)

                    elif isinstance(system.logged_in_user, Viewer):
                        products = system.inventory.view_products()
                        print(products)
                
              elif choice == '2':
                    if isinstance(system.logged_in_user, Admin):
        # Admin can update a product
                        name = input("Enter the name of the product to update: ")
                        product = system.inventory.search_product(name)
        
                        if product:
            # Handle new stock input with error checking
                            while True:
                                try:
                                    new_stock = int(input("Enter new stock level: "))
                                    break  # Exit loop if conversion is successful
                                except ValueError:
                                    print("Error: Please enter a valid integer for stock level.")

            # Handle new threshold input with error checking
                            while True:
                                try:
                                    new_threshold = int(input("Enter new low stock threshold: "))
                                    break  # Exit loop if conversion is successful
                                except ValueError:
                                    print("Error: Please enter a valid integer for low stock threshold.")

            # Update the product with the new values
                            admin.update_product(system.inventory, name, new_stock, new_threshold)
                            print(f"{name} successfully updated!")
                        else:
                            print("Error: Product not found.")

                        
                elif choice == '3':
                    if isinstance(system.logged_in_user, Admin):
 # Admin can delete a product
                        name = input("Enter the name of the product to delete: ")
                        product= system.inventory.search_product(name)
                        if product:
                             admin.delete_product(system.inventory, name)
                        else:
                            print("Product not found.")
                    elif isinstance(system.logged_in_user, Admin):
                            print("You do not have permission to delete products.")

                elif choice == '4':
# Both Admin and Viewer can view products
                    products = system.inventory.view_products()
                    for product in products:
                        print(product)

                elif choice == '5':
# Both Admin and Viewer can search for products
                    search_term = input("Enter product name or category to search: ")
                    results = system.inventory.search_product(name=search_term) 
                    if results:
                        for index, product in enumerate(results, start=1):  
                             print(product)
                    else:
                        print("No products found.")
                elif choice == '6':
                    print("Logging out...")
                    break  # Break out to login loop

                else:
                    print("Invalid choice. Please select a valid option.")
        else:
            print("Invalid username or password. Please try again.")

if __name__ == "__main__":
    main()
