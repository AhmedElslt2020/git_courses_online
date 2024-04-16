# -*- coding: utf-8 -*-
from odoo import fields, models, api, _


class ResConfigSettingsInherit(models.TransientModel):
    _inherit = 'res.config.settings'

    evaluation_type = fields.Selection([('degree', 'By Degree'), ('letters', 'By Letters')],
                                       string=_('Evaluation Type'), config_parameter='nthub_ems.evaluation_type')

    def set_values(self):
        res = super(ResConfigSettingsInherit, self).set_values()
        self.env.cr.execute("select max(yro) from education_record as yro;")
        result = self.env.cr.fetchone()
        self.env['ir.config_parameter'].set_param('nthub_ems.maxyro', result[0])
        return res

