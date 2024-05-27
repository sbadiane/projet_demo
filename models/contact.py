from odoo import models ,api ,fields
class Contacts(models.Model):
    _inherit = "res.partner"
   
    
    @api.model
    def create(self,vals):
     print('tttttttttttttttttttttttttttttt')
     results = super(Contacts, self).create(vals)
     print("pppppppppppppppppp",self.partner_id,self.email)
           
     self.env['res.users'].create({
                     
                    "name":self.partner_id,
                    "login": self.email,
                    
                            
            })
     return results