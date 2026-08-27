{
    'name': 'GPJ Core',
    'version': '1.0.0',
    'category': 'Campus Management',
    'summary': 'Core models and shared foundations for campus management',
    'description': """
GPJ Core
=========
Provides the foundational models and shared infrastructure
for the campus management system.
    """,
    'author': 'FiboMind',
    'depends': ['base', 'web'],
    'data': [
        'security/gpj_security.xml',
        'security/ir_rule.xml',
        'security/ir.model.access.csv',
        'views/dashboard/dashboard.xml',
        'views/institution/department_views.xml',
        'views/institution/organizational_unit_views.xml',
        'views/institution/designation_views.xml',
        'views/institution/institutional_role_views.xml',
        'views/membership/membership_views.xml',
        'views/institution/campus_views.xml',
        'views/institution/institution_views.xml',
        'views/users/res_users_views.xml',
        'views/menus.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'gpj_core/static/src/js/dashboard.js',
            'gpj_core/static/src/xml/dashboard.xml',
            'gpj_core/static/src/js/institution_ui.js',
            'gpj_core/static/src/xml/institution_ui.xml',
            'gpj_core/static/src/scss/institution_ui.scss',
        ],
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
