from odoo import fields,models

class HMSDepartment(models.Model):
    _name = "hospital.departments"
    _description = 'Hospital Department'
    name = fields.Char(string="Department", required=True)
    capacity = fields.Integer(string="Capacity",required=True)
    is_opened = fields.Boolean(string="Is Opened")
    patients_id = fields.One2many("hospital.patients","department_id",string="Patients")
