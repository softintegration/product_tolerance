# -*- coding: utf-8 -*- 


{
    'name': 'Product tolerance',
    'author': 'Soft-integration',
    'application': False,
    'installable': True,
    'auto_install': False,
    'qweb': [],
    'description': False,
    'images': [],
    'version': '1.0.1.1',
    'category': 'Product',
    'demo': [],
    'depends': ['stock'],
    'data': [
        'security/ir.model.access.csv',
        'security/product_tolerance_security.xml',
        'views/product_views.xml',
        'views/res_config_settings_views.xml',
    ],
    'license': 'LGPL-3',
}
