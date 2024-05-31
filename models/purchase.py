
# -*- encoding: utf-8 -*-
from odoo import models ,api ,fields, _
from datetime import date


class PurchaseOrderExt(models.Model):
    _inherit = "purchase.order"
   
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
    

     
    # @api.model
    # def write(self,vals):
    #     results = super(PurchaseOrderExt, self).create(vals)
    #     if results:
    #         if results.partner_id:
    #             partner_id = results.partner_id
    #             if partner_id.email:
    #                 user =  self.env['res.users'].search([('login','=',partner_id.email)])
    #                 if not user:
                         
    #                     new_user= self.env['res.users'].create({
    #                         "name":partner_id.name,
    #                         "login": partner_id.email,
    #                         "sel_groups_1_10_11":10,
    #                         'email':partner_id.email,
    #                         'partner_id':partner_id.id
                        
    #                     })
                        
    #                     new_user.reset_password(new_user.login)
      
    #     return results
    


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
        ('valider_ddc','Validation du DDC'),
        ('purchase','Bon de commande fournisseur'),
        
    ] ,string="state"
   )
    
    choix_prix_type =fields.Boolean(string="prix ",compute='_compute_prix_type')
    choix_employer = fields.Boolean(string="bool",compute='_compute_departement')

    def _compute_departement(self):
        for rec in self:
            current_user = self.env.user
            employees = self.env['hr.employee'].search([('user_id', '=', current_user.id), ('department_id.name', '=', 'Achats')])
            if employees and rec.state=='valider_ddc':
                rec.choix_employer = True
            else:
                rec.choix_employer =False
    

    ##################################################################
   

    #############################
    def _compute_prix_type(self):
        for rec in self:        
            if rec.amount_total > 2001 and rec.amount_total < 10000 and rec.type_commande == 'opex':
                rec.choix_prix_type =True
            else:
                 rec.choix_prix_type =False

    def button_confirme(self):
        if self:
            self.state='valider_ddc'
    
    def button_confirm(self):
        for order in self:
            if order.state == 'valider_ddc':
                order.write({'state': 'purchase'})
            if order.state not in ['draft', 'sent']:
                continue
            order.order_line._validate_analytic_distribution()
            order._add_supplier_to_product()
            # Deal with double validation process
            if order._approval_allowed():
                order.button_approve()
            else:
                order.write({'state': 'to approve'})
            if order.partner_id not in order.message_partner_ids:
                order.message_subscribe([order.partner_id.id])
        return True
