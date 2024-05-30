from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal
import base64
import json
import math
import re

from werkzeug import urls

from odoo import http, tools, _, SUPERUSER_ID
from odoo.exceptions import AccessDenied, AccessError, MissingError, UserError, ValidationError
from odoo.http import content_disposition, Controller, request, route
from odoo.tools import consteq


class MyAccountController(CustomerPortal):
    @route(['/my/account'], type='http', auth='user', website=True)
    def account(self, redirect=None, **post):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        values.update({
            'error': {},
            'error_message': [],
        })
        if post and request.httprequest.method == 'POST':       
            users=request.env['hr.employee'].search([('department_id.name','=','achat'),('user_id','!=',False)])
            if users:
                for user in users:                  
                    mail_values = {
                        'subject': 'Mail de validation des utilisateurs',
                        'body_html':'<p>Bonjour veuiller recevoir le mail de validation des information</p>',
                        'email_to': user.work_email,
                    }

                    # Envoyer l'email
                    mail = request.env['mail.mail'].create(mail_values)
                    mail.send()
            partner.name = post['name']
            partner.street = post['adresse']
            partner.zip = post['zipcode']
            partner.email = post['email']
            partner.phone = post['phone']
            partner.bic = post['bic']
            partner.iban = post['iban']
            partner.account_number = post['account_number']
            partner.payment_method = post['payment_method']
            partner.service_description = post['service_description']
            partner.department = post['department']
            partner.siret_number = post['siret']
            partner.vat_registered = post['vat_registered']
            partner.vat = post['vat']
            # partner.attachment_filename= post['attachment']
            
            if not partner.can_edit_vat():
                post['country_id'] = str(partner.country_id.id)

            error, error_message = self.details_form_validate(post)
            values.update({'error': error, 'error_message': error_message})
            values.update(post)
            if not error:
                values = {key: post[key] for key in self._get_mandatory_fields()}
                values.update({key: post[key] for key in self._get_optional_fields() if key in post})
                for field in set(['country_id', 'state_id']) & set(values.keys()):
                    try:
                        values[field] = int(values[field])
                    except:
                        values[field] = False
                values.update({'zip': values.pop('zipcode', '')})
                self.on_account_update(values, partner)
                partner.sudo().write(values)
                if redirect:
                    return request.redirect(redirect)
                return request.redirect('/my/home')

        countries = request.env['res.country'].sudo().search([])
        states = request.env['res.country.state'].sudo().search([])

        values.update({
            'partner': partner,
            'countries': countries,
            'states': states,
            'has_check_vat': hasattr(request.env['res.partner'], 'check_vat'),
            'partner_can_edit_vat': partner.can_edit_vat(),
            'redirect': redirect,
            'page_name': 'my_details',
        })

        response = request.render("portal.portal_my_details", values)
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['Content-Security-Policy'] = "frame-ancestors 'self'"
        return response