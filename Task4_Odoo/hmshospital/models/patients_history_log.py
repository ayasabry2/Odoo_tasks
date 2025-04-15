from odoo import fields,models

class HMSPatientsLog(models.Model):
    _name = "hospital.patient.log"
    _description = 'Hospital Patients Log'

    patients_id = fields.Many2one(model="hospital.patients" , string="Patient" , required=True)
    created_by = fields.Many2one(model="res.users" , string="Created By" , required=True)
    date = fields.Datetime(string='Date',required=True, default=fields.Datetime.now)
    description = fields.Text(string='Description')