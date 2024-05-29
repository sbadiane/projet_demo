# -*- encoding: utf-8 -*-
from odoo import models ,api ,fields, _

class Employer(models.Model):
    _inherit ="hr.employee"

    choix_employer = fields.Boolean(string="bool",compute='_compute_departement',default =False)
    

    def _compute_departement(self):
        if self:
            for rec in self:
                current_user = self.env.user
                employees = self.env['hr.employee'].search([('user_id', '=', current_user.id), ('department_id.name', '=', 'Achats')])
                if employees:
                    rec.choix_employer = True
