# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class Subject(models.Model):
    _name = 'subject'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Subject'
    _rec_name = "name"

    name = fields.Char(string=_("Name"))
    alternative_name = fields.Char(string=_("Alternative Name"))
    level_id = fields.Many2one("level", string='Level')
    department_id = fields.Many2one("department", string='Department')
    sub_department_id = fields.Many2one("sub.department", string='Division',
                                        domain="[('department_id', '=', department_id)]")
    instructor_ids = fields.Many2many("res.partner", string='Instructor', domain="[('is_teacher','=',True)]")
    code = fields.Char(string=_("Code"))
    oral_mark = fields.Integer(string=_("Oral Full Mark"))
    mid_term_mark = fields.Integer(string=_("Mid Term Full Mark"))
    final_full_mark = fields.Integer(string=_("Final Full Mark"))
    total_mark = fields.Integer(string=_("Total Mark"), compute="_calc_total_mark", store=True)
    lecture_hours = fields.Integer(string=_("Lecture Hours"))
    section_hours = fields.Integer(string=_("Section Hours"))
    practical_hours = fields.Integer(string=_("Practical Hours"))
    final_exam_hours = fields.Integer(string=_("Exam Hours"))
    is_readonly = fields.Boolean()

    @api.model_create_multi
    def create(self, vals_list):
        """ this field to make right and visible not edit"""
        for vals in vals_list:
            vals['is_readonly'] = True
        return super(Subject, self).create(vals_list)

    @api.onchange('oral_mark')
    def check_oral_mark(self):
        if self.oral_mark:
            if self.oral_mark < 0:
                raise UserError("You must enter degree more than Zero")

    @api.onchange('mid_term_mark')
    def check_mid_term_mark(self):
        if self.mid_term_mark:
            if self.mid_term_mark < 0:
                raise UserError("You must enter degree more than Zero")

    @api.onchange('final_full_mark')
    def check_final_full_mark(self):
        if self.final_full_mark:
            if self.final_full_mark < 0:
                raise UserError("You must enter degree more than Zero")

    @api.onchange('lecture_hours')
    def check_lecture_hours(self):
        if self.lecture_hours:
            if self.lecture_hours < 0:
                raise UserError("You must enter degree more than Zero")

    @api.onchange('section_hour')
    def check_section_hour(self):
        if self.section_hour:
            if self.section_hour < 0:
                raise UserError("You must enter degree more than Zero")

    @api.onchange('practical_hour')
    def check_practical_hour(self):
        if self.practical_hour:
            if self.practical_hour < 0:
                raise UserError("You must enter degree more than Zero")

    @api.onchange('exam_hours')
    def exam_hours(self):
        if self.exam_hours:
            if self.exam_hours < 0:
                raise UserError("You must enter degree more than Zero")

    @api.depends("oral_mark", "mid_term_mark", "final_full_mark")
    def _calc_total_mark(self):
        """This function to sum of degree of this Subject"""
        for rec in self:
            rec.total_mark = rec.oral_mark + rec.mid_term_mark + rec.final_full_mark

    def action_show_details(self):
        self.ensure_one()
        view = {
            'name': 'Subject details',
            'view_mode': 'form',
            'res_model': 'subject',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'res_id': self.id,
            'context': {'default_name': self.name, 'default_level_id': self.level_id.id,
                        'default_department_id': self.department_id.id}, 'default_code': self.code,
            'default_total_mark': self.total_mark, 'default_sub_department_id': self.sub_department_id.id,
        }
        return view
