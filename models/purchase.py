
# -*- encoding: utf-8 -*-
from odoo import models ,api ,fields, _

class PurchaseOrderExt(models.Model):
    _inherit = "purchase.order"

    # prix = fields.Monetary(string='prix',compute='_compute_prix')

    # def _compute_prix(self):
    #     for rec in self:
    #         if rec.amount_total:
    #             self.prix =rec.amount_total
    #     else:
    #          self.prix = self.prix
        
      


    type_commande = fields.Selection(
        [
            ("opex", "OPEX"),
            ("capex", "CAPEX"),
        ],
        string="Type Commande",
       
     
    )
    state = fields.Selection([
        ('draft','Demande de prix'),
        ('valide','Valider par le fournisseur'),
        ('sent','Envoyé'),
        ('purchase','Bon de commande fournisseur'),
        ('valider_ddc','Validation du DDC')
        
    ] ,string="state"
   )
    