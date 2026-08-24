{
    'name': 'GPJ Core',
    'version': '1.0.0',
    'category': 'Campus Management',
    'summary': 'Core models and shared foundations for campus management',
    'description': """
GPJ Core
=======

Provides the foundational models and shared infrastructure
for the campus management system.
    """,
    'author': 'FiboMind',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
