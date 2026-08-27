from odoo.exceptions import ValidationError
from odoo import api, fields, models


class GPJCampus(models.Model):
    _name = 'gpj.campus'
    _description = 'GPJ Campus'
    _order = 'name'

    name = fields.Char(required=True)
    code = fields.Char(required=True, index=True, size=16)
    institution_id = fields.Many2one(
        'gpj.institution',
        required=True,
        ondelete='restrict',
        index=True,
    )
    address = fields.Text()
    department_ids = fields.One2many('gpj.department', 'campus_id', string='Departments')
    active = fields.Boolean(default=True, index=True)

    _code_institution_unique = models.Constraint(
        'UNIQUE(institution_id, code)',
        'Campus code must be unique within an institution.',
    )

    @api.constrains('institution_id')
    def _check_institution_change_consistency(self):
        for campus in self:
            inconsistent = self.env['gpj.department'].search([
                ('campus_id', '=', campus.id),
                ('institution_id', '!=', campus.institution_id.id),
            ])
            if inconsistent:
                raise ValidationError(
                    'Cannot change campus institution: departments in this campus belong to a different institution.'
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
                        'Campus code must be unique within an institution.'
                    )
        return super().create(vals_list)
