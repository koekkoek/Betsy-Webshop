# Do not modify these lines
__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

# Add your code after this line
from os import path, getcwd, remove
from tabulate import tabulate
from datetime import datetime
import json
import models as md


def search(term):
    """
    Search for products based on a term.
    """
    term = term.lower()
    query = (
        md.Product
        .select()
        .where(
            md.Product.name.contains(term) |
            md.Product.description.contains(term)
            )
            )
    # Do we have a match?
    if query:
        print(f'\nResults of "{term}":')
        results = []
        for item in query:
            results_dict = {}
            results_dict["Name"] = item.name
            results_dict["Seller"] = item.seller_id.title()
            results_dict["Description"] = item.description
            results_dict["Price"] = item.price
            results_dict["Quantity"] = item.quantity
            results.append(results_dict)
        print(tabulate(results, headers="keys", tablefmt="rounded_outline"))
        return results
    # Else we don't have a match
    else:
        print(f'No results for "{term}". Please try another word.')


def list_user_products(user_id):
    """
    View the products of a given user.
    """
    # Make query to search all products with given username
    query = (
        md.Product
        .select()
        .where(md.Product.seller == user_id)
    )
    # Make a list of dicts with all users products
    products = list(query.dicts())
    # Have we find some results?
    if products:
        print(tabulate(products, headers="keys", tablefmt="rounded_outline"))
        return products
    else:
        print(f'"{user_id}" doesn\'t have any products')


def list_products_per_tag(tag_id):
    """
    View all products for a given tag.
    """
    query = (
        md.Product
        .select()
        .join(md.ProductTags)
        .join(md.Tag)
        .where(md.Tag.name == tag_id)
    )
    products = list(query.dicts())
    # If there are some results, show them
    if products:
        print(tabulate(products, headers="keys", tablefmt="rounded_outline"))
        return products
    # No result? Show error message.
    else:
        print(f'Whoops, no product to show. You used this tag: "{tag_id}".')
        print("Please try another one.")


def add_product_to_catalog(user_id, product):
    """
    Add a product to a user.
    """
    # Check if input is valid
    # Valid username?
    query = (
        md.User
        .select(md.User.username)
    )
    usernames = []
    for item in query:
        usernames.append(item.username)
    if user_id in usernames:
        # Valid dict in function?
        productkeys = ('name', 'description', 'price', 'quantity', 'tags')
        # If product-dict in function is valid...
        if all(key in product for key in productkeys):
            # Check if product name is unique
            product_query = (
                md.Product
                .select(md.Product.name)
            )
            current_product_names = []
            for item in product_query:
                current_product_names.append(item.name)
            if product['name'] in current_product_names:
                print("Error: this product already exist.")
            else:
                # Make query to create new product in database
                md.Product.create(
                    name=product['name'],
                    seller=user_id,
                    description=product['description'],
                    price=product['price'],
                    quantity=product['quantity']
                )
                print("We added the following item to the database:")
                print(f"Product name: {product['name']}")
                print(f"Seller: {user_id}")
                print(f"Description: {product['description']}")
                print(f"Price: {product['price']}")
                print(f"Quantity: {product['quantity']}")
                print("Tags: ", end="")
                for tag in product['tags']:
                    print(tag, end=" ")

                # Check for new tags and append them to database
                tag_query = (
                    md.Tag
                    .select()
                )
                current_tags = []
                for item in tag_query:
                    current_tags.append(item.name)
                for tag in product['tags']:
                    if tag not in current_tags:
                        md.Tag.create(name=tag)
                        print(f'\n\nNew tag created: "{tag}"')
        # If product-dict in function isn't valid, show error
        else:
            print("Invalid list!")
            print("Make sure you enter a dict with the following keys:")
            print("name")
            print("description")
            print("price")
            print("quantity")
            print("tags")
    # Invalid username, print error
    else:
        print(f'Invalid username: "{user_id}" doesn\'t exist')


def update_stock(product_id, new_quantity):
    """
    Update the stock quantity of a product.
    """
    # Check if input is valid
    if isinstance(product_id, float) or isinstance(new_quantity, float):
        return print("Invalid input. Don't use a float.")
    try:
        product_id = int(product_id)
        new_quantity = int(new_quantity)

        # Check if input is an positive int
        if int(product_id) > 0 and int(new_quantity) >= 0:
            # Update product stock with new quantity
            query = (
                md.Product
                .update(quantity=new_quantity)
                .where(md.Product.id == product_id)
            )
            query.execute()
            print("Stocks updated!")
            print(f"New product quantity: {new_quantity}")
        # If number isn't positive, show error.
        else:
            print("Error: only use positive numbers")
    except ValueError:
        print("Invalid input. You can only use integers.")


def purchase_product(product_id, buyer_id, quantity):
    """
    Handle a purchase between a buyer and a seller for a given product
    """
    # Does the product exist?
    query_product = (
        md.Product
        .select()
        .where(md.Product.id == product_id)
    )
    if query_product:
        # Check if buyer exist
        query_user_id = (
            md.User
            .select(md.User.id)
            .where(md.User.id == buyer_id)
        )
        if query_user_id:
            # Check for valid quantity
            product = list(query_product.dicts())
            product_quantity = product[0]['quantity']
            if product_quantity >= quantity and product_quantity != 0:
                # There is enough to sell. So, let's make a transaction
                date = str(datetime.now().date())
                md.Transactions.create(
                    date=date,
                    buyer=buyer_id,
                    seller=product[0]['seller'],
                    product=product_id,
                    quantity=quantity
                )
                print("\nSuccesfully sold product:")
                transactions_dict = [{
                    "Date": date,
                    "Buyer": str(buyer_id),
                    "Seller": product[0]['seller'],
                    "Product": product_id,
                    "Quantity": str(quantity)
                }]
                print(tabulate(
                    transactions_dict,
                    headers="keys",
                    tablefmt="rounded_outline"))
                # Update the new product quantity.
                new_amount = product[0]['quantity'] - int(quantity)
                amount_update = (
                    md.Product
                    .update(quantity=new_amount)
                    .where(md.Product.id == product_id)
                )
                amount_update.execute()
            # Product quantity is insufficient
            else:
                print("Error: we can't sell this product.")
                print("Because the quantity is nog enough.")
                print(f"Current available quantity: {product_quantity}")
        # Invalid input, no user found...
        else:
            print("Error: user doesn't exist.")
    # Invalid input, no product found...
    else:
        print("Error: product doesn't exist.")


def remove_product(product_id):
    """
    Remove a product from a user.
    """
    # Check if input is valid
    if isinstance(product_id, float):
        return print("Invalid input. Don't use a float.")
    try:
        product_id = int(product_id)
        if int(product_id) < 0:
            return print("Please use a positive number.")
    except ValueError:
        return print("Invalid input. You can only use integers.")
    # Remove product from database
    query = (
        md.Product
        .delete()
        .where(md.Product.id == product_id)
    )
    query.execute()
    print("Succesfully removed product.")


def populate_test_database():
    """
    Function to add some test data to the database.
    """
    import_path = path.join("data", "test_database.json")
    # Get test data in JSON format
    with open(import_path) as file:
        test_data = json.load(file)

    # Make DB tables
    md.db.connect()
    md.db.create_tables(
        [md.User, md.Product, md.Transactions, md.Tag, md.ProductTags])

    # Add users to database
    for user in test_data['users']:
        md.User.create(
            username=user['username'],
            street=user['street'],
            housenumber=user['housenumber'],
            postal=user['postal'],
            city=user['city'],
            card=user['card']
        )

    # Add products to database
    for product in test_data['products']:
        md.Product.create(
            name=product['name'],
            seller=product['seller'],
            description=product['description'],
            price=product['price'],
            quantity=product['quantity']
        )

    # Add tags to database
    for tag in test_data['tags']:
        md.Tag.create(
            name=tag
        )

    # Add ProductTags to database
    for product_id, product in enumerate(test_data['products'], 1):
        for tag in product['tags']:
            tag_id = md.Tag.select(md.Tag.id).where(md.Tag.name == tag)
            md.ProductTags.create(product_id=product_id, tag_id=tag_id)

    # Add some transactions
    purchase_product(1, 1, 2)
    purchase_product(1, 1, 8)
    purchase_product(2, 3, 1)
    purchase_product(2, 2, 1)
    purchase_product(3, 4, 2)
    purchase_product(4, 2, 1)
    purchase_product(5, 4, 10)

    # Close the database
    md.db.close()


def delete_database():
    """
    Delete the database.
    """
    cwd = getcwd()
    database_path = path.join(cwd, "betsy_webshop.db")
    if path.exists(database_path):
        remove(database_path)


if __name__ == "__main__":
    populate_test_database()
    # delete_database()
    # search("Pro")
    # search("ip")
    # list_user_products("fien")
    # list_user_products("doesntexist")
    # list_products_per_tag("Electronics")
    # list_products_per_tag("doesntexist")
    product_item = {
        "name": "FIFA 24",
        "description": "New Playstation 5 soccer game.",
        "price": "60",
        "quantity": "500",
        "tags": ["Electronics", "Videogames", "Playstation"]
        }
    # add_product_to_catalog("fien", product_item)
    # add_product_to_catalog("invalidname", ["data", "Dataff"])
    # update_stock("9", "500")
    # remove_product(9)
    # purchase_product(9, 2, 250)
