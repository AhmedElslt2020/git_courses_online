# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import json


class Marks(models.Model):
    _name = 'marks'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'marks'
    _rec_name = 'name'

    name = fields.Char(compute='_compute_name')
    student_id = fields.Many2one("res.partner", string=_('Student'), domain="[('is_student','=',True)]")
    sitting_number = fields.Char(string=_("Sitting Number"), related='education_record_id.sitting_number')
    education_record_id = fields.Many2one("education.record", string=_('Education Record'))
    office_year = fields.Integer(string=_('Office Year'))
    subject_id = fields.Many2one("subject", string=_('Subject'))
    oral_mark = fields.Integer(string=_("Oral Mark"))
    term_mark = fields.Integer(string=_("Mid Term Mark"))
    final_mark = fields.Integer(string=_("Final Mark"))
    total_mark = fields.Integer(string=_("Total Mark"), compute='_calc_total_mark', store=True)
    subject_id_domain = fields.Char(compute='_compute_subject_id_domain', readonly=True, store=False)
    percentage = fields.Float(string=_("Percentage"), compute="_calc_subject_percentage", store=True)
    degree = fields.Selection(
        [('good', 'Good'), ('very_good', 'Very Good'), ('excellent', 'Excellent'), ('pass', 'Pass'), ('fall', 'Fall'),
         ('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D'), ('f', 'F')],
        string="Degree", compute='_calc_degree')
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirmed')], default='draft')
    is_readonly = fields.Boolean()

    _sql_constraints = [
        ('mrk_record_unique', 'UNIQUE(student_id,office_year,subject_id)',
         'Must be "Student and Office Year and Subject" Unique'),
    ]

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'

    def _get_value_letters(self):
        for rec in self:
            evaluation_type = self.env['ir.config_parameter'].search([('key', '=', 'nthub_ems.evaluation_type')])
            if evaluation_type.value == 'letters':
                rec.is_letters = True
            else:
                rec.is_letters = False

    @api.depends("education_record_id", "subject_id")
    def _compute_name(self):
        """This function to sum of degree of this Subject"""
        for rec in self:
            if rec.sitting_number and rec.subject_id:
                rec.name = f'{rec.subject_id.code} / {rec.sitting_number}'
            else:
                rec.name = f'{rec.subject_id.code} / 000'

    @api.model_create_multi
    def create(self, vals_list):
        """ this field to make right and visible not edit"""
        res = super(Marks, self).create(vals_list)
        res.is_readonly = True
        if res.education_record_id:
            res.student_id = res.education_record_id.student_id
            res.office_year = res.education_record_id.yro
        return res

    @api.model_create_multi
    def create(self, vals_list):
        """ this field to make right and visible not edit"""
        res = super(Marks, self).create(vals_list)
        res.is_readonly = True
        if res.education_record_id:
            res.student_id = res.education_record_id.student_id
            res.office_year = res.education_record_id.yro
        return res

    @api.depends('percentage')
    def _calc_degree(self):
        for record in self:
            evaluation_type = self.env['ir.config_parameter'].search([('key', '=', 'nthub_ems.evaluation_type')])
            if evaluation_type.value == 'degree' or evaluation_type.value == '':
                if record.percentage >= 0.85:
                    record.degree = 'excellent'
                elif record.percentage >= 0.75:
                    record.degree = 'very_good'
                elif record.percentage >= 0.65:
                    record.degree = 'good'
                elif record.percentage >= 0.50:
                    record.degree = 'pass'
                else:
                    record.degree = 'fall'
            elif evaluation_type.value == 'letters':
                if record.percentage >= 0.85:
                    record.degree = 'a'
                elif record.percentage >= 0.75:
                    record.degree = 'b'
                elif record.percentage >= 0.65:
                    record.degree = 'c'
                elif record.percentage >= 0.50:
                    record.degree = 'd'
                else:
                    record.degree = 'f'

    @api.depends('education_record_id.level_id')
    def _compute_subject_id_domain(self):
        """Calculates the domain of subjects."""
        for rec in self:
            selected_subject_ids = rec.education_record_id.marks_ids.mapped('subject_id.id')
            subject_ids = self.env['subject'].search([('level_id', '=', rec.education_record_id.level_id.id)]).ids
            m_objects = self.search([('education_record_id.student_id', '=', rec.education_record_id.student_id.id)])
            full_subject_ids = m_objects.filtered(lambda s: s.percentage < 0.50).mapped('subject_id.id')
            pass_subject_ids = m_objects.filtered(lambda s: s.percentage >= 0.50).mapped('subject_id.id')
            # Calculate the difference between full_subject_ids and pass_subject_ids
            subject_ids = subject_ids + list(set(full_subject_ids) - set(pass_subject_ids))
            available_subject_ids = [i for i in subject_ids if i not in selected_subject_ids]
            unique_subject_ids = available_subject_ids
            rec.subject_id_domain = json.dumps([('id', 'in', unique_subject_ids)])

    @api.onchange("subject_id", 'oral_mark')
    def check_oral_mark(self):
        if self.subject_id and self.oral_mark:
            if self.oral_mark > self.subject_id.oral_mark or self.oral_mark < 0:
                self.oral_mark = self.subject_id.oral_mark

    @api.onchange("subject_id", 'term_mark')
    def check_term_mark(self):
        if self.subject_id and self.term_mark:
            if self.term_mark > self.subject_id.mid_term_mark or self.term_mark < 0:
                self.term_mark = self.subject_id.mid_term_mark

    @api.onchange("subject_id", 'final_mark')
    def check_final_mark(self):
        if self.subject_id and self.final_mark:
            if self.final_mark > self.subject_id.final_full_mark:
                self.final_mark = self.subject_id.final_full_mark

    @api.depends("oral_mark", "term_mark", "final_mark")
    def _calc_total_mark(self):
        """This function to sum of degree of this Subject"""
        for rec in self:
            if rec.final_mark > 0:
                rec.total_mark = rec.oral_mark + rec.term_mark + rec.final_mark
            else:
                rec.total_mark = rec.oral_mark + rec.term_mark

    @api.depends('total_mark', 'subject_id')
    def _calc_subject_percentage(self):
        """ This function to make percentage to student mark"""
        for rec in self:
            if rec.subject_id or rec.total_mark:
                if rec.subject_id.total_mark > 0:
                    rec.percentage = rec.total_mark / rec.subject_id.total_mark
            else:
                rec.percentage = False
