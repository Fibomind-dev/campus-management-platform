from odoo.exceptions import ValidationError
from odoo import api, fields, models


class GPJInstitutionMembership(models.Model):
    _name = 'gpj.institution.membership'
    _description = 'GPJ Institution Membership'
    _rec_name = 'institution_id'

    user_id = fields.Many2one(
        'res.users', required=True, ondelete='cascade', index=True
    )
    institution_id = fields.Many2one(
        'gpj.institution', required=True, ondelete='cascade', index=True
    )
    role_ids = fields.Many2many(
        'gpj.institutional.role', string='Institution Roles'
    )
    is_default = fields.Boolean(
        default=False, help='Default active institution for this user'
    )
    active = fields.Boolean(default=True)

    _user_institution_unique = models.Constraint(
        'UNIQUE(user_id, institution_id)',
        'User can only have one membership per institution.',
    )

    @api.constrains('user_id', 'is_default')
    def _check_single_default_membership(self):
        for record in self:
            if record.is_default:
                other_defaults = self.search([
                    ('user_id', '=', record.user_id.id),
                    ('is_default', '=', True),
                    ('id', '!=', record.id),
                ])
                if other_defaults:
                    raise ValidationError(
                        'User can only have one default institution membership.'
                    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            user_id = vals.get('user_id')
            institution_id = vals.get('institution_id')
            if user_id and institution_id:
                existing = self.with_context(active_test=False).search([
                    ('user_id', '=', user_id),
                    ('institution_id', '=', institution_id),
                ], limit=1)
                if existing:
                    raise ValidationError(
                        'User can only have one membership per institution.'
                    )
            if user_id and vals.get('is_default'):
                existing_default = self.search([
                    ('user_id', '=', user_id),
                    ('is_default', '=', True),
                    ('active', '=', True),
                ], limit=1)
                if existing_default:
                    raise ValidationError(
                        'User can only have one default institution membership.'
                    )

        memberships = super().create(vals_list)

        for membership in memberships:
            if membership.is_default and membership.active:
                membership.user_id.gpj_active_institution_id = membership.institution_id

        return memberships

    def init(self):
        """Create partial unique index for single default membership per user."""
        self.env.cr.execute("""
            CREATE UNIQUE INDEX IF NOT EXISTS gpj_institution_membership_user_default_uniq
            ON gpj_institution_membership (user_id)
            WHERE is_default AND active
        """)
