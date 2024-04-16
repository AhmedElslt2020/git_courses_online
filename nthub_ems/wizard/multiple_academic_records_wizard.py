# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class MultipleAcademicRecordsWizard(models.TransientModel):
    _name = "multiple.academic.records"
    _description = "Wizard: 'Create Multiple Academic Records'"

    yro = fields.Integer(default=fields.date.today().year, string=_("Office Year"), required=True)
    level_id = fields.Many2one("level", string=_('Level'))
    department_id = fields.Many2one("department", string=_('Department'))
    sub_department_id = fields.Many2one("sub.department", string=_('Division'),
                                        domain="[('department_id', '=', department_id)]")
    type = fields.Selection([('class', 'Number Of Classes'), ('student', 'Students In Classes')],
                            string=_('Distribution Type'))
    type_committees = fields.Selection(
        [('committee', 'Number Of Committees'), ('student_committee', 'Students In Committees')],
        string=_('Distribution Type'))
    number = fields.Integer(string=_("Number"))
    is_committees = fields.Boolean()
    is_sitting_number = fields.Boolean()

    def action_multiple_academic_records(self):
        if self.level_id and self.department_id and self.sub_department_id and self.yro:
            no_of_student: int = 0
            education_records = self.env['education.record'].search(
                [('level_id', '=', self.level_id.id), ('department_id', '=', self.department_id.id),
                 ('sub_department_id', '=', self.sub_department_id.id), ('yro', '=', self.yro)], order='name')
            if self.is_committees == False:
                if self.type == 'student':
                    no_of_student = self.number
                elif self.type == 'class':
                    no_of_student = int(len(education_records) / self.number)
                cur_class: int = 1
                cur_cap: int = 0
                for rec in education_records:
                    rec.class_number = cur_class
                    cur_cap += 1
                    if cur_cap == no_of_student:
                        cur_class += 1
                        cur_cap = 0
            elif self.is_committees == True:
                if self.type_committees == 'student_committee':
                    no_of_student = self.number
                elif self.type_committees == 'committee':
                    no_of_student = int(len(education_records) / self.number)
                cur_committee: int = 1
                cur_cap: int = 0
                for rec in education_records:
                    rec.committees_number = cur_committee
                    cur_cap += 1
                    rec.chair_number = cur_cap
                    if cur_cap == no_of_student:
                        cur_committee += 1
                        cur_cap = 0
            return {
                'name': 'Academic Records',
                'view_mode': 'tree,form',
                'res_model': 'education.record',
                'type': 'ir.actions.act_window',
                'target': 'main',
            }

    # @api.onchange('level_id', 'department_id', 'sub_department_id', 'yro')
    # def get_students(self):
    #     self.student_ids = [(5, 0, 0)]
    #     if self.level_id and self.department_id and self.sub_department_id and self.yro:
    #         education_records = self.env['education.record'].search(
    #             [('level_id', '=', self.level_id.id), ('department_id', '=', self.department_id.id),
    #              ('sub_department_id', '=', self.sub_department_id.id), ('yro', '=', self.yro)])
    #         student_records = [line.student_id for line in education_records]
    #         for s in student_records:
    #             self.student_ids += s
    #     else:
    #         self.student_ids = False
