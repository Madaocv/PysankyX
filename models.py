from tortoise import fields, models

class Users(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(50)

    def __str__(self):
        return f"I am {self.name}"
    
class Item(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    description = fields.TextField(max_length=10000)
    slider = fields.CharField(max_length=255)
    link = fields.CharField(max_length=255, null=True)
    price = fields.CharField(max_length=255)
    image1 = fields.CharField(max_length=255, null=True)
    image2 = fields.CharField(max_length=255, null=True)
    image3 = fields.CharField(max_length=255, null=True)
    image4 = fields.CharField(max_length=255, null=True)
    customer = fields.ForeignKeyField(
        'models.Customer', related_name='items', null=True
    )
    category = fields.ForeignKeyField(
        'models.Category', related_name='items', null=True
    )
    exist = fields.BooleanField(default=True)

    def __str__(self):
        return f'<Item(id={self.id}, name={self.name})>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'link': self.link,
            'price': self.price,
            'image1': self.image1,
            'image2': self.image2,
            'image3': self.image3,
            'customer_id': self.customer_id,
            'category_name': self.category.name,
            'category_slug': self.category.slug,
            'exist': self.exist,
            'slider': self.slider,
        }


class Customer(models.Model):
    id = fields.IntField(pk=True)
    first_name = fields.CharField(max_length=50)
    last_name = fields.CharField(max_length=50)
    company_name = fields.CharField(max_length=100, null=True)
    country = fields.CharField(max_length=50)
    street_address = fields.CharField(max_length=100)
    town_city = fields.CharField(max_length=50)
    postcode_zip = fields.CharField(max_length=20)
    phone = fields.CharField(max_length=20)
    email = fields.CharField(max_length=100)
    items = fields.ReverseRelation['Item']

    def __str__(self):
        return f'<Customer(id={self.id}, first_name={self.first_name}, last_name={self.last_name})>'


class Category(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    slug = fields.CharField(max_length=255)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug
        }