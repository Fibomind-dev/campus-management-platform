from odoo import models, fields


class SimpleNotes(models.Model):
    _name = 'simple.notes'
    _description = 'Simple Notes'
    _order = 'date desc, id desc'

    name = fields.Char(string='Title', required=True)
    partner_id = fields.Many2one(
        'res.partner',
        string='Contact',
        required=True,
        ondelete='cascade',
        index=True,
    )
    content = fields.Text(string='Content')
    date = fields.Date(string='Date', default=fields.Date.today)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    simple_notes_ids = fields.One2many(
        'simple.notes',
        'partner_id',
        string='Notes',
    )
