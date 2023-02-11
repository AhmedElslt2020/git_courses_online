from odoo import models, fields


class HmsDoctor(models.Model):
    _name = "hms.doctor"

    name = fields.Char()
    last_name = fields.Char()
    image = fields.Binary()
    department_id = fields.Many2many("hms.department")
