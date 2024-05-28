# -*- coding: utf-8 -*-
{
    'name': "test_demo",
    'version': '17.0.1.0.0',
    'depends': ["base","purchase","website"],
    "author":"Unikerp",
    "website" : "www.unikerp.com",
    'description': """ Gestion des demo """,
    'application': True,
    'module_type' : 'officiel',
    'data': [
        'views/account.xml',
        'views/res_partner_views.xml',
        # 'views/purchase.xml',
        # 'security/ir.model.access.csv',
        # 'views/contact.xml',
        'views/purchase.xml',
        'security/security.xml',
        'security/ir.model.access.csv',


     ],
}
