# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from lxml import etree


class EducationRecord(models.Model):
    _name = 'education.record'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Education Record'
    _rec_name = "yro"
    _order = "name"

    student_id = fields.Many2one("res.partner", string=_('Student'), required=True, domain="[('is_student','=',True)]")
    name = fields.Char(string=_('Name'), related='student_id.name', store=True)
    level_id = fields.Many2one("level", string=_('Level'))
    department_id = fields.Many2one("department", string=_('Department'))
    sub_department_id = fields.Many2one("sub.department", string=_('Division'),
                                        domain="[('department_id', '=', department_id)]")
    yro = fields.Integer(default=fields.date.today().year, string=_("Office Year"), required=True)
    eds = fields.Selection([('fresh', 'Fresh'), ('remaining', 'Remaining'), ('chance', 'Chance')],
                           string=_("Education State"))
    class_number = fields.Integer(string=_('Class'))
    sitting_number = fields.Char(string=_("Sitting Number"))
    committees_number = fields.Integer(string=_("Committees Number"))
    chair_number = fields.Integer(string=_("Chair Number"))
    marks_ids = fields.One2many('marks', 'education_record_id')
    total_mark = fields.Float(compute='calc_total_mark', store=True, string=_("Total Marks"))
    year_percentage = fields.Float(compute='calc_year_percentage', store=True, string=_("Year Percentage"))
    nofs = fields.Float(string=_("No. of Failed Subjects"))
    # max_year = fields.Char(string=_('Max Year'), default='2024')
    is_readonly = fields.Boolean()

    _sql_constraints = [
        ('edu_record_unique', 'UNIQUE(student_id,yro)',
         'Must be "Student and Office Year" Unique'),
    ]

    @api.model
    def get_view(self, view_id=None, view_type='search', **options):
        res = super(EducationRecord, self).get_view(view_id=view_id, view_type=view_type, options=options)
        if view_type == 'search':
            doc = etree.XML(res['arch'])
            search_filter = doc.xpath("//filter[@name='max_year']")
            if search_filter:
                max_year_parameter_id = self.env['ir.config_parameter'].search([('key', '=', 'nthub_ems.maxyro')])
                # self.env.cr.execute("select max(yro) from education_record as yro;")
                # result = self.env.cr.fetchone()
                search_filter[0].set("domain", f"[('yro', '=', {max_year_parameter_id.value})]")
            res['arch'] = etree.tostring(doc, encoding='unicode')
        return res

    @api.model_create_multi
    def create(self, vals_list):
        """ this field to make right and visible not edit"""
        for vals in vals_list:
            vals['is_readonly'] = True
        res = super(EducationRecord, self).create(vals_list)
        self.env.cr.execute("select max(yro) from education_record as yro;")
        result = self.env.cr.fetchone()
        self.env['ir.config_parameter'].set_param('nthub_ems.maxyro', result[0])
        return res
    # @api.model
    # def get_view(self, view_id=None, view_type='search', **options):
    #     res = super(EducationRecord, self).get_view(view_id=view_id, view_type=view_type, options=options)
    #     if view_type == 'search':
    #         doc = etree.XML(res['arch'])
    #         search_filter = doc.xpath("//filter[@name='max_year']")
    #         if search_filter:
    #             max_year_parameter_id = self.env['ir.config_parameter'].search([('key', '=', 'nthub_ems.maxyro')])
    #             search_filter[0].set("domain",
    #                                  f"[ '|', '&', ('yro', '=', (context_today() + relativedelta(years=-1)).strftime('%Y')), ('yro', '=', context_today().strftime('%Y')), ('yro', '=', {max_year_parameter_id.value})]")
    #         res['arch'] = etree.tostring(doc, encoding='unicode')
    #     return res
    #
    # @api.model_create_multi
    # def create(self, vals_list):
    #     for vals in vals_list:
    #         vals['is_readonly'] = True
    #     res = super(EducationRecord, self).create(vals_list)
    #     self.env.cr.execute("select max(yro) from education_record as yro;")
    #     result = self.env.cr.fetchone()
    #     self.env['ir.config_parameter'].set_param('nthub_ems.maxyro', result[0])
    #     return res


    @api.depends('marks_ids.total_mark', 'marks_ids')
    def calc_total_mark(self):
        """this function add smaller than 50"""
        for rec in self:
            filtered_marks = rec.marks_ids.filtered(
                lambda x: x.subject_id.level_id.id == rec.level_id.id and x.percentage >= 0.50)
            rec.total_mark = sum(filtered_marks.mapped('total_mark'))

    @api.depends("total_mark", "level_id")
    def calc_year_percentage(self):
        """this function calculates the sum of the student marks"""
        for rec in self:
            if rec.total_mark or rec.level_id.sum_mark_level:
                rec.year_percentage = rec.total_mark / rec.level_id.sum_mark_level
            else:
                rec.year_percentage = False

    def action_multiple_academic_records(self):
        return {
            'name': 'Multiple Academic Records',
            'view_mode': 'form',
            'view_type': 'form',
            'res_model': 'multiple.academic.records',
            'type': 'ir.actions.act_window',
            'target': 'new',
        }
