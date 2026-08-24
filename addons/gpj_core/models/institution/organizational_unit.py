from odoo import fields, models


class GPJOrganizationalUnit(models.Model):
    _name = 'gpj.organizational.unit'
    _description = 'GPJ Organizational Unit'
    _order = 'name'

    name = fields.Char(required=True)
    code = fields.Char(required=True, index=True)
    institution_id = fields.Many2one(
        'gpj.institution',
        required=True,
        ondelete='cascade',
        index=True,
    )
    parent_id = fields.Many2one(
        'gpj.organizational.unit',
        string='Parent Unit',
        ondelete='restrict',
        index=True,
    )
    active = fields.Boolean(default=True)

    _code_institution_unique = models.Constraint(
        'UNIQUE(institution_id, code)',
        'Organizational unit code must be unique within an institution.',
    )
