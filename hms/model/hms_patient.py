from odoo import models, fields, api
from odoo.exceptions import UserError
import re
from datetime import datetime


class HmsPatient(models.Model):
    _name = "hms.patient"

    name = fields.Char()
    Last_name = fields.Char()
    email = fields.Char()
    Birth_data = fields.Date()
    Age = fields.Integer(compute="get_age", store=True)
    History_data = fields.Html()
    Blood_down = fields.Selection([("a", "a"), ("o", "o"), ("ab", "ab")])
    image = fields.Binary()

    Pcr = fields.Boolean()
    Cr_ratio = fields.Float()
    Address = fields.Text()
    # Age = fields.Integer()
    depart_id = fields.Many2one("hms.department")
    dep_capacity = fields.Integer(related="depart_id.capacity")
    doctor_id = fields.Many2many("hms.doctor")
    state = fields.Selection([("undetermined", "Undetermined"),
                              ("good", "Good"),
                              ("fair", "Fair"),
                              ("serious", "Serious")
                              ], default="undetermined")
    history_ids = fields.One2many("hms.history", "patient_id")

    _sql_constraints = [
        ("unique email", "UNIQUE(email)", " email is exitsss"),
    ]

    @api.model
    def create(self, vals):
        search_customer = self.search([('email', '=', vals['email'])])
        if search_customer:
            raise UserError(' EMAIL EXITS')
        return super().create(vals)

    @api.constrains("email")
    def check_email(self):
        if self.email:
            my_pattern = r'^[a-zA-Z0-9\.]+@[a-z0-9]+\.(com|org|net)$'
            is_match = re.match(my_pattern, self.email)
            if not is_match:
                raise UserError(f'This email {self.email} is Invalid')

    @api.onchange("Age")
    def _on_change_gender(self):
        if self.Age < 30:
            self.Pcr = True
        else:
            self.Pcr = False
        return {
            'warning': {
                'title': 'hello',
                'message': 'the Pcr has chnged'
            }}

    def create_log(self):
        self.env['hms.history'].create({
            'description': f'change to new state {self.state}',
            'patient_id': self.id,
        })

    def set_good(self):
        for record in self:
            record.state = 'good'
            record.create_log()

    def set_fair(self):
        for record in self:
            record.state = 'fair'
            record.create_log()

    def set_serious(self):
        for record in self:
            record.state = 'serious'
            record.create_log()

    def set_back(self):
        for record in self:
            record.state = 'undetermined'
            record.create_log()

    @api.onchange("Birth_data")
    def get_age(self):
        for record in self:
            if record.Birth_data:
                Birth_data_time = datetime.strptime(str(record.Birth_data), "%Y-%m-%d")

                record.Age = abs((Birth_data_time - datetime.now()).days) // 365


class ResPartner(models.Model):
    _inherit = 'res.partner'

    cat = fields.Text()
    patient_id = fields.Many2one("hms.patient", string='Patient')

    @api.model
    def create(self, vals):

        search_customer = self.env['hms.patient'].search([('email', '=', vals['email'])])
        if search_customer:
            raise UserError(' EMAIL EXITS hello this  created by patient')
        return super().create(vals)

    def unlink(self):

        if self.cat:
            raise UserError('nott deleted')

        return super().unlink()


