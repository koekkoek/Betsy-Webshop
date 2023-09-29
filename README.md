# Betsy Webshop
Betsy is a site where people can sell homemade goods.

## Install instructions
1. Make sure you have the latest Python version installed.
2. Download all files to your computer
3. Before running the application, instal the following modules:
    * Install Tabulate via command: pip install tabulate
4. You can start using the program by editing the functions in main.py

## Features
Some examples on how to use Betsy Webshop. Go to the bottom of main.py and change wich function you want to use.

1. Want to try Betsy Webshop with demo data? use:

Use function populate_test_database()

2. Do you want to delete the database?

Use delete_database()

Attention: be aware this function will delete the entire database. Permanent.

3. Want to search the database for a product?

Use search("\<search_term>"). Change search_term to the word you're searching for.

4. Do you want to view all products of a given user?

Use list_user_products("\<username>"). Change argument for the user you need.

5. Want an overview of all products of a specific tag?

Use list_products_per_tag("\<argument>"). Fill in your own tag.

6. Do you want to add a product to the catalog?

Use add_product_to_catalog("\<username>", \<product_item>). Pay attention: product_item has to be a dict with the following keys:
* name
* description
* price
* quantity
* tags (use a list for multiplye tags)

7. Stock change? Update the amount of a product with this function.

Use update_stock("9", "500"). The first argument has to be the product_id and the second argument the new stock amount.

8. Do you want to remove a product?

Use remove_product(\<product_id>). Make sure you use the right product_id, because deleting it will be permanent.

9. Want to purchase a product? Let this function handle the entire transaction.

Use purchase_product(\<product_id>, \<buyer_id>, \<quantity>).
* product_id has to be an int and the id of the product you want to sell.
* buyer_id has to be an int and the buyers' id.
* quantity has to be an int, a positive number and can't be greater then the current stock.

# Author
Michel. Need some help? Send an e-mail to helpdesk@betsy-webshop.nl
