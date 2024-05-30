from odoo import models, fields, api , _
from odoo.exceptions import ValidationError,UserError

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    iban = fields.Char(string="IBAN")
    bic = fields.Char(string="BIC")
    account_number = fields.Char(string="Numéro de compte")
    payment_method = fields.Char(string="Mode de règlement")
    service_description = fields.Text(string="Description du type de prestation fourni")
    department = fields.Char(string="Département (Centre de coûts)")
    siret_number = fields.Char(string="Numéro de SIRET")
    vat_registered = fields.Boolean(string="Immatriculée à la TVA")
    attachment_filename = fields.Binary(string="Attachment Filename")