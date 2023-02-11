from odoo import models, fields, api


class HmsHistory(models.Model):
    _name = "hms.history"
    _rec_name = 'description'

    description = fields.Text()

    patient_id = fields.Many2one("hms.patient")

    @api.model
    def create(self, val_list):
        print('In Log History')

        return super(HmsHistory, self).create(val_list)

# hor = fields.Text(related="patient_od.state")
