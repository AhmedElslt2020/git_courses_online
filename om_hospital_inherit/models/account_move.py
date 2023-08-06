from datetime import date
from email.policy import default


from odoo import models, fields, api, tools


class AccountMove(models.Model):
    _inherit = 'account.move'

    so_confirmed_user_id = fields.Many2one('res.users')
    my_years = fields.Date()
    my_boolean = fields.Boolean()
    invoice_date = fields.Date()

    @api.onchange('invoice_date')
    def _compute_invoice_date(self):
        for rec in self:
            today = date.today()
            if rec.invoice_date.year < today.year:
                rec.my_boolean = True
            else:
                rec.my_boolean = False




class AccountMove(models.Model):
    _inherit = 'account.move.line'

    line_number = fields.Integer()



