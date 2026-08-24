from odoo import fields, models


class GPJDesignation(models.Model):
    _name = 'gpj.designation'
    _description = 'GPJ Designation'
    _order = 'name'

    name = fields.Char(required=True)
    code = fields.Char(required=True, index=True)
    institution_id = fields.Many2one(
        'gpj.institution',
        required=True,
        ondelete='cascade',
        index=True,
    )
    active = fields.Boolean(default=True)

    _code_institution_unique = models.Constraint(
        'UNIQUE(institution_id, code)',
        'Designation code must be unique within an institution.',
    )
