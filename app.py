from sanic import Sanic, response
from sanic.exceptions import SanicException
from sanic_session import Session, InMemorySessionInterface
from sanic_jinja2 import SanicJinja2
from sanic.request import Request
from models import Users, Item, Category
from sanic.response import json
from tortoise.contrib.sanic import register_tortoise
from pprint import pformat


app = Sanic(__name__)
register_tortoise(
    app,
    db_url='postgres://postgres:postgres@localhost:5432/madao',
    modules={"models": ["models"]},
    generate_schemas=True
)

# Завантаження статичних файлів
app.static('/assets', './assets')
session = Session(app, interface=InMemorySessionInterface())
jinja = SanicJinja2(app, session=session, pkg_name='templates')

# Shop card
@app.route('/card')
@jinja.template("shop-card.html")
async def shopcard(request):
    return dict(
        greetings="Hello, template decorator!",
        )
    
# Home page with the list of products
@app.route('/')
@jinja.template("op-dotted-menu.html")
async def index(request):
    items = await Item.filter(exist=True).select_related("category").all()
    filter_obj = [{"name":item.category.name,"slug":item.category.slug} for item in items]
    unique_filter = [dict(t) for t in {tuple(d.items()) for d in filter_obj}]
    return dict(
        greetings="Hello, template decorator!",
        pysankyx=[item.to_dict() for item in items],
        filter=unique_filter
        )


# Admin page to upload products
@app.route('/admin/upload', methods=['POST'])
async def upload_product(request):
    if not request.json:
        raise SanicException('Invalid JSON payload', status_code=400)

    product = {
        'id': len(products) + 1,
        'name': request.json.get('name'),
        'description': request.json.get('description'),
        'image_url': request.json.get('image_url')
    }

    products.append(product)
    return response.json(product, status=201)

# Error handler for SanicExceptions
@app.exception(SanicException)
async def handle_exceptions(request, exception):
    return response.json({'error': str(exception)}, status=exception.status_code)

@app.route("/user")
async def list_all(request):
    users = await Users.all()
    return response.json({"users": [str(user) for user in users]})


@app.route("/user/<pk:int>")
async def get_user(request, pk):
    user = await Users.get(pk=pk)
    return response.json({"user": str(user)})

# Route for uploading an Item
@app.post("/items")
async def create_item(request: Request):
    # Extract the data from the request
    name = request.form.get("name")
    description = request.form.get("description")
    link = request.form.get("link")
    slider = request.form.get("slider")
    price = request.form.get("price")
    category = request.form.get("category")
    # Access the uploaded files
    image1 = request.files.get("image1")
    image2 = request.files.get("image2")
    image3 = request.files.get("image3")
    image4 = request.files.get("image4")

    # Save the uploaded files to a desired location
    image1_path = f"assets/uploads/{image1.name}_1.jpg"
    image2_path = f"assets/uploads/{image2.name}_2.jpg"
    image3_path = f"assets/uploads/{image3.name}_3.jpg"
    if image4:
        image4_path = f"assets/uploads/{image4.name}_3.jpg"
    # Path to db
    image1_path_db = f"uploads/{image1.name}_1.jpg"
    image2_path_db = f"uploads/{image2.name}_2.jpg"
    image3_path_db = f"uploads/{image3.name}_3.jpg"
    if image4:
        image4_path_db = f"uploads/{image4.name}_3.jpg"
    else:
        image4_path_db = None
    with open(image1_path, "wb") as f:
        f.write(image1.body)
    with open(image2_path, "wb") as f:
        f.write(image2.body)
    with open(image3_path, "wb") as f:
        f.write(image3.body)
    if image4:
        with open(image4_path, "wb") as f:
            f.write(image4.body)
    # Create a new Item object
    item = Item(
        name=name,
        description=description,
        link=link,
        price=price,
        slider=slider,
        image1=image1_path_db,
        image2=image2_path_db,
        image3=image3_path_db,
        image4=image4_path_db,
        category_id=int(category),
    )

    # Save the Item to the database
    await item.save()

    return json({"message": "Item created successfully", "item": item.to_dict()})
# CRUD endpoints for the Category

# Create a new category
@app.route('/categories', methods=['POST'])
async def create_category(request):
    data = request.json
    category = await Category.create(name=data['name'], slug=data['slug'])
    return json({'message': 'Category created successfully', 'category': category.to_dict()})

# Get all categories
@app.route('/categories', methods=['GET'])
async def get_all_categories(request):
    categories = await Category.all()
    return json({'categories': [category.to_dict() for category in categories]})

# Get a specific category by ID
@app.route('/categories/<category_id>', methods=['GET'])
async def get_category(request, category_id):
    category = await Category.get(id=category_id)
    return json({'category': category.to_dict()})

# Update a category
@app.route('/categories/<category_id>', methods=['PUT'])
async def update_category(request, category_id):
    data = request.json
    category = await Category.get(id=category_id)
    category.name = data['name']
    category.slug = data['slug']
    await category.save()
    return json({'message': 'Category updated successfully', 'category': category.to_dict()})

# Delete a category
@app.route('/categories/<category_id>', methods=['DELETE'])
async def delete_category(request, category_id):
    category = await Category.get(id=category_id)
    await category.delete()
    return json({'message': 'Category deleted successfully'})


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=8000, debug=True, auto_reload=True)
