from odoo import models, fields, api
from odoo.exceptions import ValidationError


class StudentPartner(models.Model):
    _inherit = "res.partner"

    is_student = fields.Boolean(string="Is student")
    birth_date = fields.Date(string="Birth date")




    @api.constrains('birth_date','to_day')
    def validate_past_date(self):
        for partner in self:
            today_date = fields.Date().today()
            if partner.birth_date > today_date.today():
                raise ValidationError("your Birth date not allow to register th is  in past")


