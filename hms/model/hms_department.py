from odoo import models, fields


class HmsDepartment(models.Model):
    _name = "hms.department"

    name = fields.Char()
    capacity= fields.Integer()
    is_open = fields.Boolean()
    patient_id = fields.One2many("hms.patient", "depart_id")
    doctor_ids = fields.Many2many("hms.doctor", "dep_doc_rel", "dep_id", "doc_id")


