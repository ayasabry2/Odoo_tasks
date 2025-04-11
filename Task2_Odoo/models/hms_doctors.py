from odoo import models,fields

class  doctors(models.Model):
     _name="hms.doctor"

     firstname = fields.Char()
     lastname = fields.Char()
     image =fields.Binary()

     patient_ids = fields.Many2many('hms.patient')