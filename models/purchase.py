from odoo import models ,api ,fields,exceptions
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
    

   