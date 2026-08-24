from odoo.exceptions import ValidationError
from odoo import api, fields, models


class GPJOrganizationalUnit(models.Model):
    _name = 'gpj.organizational.unit'
    _description = 'GPJ Organizational Unit'
    _order = 'name'
    _parent_store = True

    name = fields.Char(required=True)
    code = fields.Char(required=True, index=True, size=16)
    institution_id = fields.Many2one(
        'gpj.institution',
        required=True,
        ondelete='restrict',
        index=True,
    )
    parent_id = fields.Many2one(
        'gpj.organizational.unit',
        string='Parent Unit',
        ondelete='restrict',
        index=True,
    )
    parent_path = fields.Char(index=True)
    active = fields.Boolean(default=True, index=True)

    _code_institution_unique = models.Constraint(
        'UNIQUE(institution_id, code)',
        'Organizational unit code must be unique within an institution.',
    )

    @api.constrains('parent_id')
    def _check_parent_id_recursion(self):
        if self._has_cycle():
            raise ValidationError(
                'You cannot create a recursive hierarchy of organizational units.'
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
                        'Organizational unit code must be unique within an institution.'
                    )
        return super().create(vals_list)
