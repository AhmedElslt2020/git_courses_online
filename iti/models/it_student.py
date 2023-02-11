from odoo import models, fields, api
from odoo.exceptions import UserError


class ITiStudent(models.Model):
    _name = "iti.student"

    name = fields.Char()
    email = fields.Char()
    birth_date = fields.Date()
    salary = fields.Float()
    tax = fields.Float(compute="calc_salary", store=True)
    net_salary = fields.Float(compute="calc_salary")
    adress = fields.Text()
    gender = fields.Selection([("m", "male"), ("f", "female")])
    accepted = fields.Boolean()
    level = fields.Integer(default=3)
    image = fields.Binary()
    cv = fields.Html()
    login_time = fields.Datetime()
    track_id = fields.Many2one("iti.track")
    track_capacity = fields.Integer(related="track_id.capacity")
    skill_id = fields.Many2many("it.skill")
    state = fields.Selection([
        ('applied', 'Applied'),
        ('first', 'first interview'),
        ('second', 'second interview'),
        ('passed', 'passed'),
        ('rejected', 'rejected'),
        ('re', 're')

    ], default="applied")
    _sql_constraints = [
        ("unique_name", "UNIQUE(name)", "name is exits"),
    ]

    @api.depends("salary")
    def calc_salary(self):
        for student in self:
            student.tax = student.salary * .20
            student.net_salary = student.salary - student.tax

    def write(self, vals):
        if "name" in vals:
            name_split = vals['name'].split()
            if len(name_split) > 1:
                vals['email'] = f"{name_split[0]}{name_split[1]}@gmail.com"
            else:
                vals['email'] = f"{name_split[0]}@gmail.com"
        return super().write(vals)

    @api.constrains("track_id")
    def check_track_id(self):
        track_count = len(self.track_id.students_id)
        track_capacity = self.track_id.capacity
        if track_count > track_capacity:
            raise UserError("TRACK IS full")

    @api.model
    def create(self, vals):
        name_split = vals['name'].split(" ")
        vals['email'] = f"{name_split[0][0]}{name_split[1]}@gmail.com"
        search_student = self.search([('email', '=', vals['email'])])
        if search_student:
            raise UserError(' EMAIL EXITS')
        return super().create(vals)

    def change_state(self):
        if self.state == 'applied':
            self.state = 'first'
        elif self.state == 'first':

            self.state = 'second'
        elif self.state in ['passed', 'rejected']:
            self.state = 'applied'

    def set_passed(self):
        self.state = 'passed'

    def set_rejected(self):
        self.state = 'rejected'

    @api.onchange("gender")
    def _on_change_gender(self):
        domain = {'track_id': []}
        if self.gender == "m":
            domain = {'track_id': [('is_open', '=', True)]}
            self.salary = 10000
        else:
            self.salary = 5000

        return {
            'warning': {
                'title': 'hello',
                'message': 'the gender has chnged'
            },
            'domain': domain
        }
