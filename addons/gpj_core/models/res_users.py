from odoo import api, fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    gpj_institution_membership_ids = fields.One2many(
        'gpj.institution.membership', 'user_id', string='Institution Memberships'
    )

    gpj_institution_ids = fields.Many2many(
        'gpj.institution',
        compute='_compute_gpj_institution_ids',
        search='_search_gpj_institution_ids',
        string='Accessible Institutions',
        help='Institutions this user has active membership in'
    )

    gpj_active_institution_id = fields.Many2one(
        'gpj.institution',
        string='Active Institution',
        default=lambda self: self._default_gpj_active_institution(),
        help='Currently selected institution (UI context only; not a security boundary)',
        domain="[('id', 'in', gpj_institution_ids)]",
    )

    def _default_gpj_active_institution(self):
        membership = self.env.user.gpj_institution_membership_ids.filtered(
            lambda m: m.active and m.is_default
        )[:1]
        return membership.institution_id

    @api.depends(
        'gpj_institution_membership_ids.active',
        'gpj_institution_membership_ids.institution_id'
    )
    def _compute_gpj_institution_ids(self):
        for user in self:
            user.gpj_institution_ids = (
                user.gpj_institution_membership_ids
                .filtered('active')
                .institution_id
            )

    def _search_gpj_institution_ids(self, operator, value):
        # Translate the computed Many2many filter into a domain on res.users
        # that mirrors _compute_gpj_institution_ids (active memberships only).
        if operator not in ('=', '!=', 'in', 'not in'):
            return [
                ('gpj_institution_membership_ids.institution_id', operator, value),
                ('gpj_institution_membership_ids.active', '=', True),
            ]
        values = list(value) if isinstance(value, (list, tuple)) else [value]
        self.env.cr.execute(
            """
            SELECT DISTINCT m.user_id
            FROM gpj_institution_membership m
            WHERE m.active = TRUE
              AND m.institution_id = ANY(%s)
            """,
            [values],
        )
        user_ids = [r[0] for r in self.env.cr.fetchall()]
        if operator in ('=', 'in'):
            return [('id', 'in', user_ids)]
        # '!=' / 'not in'
        return [('id', 'not in', user_ids)]
