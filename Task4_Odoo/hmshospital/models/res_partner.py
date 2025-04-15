from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    related_patient_id = fields.Many2one('hospital.patients', string='Related Patient')

    @api.constrains('email')
    def _check_email_not_in_patients(self):
        for record in self:
            if record.email and record.is_company == False:
                patient = self.env['hospital.patients'].search([('email', '=', record.email)], limit=1)
                if patient:
                    raise ValidationError(
                        f"Email '{record.email}' is already used by a patient ({patient.first_name} {patient.last_name})."
                    )

    @api.constrains('vat')
    def _check_vat_mandatory(self):
        for record in self:
            if record.is_company == False and record.customer_rank > 0 and not record.vat:
                raise ValidationError("Tax ID (VAT) is mandatory for customers.")

    def unlink(self):
        for record in self:
            if record.related_patient_id:
                raise ValidationError(
                    f"Cannot delete customer '{record.name}' because it is linked to patient "
                    f"'{record.related_patient_id.first_name} {record.related_patient_id.last_name}'."
                )
        return super(ResPartner, self).unlink()