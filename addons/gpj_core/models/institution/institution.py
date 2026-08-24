from odoo import fields, models


class GPJInstitution(models.Model):
    _name = 'gpj.institution'
    _description = 'GPJ Institution'
    _order = 'name'

    name = fields.Char(required=True)
    code = fields.Char(required=True, index=True)
    dte_code = fields.Char(string='DTE Code')
    msbte_code = fields.Char(string='MSBTE Code')
    established_year = fields.Integer()
    institution_type = fields.Selection(
        [
            ('government', 'Government'),
            ('aided', 'Aided'),
            ('private', 'Private'),
            ('other', 'Other'),
        ],
        default='government',
        required=True,
    )
    active = fields.Boolean(default=True)

    _code_unique = models.Constraint(
        'UNIQUE(code)',
        'Institution code must be unique.',
    )
