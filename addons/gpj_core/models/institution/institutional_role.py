from odoo import fields, models


class GPJInstitutionalRole(models.Model):
    _name = 'gpj.institutional.role'
    _description = 'GPJ Institutional Role'
    _order = 'name'

    name = fields.Char(required=True)
    code = fields.Char(required=True, index=True)
    institution_id = fields.Many2one(
        'gpj.institution',
        required=True,
        ondelete='cascade',
        index=True,
    )
    description = fields.Text()
    active = fields.Boolean(default=True)

    _code_institution_unique = models.Constraint(
        'UNIQUE(institution_id, code)',
        'Institutional role code must be unique within an institution.',
    )
