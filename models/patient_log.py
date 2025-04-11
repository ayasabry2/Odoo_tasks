from odoo import models,fields
class  PatientLog(models.Model):
     _name="hms.patient.log"


     patient_id = fields.Many2one('hms.patient')
     created_by = fields.Many2one('res.users')
     date = fields.Datetime()
     description = fields.Text()
