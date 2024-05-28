
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
        
      
   
    @api.model
    def create(self,vals):
        results = super(PurchaseOrderExt, self).create(vals)
        if results:
            if results.partner_id:
                partner_id = results.partner_id
                if partner_id.email:
                    user =  self.env['res.users'].search([('login','=',partner_id.email)])
                    if not user:
                         
                        new_user= self.env['res.users'].create({
                            "name":partner_id.name,
                            "login": partner_id.email,
                            "sel_groups_1_10_11":10,
                            'email':partner_id.email,
                            'partner_id':partner_id.id
                        
                        })
                        
                        new_user.reset_password(new_user.login)
      
        return results
    

     
    @api.model
    def write(self,vals):
        results = super(PurchaseOrderExt, self).create(vals)
        if results:
            if results.partner_id:
                partner_id = results.partner_id
                if partner_id.email:
                    user =  self.env['res.users'].search([('login','=',partner_id.email)])
                    if not user:
                         
                        new_user= self.env['res.users'].create({
                            "name":partner_id.name,
                            "login": partner_id.email,
                            "sel_groups_1_10_11":10,
                            'email':partner_id.email,
                            'partner_id':partner_id.id
                        
                        })
                        
                        new_user.reset_password(new_user.login)
      
        return results
    


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
    
