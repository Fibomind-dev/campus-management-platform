from odoo import fields, models


class GPJDepartment(models.Model):
    _name = 'gpj.department'
    _description = 'GPJ Department'
    _order = 'name'

    name = fields.Char(required=True)
    code = fields.Char(required=True, index=True)
    institution_id = fields.Many2one(
        'gpj.institution',
        required=True,
        ondelete='cascade',
        index=True,
    )
    campus_id = fields.Many2one(
        'gpj.campus',
        ondelete='restrict',
        index=True,
    )
    active = fields.Boolean(default=True)

    _code_institution_unique = models.Constraint(
        'UNIQUE(institution_id, code)',
        'Department code must be unique within an institution.',
    )
