from odoo import models, fields, api, tools


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = "Hospital Patient"

    name = fields.Char(string="Name",tracking=True)
    age = fields.Integer(string="Age")
    gender = fields.Selection(selection=[
        ("male", "Male"),
        ("female", "Female")],string="Gender")
    ref = fields.Char(string="Reference")
