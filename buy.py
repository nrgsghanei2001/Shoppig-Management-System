import file_handler
import csv
import logging

# This class is for buying stuff and its for second faze and not completed yet
class Buy:
    def __init__(self, shop_name, user_name):
        logging.basicConfig(filename='records.log', filemode='a',
                            format='%(asctime)s  -  %(levelname)s - %(message)s',
                            level=logging.INFO)
        self.shop_name = shop_name
        self.user_name = user_name

    def view_products(self):
        ob = file_handler.FileHandler('products.csv')
        products = ob.read_file()
        print("\nHere is the list of products in this store:\n")
        i = 1
        for product in products:
            if product['shop_name'] == self.shop_name:
                print(f"{i} - name: {product['name']} of brand: {product['brand']} with price: {product['price']} tooman.")
                i += 1
        print()

    def search_a_product(self):
        ob = file_handler.FileHandler('products.csv')
        products = ob.read_file()
        searched = False
        name, brand = None, None
        print()
        while not searched:
            try:
                base = input("In which base do you want to search(name/brand)? ")
                if base == 'name':
                    searched = 'name'
                elif base == 'brand':
                    searched = 'brand'
                else:
                    raise Exception("There is not such a search base!")
            except Exception as error:
                print(f"{error} Please try again.")
                logging.error(f"{error}  , Happened in searching for a product.")
            if not searched:
                continue
            if searched == 'name':
                find = False
                name = input("Enter the name of product: ")
                if name:
                    print(f"\nList of all {name} in this store: (searching...)")
                    for product in products:
                        if product['shop_name'] == self.shop_name and product['name'] == name:
                            find = True
                            print(f"Of brand: {product['brand']} with price: {product['price']} tooman.")
                    if not find:
                        print(f"Sorry! There is not any {name} in this store.\n")
            elif searched == 'brand':
                find = False
                brand = input("Enter the brand of product: ")
                if brand:
                    print(f"\nList of all products with brand {brand} in this store: (searching...)")
                    for product in products:
                        if product['shop_name'] == self.shop_name and product['brand'] == brand:
                            find = True
                            print(f"name: {product['name']} with price: {product['price']} tooman.")
                    if not find:
                        print(f"Sorry! There is not any product  of brand {brand} in this store.\n")
            else:
                continue

            if searched == "name":
                brand = input(f"Enter the brand of {name} you want? ")
            elif searched == "brand":
                name = input(f"Enter the name of product you want from brand {brand}: ")
            headers = ["shop_name", "barcode", "name", "price", "brand",
                       "number", "expire_time"]
            buyed, number = None, 0
            for product in products:
                if product['name'] == name and product['brand'] == brand:
                    try:
                        number = int(input(f"How many {name} of {brand} do you want? "))
                        if number > int(product['number']):
                            raise Exception("Sorry! There is not enough of your choice.")
                    except Exception as error:
                        print(f"{error} Please try again!")
                        logging.error(f"{error}  , Happened in searching a product.")
                        break
                    buyed = product
                    break
            if buyed:
                with open("products.csv", 'w') as my_file:
                    writer = csv.DictWriter(my_file, fieldnames=headers)
                    writer.writeheader()
                    for product in products:
                        if not (product['name'] == name and product['brand'] == brand):
                            ob.add_to_file(product)
                        else:
                            updated = {"shop_name": product['shop_name'], "barcode": product['barcode'],
                                       "name": product['name'], "price": product['price'],
                                       "brand": product['brand'], "number": int(product['number']) - number,
                                       "expire_time": product['expire_time']}
                ob.add_to_file(updated)
                self.add_to_pre_invoice(name, brand, number, float(updated['price'])* number)

    def add_to_pre_invoice(self, name, brand, number, payment):
        ob = file_handler.FileHandler("pre_invoice.csv")
        new_pre_invoice = {"username": self.user_name, "shop_name": self.shop_name,
                           "name": name,"brand": brand, "number": number,
                           "payment": payment}
        ob.add_to_file(new_pre_invoice)
        print(f"from store {self.shop_name}, {number} {name} of brand \
{brand} with total price {payment} tooman was recorded for you.")





