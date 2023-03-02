{
    'name': 'sale_stock',
    'version': '1.0',
    'category': 'sale',
    'summary': '',
    'depends': [
        'sale_management',
        'stock',
    ],
    'data': [
        # views
        'views/sale_order_views.xml',
        'views/stock_move_views.xml',
    ],
}
