from odoo.exceptions import ValidationError
from odoo import api, fields, models


class GPJInstitutionalRole(models.Model):
    _name = 'gpj.institutional.role'
    _description = 'GPJ Institutional Role'
    _order = 'name'

    name = fields.Char(required=True)
    code = fields.Char(required=True, index=True, size=16)
    institution_id = fields.Many2one(
        'gpj.institution',
        required=True,
        ondelete='restrict',
        index=True,
    )
    description = fields.Text()
    active = fields.Boolean(default=True, index=True)

    _code_institution_unique = models.Constraint(
        'UNIQUE(institution_id, code)',
        'Institutional role code must be unique within an institution.',
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            institution_id = vals.get('institution_id')
            code = vals.get('code')
            if institution_id and code:
                existing = self.with_context(active_test=False).search([
                    ('institution_id', '=', institution_id),
                    ('code', '=', code),
                ], limit=1)
                if existing:
                    raise ValidationError(
                        'Institutional role code must be unique within an institution.'
                    )
        return super().create(vals_list)
