# -*- coding: utf-8 -*-

from odoo import models, fields, api,_


class Level(models.Model):
    _name = 'level'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Level'
    _rec_name = "name"

    name = fields.Char(string=_("Name"))
    alternative_name = fields.Char(string=_("Alternative Name"))
    subject_line_ids = fields.One2many("subject", "level_id")
    sum_mark_level = fields.Float(compute='_calc_sum_mark_level', store=True, string="Level Total Mark")

    @api.depends("subject_line_ids")
    def _calc_sum_mark_level(self):
        """This function to sum tho subject in the levels"""
        for rec in self:
            rec.sum_mark_level = sum(rec.subject_line_ids.mapped('total_mark'))


