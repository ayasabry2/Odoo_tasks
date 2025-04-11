from odoo import models, fields, api

class HMSPatient(models.Model):
    _name = 'hms.patient'
    _description = 'Hospital Patient'

    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    birth_date = fields.Date(string='Birth Date', required=True)
    age = fields.Integer(string='Age', compute='_compute_age', store=True)
    history = fields.Html(string='History')
    cr_ratio = fields.Float(string='CR Ratio', digits=(6, 2))
    blood_type = fields.Selection([
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-')
    ], string='Blood Type')
    pcr = fields.Boolean(string='PCR')
    image = fields.Binary(string='Image')
    address = fields.Text(string='Address')

    @api.depends('birth_date')
    def _compute_age(self):
        for record in self:
            if record.birth_date:
                today = fields.Date.today()
                birth = fields.Date.from_string(record.birth_date)
                record.age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
            else:
                record.age = 0