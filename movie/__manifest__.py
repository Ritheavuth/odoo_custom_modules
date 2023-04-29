# -*- coding: utf-8 -*-
{
    'name': "Movie",
    'version': '13.0.1.0.0',
    'summary': """A Module for booking movie tickets""",
    'sequence': 0,
    'author': "Theavuth (B9)",
    'category': 'POS',
    'depends': ['base'],
    'data': [
        'security/security_access.xml',
        'security/ir.model.access.csv',
        'views/movie_view.xml',
        'wizard/movie_book_ticket_wizard_view.xml',
        'wizard/ticket_report_wizard_view.xml',
        'report/ticket_report_template.xml',
        'report/receipt.xml',
        'views/assets.xml'
    ],
    'qweb': [
        'static/src/xml/tree_view_button.xml'
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False
}
