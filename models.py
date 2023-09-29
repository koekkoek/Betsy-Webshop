# Models go here
import peewee as pw

db = pw.SqliteDatabase('betsy_webshop.db')


class BaseModel(pw.Model):
    class Meta:
        database = db


class User(BaseModel):
    username = pw.CharField(unique=True)
    street = pw.CharField(max_length=75)
    housenumber = pw.IntegerField()
    postal = pw.CharField(max_length=20)
    city = pw.CharField()
    card = pw.IntegerField()


class Product(BaseModel):
    name = pw.CharField(unique=True)
    seller = pw.ForeignKeyField(User, backref="products")
    description = pw.TextField()
    price = pw.DecimalField(auto_round=False, decimal_places=2)
    quantity = pw.IntegerField()


class Transactions(BaseModel):
    date = pw.DateField()
    buyer = pw.ForeignKeyField(User, backref="purchases")
    seller = pw.ForeignKeyField(User, backref="sales")
    product = pw.ForeignKeyField(Product, backref="transactions")
    quantity = pw.IntegerField()


class Tag(BaseModel):
    name = pw.CharField(unique=True)


class ProductTags(BaseModel):
    product_id = pw.ForeignKeyField(Product, backref="product_tags")
    tag_id = pw.ForeignKeyField(Tag, backref="product_tags")
