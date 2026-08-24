{
    'name': 'Simple Notes',
    'version': '1.0.0',
    'category': 'Tools',
    'summary': 'Add notes to contacts',
    'description': """
Simple Notes Module
===================

Adds a Notes tab to the Contact form with a one2many relation to a
simple.notes model. Demonstrates core Odoo patterns:
- Model definition with relational fields
- View inheritance (notebook page on res.partner)
- Access rights via ir.model.access.csv
- Basic test coverage
    """,
    'author': 'FiboMind',
    'depends': ['base'],
    'data': [
        'views/simple_notes_views.xml',
        'views/partner_views.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}