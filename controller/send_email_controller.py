# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import base64
from collections import OrderedDict
from datetime import datetime

from odoo import http
from odoo.exceptions import AccessError, MissingError
from odoo.http import request, Response
from odoo.tools import image_process
from odoo.tools.translate import _
from odoo.addons.portal.controllers import portal
from odoo.addons.portal.controllers.portal import pager as portal_pager


class send_email(portal.CustomerPortal):
    
    @http.route(['/my/purchase/<int:order_id>'], type='http', auth="public", website=True)
    def portal_my_purchase_order(self, order_id=None, access_token=None, **kw):
        try:
            order_sudo = self._document_check_access('purchase.order', order_id, access_token=access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')

        report_type = kw.get('report_type')
        if report_type in ('html', 'pdf', 'text'):
            return self._show_report(model=order_sudo, report_type=report_type, report_ref='purchase.action_report_purchase_order', download=kw.get('download'))

        confirm_type = kw.get('confirm')
        if confirm_type == 'reminder':
            order_sudo.confirm_reminder_mail(kw.get('confirmed_date'))
        if confirm_type == 'reception':
            order_sudo._confirm_reception_mail()

        values = self._purchase_order_get_page_view_values(order_sudo, access_token, **kw)
        update_date = kw.get('update')
        if order_sudo.company_id:
            values['res_company'] = order_sudo.company_id
        if update_date == 'True':
            return request.render("purchase.portal_my_purchase_order_update_date", values)
        return request.render("projet_demo.portal_my_purchase_order1", values)
    


    @http.route('/my/proposistiondate', type='http', auth="public",website=True)
    def test(self, redirect=None, **post):
        if post and request.httprequest.method == 'POST':
            po =request.env['purchase.order'].search([('id','=',post['po_id'])])
            date_proposition =post['date']
            date_proposition = date_proposition.replace('T',' ')
            date_ = datetime.strptime(date_proposition,'%Y-%m-%d %H:%M')
            po.date_planned = date_
        return request.render('projet_demo.template_date_valider')