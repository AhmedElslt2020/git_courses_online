from odoo import models,fields

class ITiTrack(models.Model):
    _name ="iti.track"

    name = fields.Char()
    is_open = fields.Boolean()
    capacity = fields.Integer()
    students_id= fields.One2many("iti.student","track_id")