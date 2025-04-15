from odoo import models, fields, api
from odoo.exceptions import ValidationError,UserError
from datetime import date

class Patient(models.Model):
    _name = 'hospital.patients'
    _description = 'Hospital Patient'


    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    birth_date = fields.Date(string='Birth Date')
    age = fields.Integer(string='Age', compute='_compute_age', store=True)
    address = fields.Text(string='Address')
    email = fields.Char(string='Email')
    doctors_id = fields.Many2many('hospital.doctors', string='Doctors')
    department_id = fields.Many2one('hospital.departments', string='Department')
    capacity_id = fields.Integer(related='department_id.capacity', string="Capacity", readonly=True)
    history_log = fields.One2many('hospital.patient.log', 'patients_id', string='History Log')
    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious')
    ], string="State", default='undetermined')
    cr_ratio = fields.Float(string='CR Ratio')
    pcr = fields.Boolean(string='PCR')
    history = fields.Text(string='History')
    blood_type = fields.Selection([
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-')
    ], string='Blood Type')
    image = fields.Binary(string='Image')

    @api.depends('birth_date')
    def _compute_age(self):
        for record in self:
            if record.birth_date:
                today = date.today()
                record.age = today.year - record.birth_date.year - (
                    (today.month, today.day) < (record.birth_date.month, record.birth_date.day)
                )
            else:
                record.age = 0

    @api.onchange('department_id')
    def _onchange_department_id(self):
        self.doctors_id = [(5, 0, 0)]
        return {'domain': {'doctors_id': [('id', 'in', [])]}}

    @api.constrains('department_id')
    def _check_department_is_opened(self):
        for record in self:
            if record.department_id and not record.department_id.is_opened:
                raise ValidationError("Cannot assign patient to a closed department")

    @api.onchange('age')
    def _onchange_age(self):
        for record in self:
            if record.age < 30:
                record.pcr = True
                return {
                    'warning': {
                        'title': 'PCR Checked',
                        'message': 'PCR has been automatically checked as age is below 30.'
                    }
                }
            else:
                record.pcr = False

    @api.constrains('pcr', 'cr_ratio')
    def _check_cr_ratio(self):
        for record in self:
            if record.pcr and not record.cr_ratio:
                raise ValidationError("CR Ratio is mandatory when PCR is checked.")

    @api.onchange('state')
    def _onchange_state(self):
        if self.state and self.id:
            self.env['hospital.patient.log'].create({
                'patients_id': self.id,
                'created_by': self.env.user.id,
                'date': fields.Datetime.now(),
                'description': f'State changed to {self.state}',
            })

    @api.model
    def create(self, vals):
        first_name = vals.get('first_name', '').strip()
        last_name = vals.get('last_name', '').strip()
        if first_name and last_name:
            email = f"{first_name[0]}{last_name}@gmail.com".lower()
            vals['email'] = email
        else:
            raise UserError("First Name and Last Name are required to generate the email.")

        return super(Patient, self).create(vals)

    def write(self, vals):
        first_name = vals.get('first_name',self.first_name).strip() if 'first_name' in vals else self.first_name.strip()
        last_name = vals.get('last_name', self.last_name).strip() if 'last_name' in vals else self.last_name.strip()
        if first_name and last_name:
            email = f"{first_name[0]}{last_name}@gmail.com".lower()
            vals['email'] = email
        super(Patient, self).write(vals)

class HMSPatientsLog(models.Model):
    _name = "hospital.patient.log"
    _description = 'Hospital Patients Log'

    patients_id = fields.Many2one('hospital.patients', string="Patient", required=True)
    created_by = fields.Many2one('res.users', string="Created By", required=True, default=lambda self: self.env.user)
    date = fields.Datetime(string='Date', required=True, default=fields.Datetime.now)
    description = fields.Text(string='Description')