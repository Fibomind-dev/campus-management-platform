from odoo import fields, models


class GPJCampus(models.Model):
    _name = 'gpj.campus'
    _description = 'GPJ Campus'
    _order = 'name'

    name = fields.Char(required=True)
    code = fields.Char(required=True, index=True)
    institution_id = fields.Many2one(
        'gpj.institution',
        required=True,
        ondelete='cascade',
        index=True,
    )
    address = fields.Text()
    active = fields.Boolean(default=True)

    _code_institution_unique = models.Constraint(
        'UNIQUE(institution_id, code)',
        'Campus code must be unique within an institution.',
    )
