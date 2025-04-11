from odoo import models,fields,api
from odoo.exceptions import ValidationError
class  Partner(models.Model):
     _inherit = 'res.partner'

     related_patient_id = fields.Many2one('hms.patient', string="Related Patient")

