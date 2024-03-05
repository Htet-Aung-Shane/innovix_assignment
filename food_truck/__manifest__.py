{
    'name': 'Food Truck',
    'description': 'Food Truck Module Developed By Htet Aung Shane',
    "depends": [
        "base",
        "product",
        "sale",
        'stock',
        "mail",
    ],
    'category': 'Customizations',
    'author': 'Htet Aung Shane',
    "license": "OPL-1",
    'installable': True,
    'auto_install': False,
    'application': True,
    "data": [
        'security/ir.model.access.csv',
        'views/product_set_sequence.xml',
        'views/product_set.xml',
        'views/sale_extension.xml',
        'views/sale_food_truck_sequence.xml',
        'views/user_extension.xml',
        'views/product_request.xml',
        'views/menu.xml',
    ],
    # 'assets':{
    #     'web.assets_backend' : [
    #         'food_truck/static/src/js/*'
    #     ]
    # }
}
