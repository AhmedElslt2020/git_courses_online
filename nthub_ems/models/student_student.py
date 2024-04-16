from odoo import api, fields, models, _
from odoo.exceptions import MissingError, ValidationError, AccessError
from odoo.exceptions import UserError
import re


class StudentResPartnerInherit(models.Model):
    _inherit = 'res.partner'
    _order = 'name'

    alternative_name = fields.Char(string=_('Alternative Name'))
    birth_date = fields.Date(string=_('Birth Date'), required=True)
    age = fields.Integer(string=_('Age'), store=True, compute='calc_age_student')
    place_of_birth = fields.Char(string=_('Place Of Birth'), required=True)
    qualification = fields.Many2one('qualification.student', string=_('Qualification'))
    image_qualify = fields.Binary(string="Qualify Attach")
    is_student = fields.Boolean(string=_('Is Student'), default=False)
    is_graduated = fields.Boolean(string=_('Is Graduated'), default=False)
    street = fields.Char()
    street2 = fields.Char()
    city = fields.Char()
    country_id = fields.Many2one('res.country', string=_('Country'))

    # Parent Information
    parent_name_other = fields.Char(string=_('Parent Name'))
    parent_job = fields.Char(string=_('Parent Job'))
    street_two = fields.Char()
    street2_two = fields.Char()
    city_two = fields.Char()
    country_two_id = fields.Many2one('res.country', string=_('Country'))
    phone = fields.Char(unaccent=False)
    email = fields.Char()
    joining_date = fields.Char(string=_('Joining Date'))

    gender = fields.Selection([("male", "Male"), ("female", "Female")], default="female")
    army_state = fields.Selection([("exempt", "Exempt"), ("muggle", "Muggle"), ("finished", "Finished")])
    nationality = fields.Selection([("egyptian", "Egyptian"), ("other", "Other")], default="egyptian")
    education_record_ids = fields.One2many('education.record', 'student_id')
    other = fields.Char()
    triple_number = fields.Integer(string=_('Triple Number'))
    Postponement_decision_no = fields.Char(string=_('Postponement Decision Number'))
    Postponement_date = fields.Date(string=_('Postponement Date'))
    student_total_mark = fields.Integer(compute="comput_student_total_mark", string="Student Total Marks")
    sum_year_total = fields.Float(compute="compute_sum_year_total")
    student_total_percentage = fields.Float(compute="compute_sum_year_total")

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Name must be unique!'),
        ('alternative_name_unique', 'UNIQUE(alternative_name)', 'Alternative Name must be unique!'),
    ]

    @api.depends('birth_date')
    def calc_age_student(self):
        """ calculate age from birth_date"""
        for rec in self:
            today = fields.Date.today()
            if rec.birth_date:
                rec.age = today.year - rec.birth_date.year
            else:
                rec.age = False

    @api.onchange('name')
    def get_parent_name(self):
        """ Get Parent Name"""
        if self.name and not self.parent_name_other:
            name_content = self.name.split()
            if len(name_content) > 1:
                name_content.pop(0)
                parent = " ".join(name_content)
                self.parent_name_other = parent

    @api.constrains("email")
    def check_email(self):
        if self.email:
            my_pattern = r'^[a-zA-Z0-9\.]+@[a-z0-9]+\.(com|org|net)$'
            is_match = re.match(my_pattern, self.email)
            if not is_match:
                raise UserError(f'This email {self.email} is Invalid')

    @api.constrains('phone')
    def _check_phone_number(self):
        for record in self:
            if record.phone and not record.phone.isdigit():
                raise ValidationError("Phone number must contain only digits.")

    def comput_student_total_mark(self):
        """calculates the total mark to the student and not sum the subject less than 50"""
        for rec in self:
            rec.student_total_mark = sum(
                rec.education_record_ids.mapped("marks_ids").filtered(lambda x: x.percentage > .50).mapped(
                    "total_mark"))

    def compute_sum_year_total(self):
        """calculates the sum year total to the student"""
        for rec in self:
            rec.sum_year_total = sum(rec.education_record_ids.mapped("level_id").mapped("sum_mark_level"))
            if rec.student_total_mark or rec.sum_year_total:
                rec.student_total_percentage = rec.student_total_mark / rec.sum_year_total
            else:
                rec.student_total_percentage = 0
