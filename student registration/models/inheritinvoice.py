from odoo import models, fields, api, tools


class InheritInvoice(models.Model):
    _inherit = "account.move"


    registration_id = fields.Many2one("student.registration")






