from odoo.exceptions import ValidationError
from odoo import api, fields, models


class GPJDepartment(models.Model):
    _name = 'gpj.department'
    _description = 'GPJ Department'
    _order = 'name'

    name = fields.Char(required=True)
    code = fields.Char(required=True, index=True, size=16)
    institution_id = fields.Many2one(
        'gpj.institution',
        required=True,
        ondelete='restrict',
        index=True,
    )
    campus_id = fields.Many2one(
        'gpj.campus',
        ondelete='restrict',
        index=True,
        domain="[('institution_id', '=', institution_id)]",
    )
    active = fields.Boolean(default=True, index=True)

    _code_institution_unique = models.Constraint(
        'UNIQUE(institution_id, code)',
        'Department code must be unique within an institution.',
    )

    @api.constrains('institution_id', 'campus_id')
    def _check_campus_institution_consistency(self):
        for record in self:
            if record.campus_id and record.campus_id.institution_id != record.institution_id:
                raise ValidationError(
                    'Department campus must belong to the same institution as the department.'
                )

    @api.onchange('campus_id')
    def _onchange_campus_id(self):
        if self.campus_id:
            self.institution_id = self.campus_id.institution_id

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
                        'Department code must be unique within an institution.'
                    )
        return super().create(vals_list)
