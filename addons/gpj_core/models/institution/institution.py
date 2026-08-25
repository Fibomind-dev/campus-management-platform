from odoo.exceptions import ValidationError
from odoo import api, fields, models


class GPJInstitution(models.Model):
    _name = 'gpj.institution'
    _description = 'GPJ Institution'
    _order = 'name'

    name = fields.Char(required=True)
    code = fields.Char(required=True, index=True, size=16)
    dte_code = fields.Char(string='DTE Code', size=16)
    msbte_code = fields.Char(string='MSBTE Code', size=16)
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
    active = fields.Boolean(default=True, index=True)

    campus_ids = fields.One2many('gpj.campus', 'institution_id', string='Campuses')
    department_ids = fields.One2many('gpj.department', 'institution_id', string='Departments')
    organizational_unit_ids = fields.One2many('gpj.organizational.unit', 'institution_id', string='Organizational Units')
    designation_ids = fields.One2many('gpj.designation', 'institution_id', string='Designations')
    institutional_role_ids = fields.One2many('gpj.institutional.role', 'institution_id', string='Institutional Roles')
    membership_ids = fields.One2many('gpj.institution.membership', 'institution_id', string='Memberships')

    _code_unique = models.Constraint(
        'UNIQUE(code)',
        'Institution code must be unique.',
    )
    _dte_code_unique = models.Constraint(
        'UNIQUE(dte_code)',
        'DTE code must be unique.',
    )
    _msbte_code_unique = models.Constraint(
        'UNIQUE(msbte_code)',
        'MSBTE code must be unique.',
    )

    @api.constrains('established_year')
    def _check_established_year(self):
        current_year = fields.Date.today().year
        for record in self:
            if record.established_year and (
                record.established_year < 1800 or record.established_year > current_year + 1
            ):
                raise ValidationError(
                    f'Established year must be between 1800 and {current_year + 1}.'
                )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            code = vals.get('code')
            if code:
                if self.with_context(active_test=False).search([('code', '=', code)], limit=1):
                    raise ValidationError('Institution code must be unique.')
            dte_code = vals.get('dte_code')
            if dte_code:
                if self.with_context(active_test=False).search([('dte_code', '=', dte_code)], limit=1):
                    raise ValidationError('DTE code must be unique.')
            msbte_code = vals.get('msbte_code')
            if msbte_code:
                if self.with_context(active_test=False).search([('msbte_code', '=', msbte_code)], limit=1):
                    raise ValidationError('MSBTE code must be unique.')
        return super().create(vals_list)

    def unlink(self):
        for institution in self:
            if institution.campus_ids or institution.department_ids \
                    or institution.organizational_unit_ids or institution.designation_ids \
                    or institution.institutional_role_ids:
                raise ValidationError(
                    'Cannot delete institution with related records. Archive it instead.'
                )
        return super().unlink()
