{
    'name': 'stock_lote',
    'version': '1.0',
    'category': 'sale',
    'summary': '',
    'depends': [
        'sale_management',
        'stock',
        'sale_coupon',
        'product_expiry',
    ],
    'data': [
        # Views
        'views/sale_order_views.xml',
        'views/stock_move_views.xml',
        'views/coupon_program_views.xml',
    ],
}
