from odoo import models, fields, api , _
from odoo.exceptions import ValidationError,UserError

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    # street = fields.Char(string="Adresse", required=True)
    # zip = fields.Char(string="Code postal", size=5, required=True)
    # accounting_contact_name = fields.Char(string="Point de contact du service comptable", required=True)
    iban = fields.Char(string="IBAN", required=True)
    bic = fields.Char(string="BIC", required=True)
    # account_number = fields.Char(string="Numéro de compte", required=True)
    payment_method = fields.Char(string="Mode de règlement", required=True)
    service_description = fields.Text(string="Description du type de prestation fourni", required=True)
    # attachment_filename = fields.Binary(string="Attachment Filename")
    # department = fields.Char(string="Département (Centre de coûts)", required=True)
    # siret = fields.Char(string="Numéro de SIRET", required=True)
    # vat_registered = fields.Selection([('yes', 'Oui'), ('no', 'Non')], string="Immatriculée à la TVA", required=True)
    # vat_number = fields.Char(string="Numero de TVA", required=True)