from odoo import models, fields, api


class HospitalAppointment(models.Model):
    _name = "hospital.appointment"



    name = fields.Char()
    patient_id = fields.Many2one('hospital.patient', string='the Patient')


