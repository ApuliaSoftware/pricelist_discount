# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015
#    Andrea Cometa <info@andreacometa.it>
#    WEB (<http://www.andreacometa.it>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


from openerp import models, fields, api, _


class SaleOrderLine(models.Model):

    _inherit = "sale.order.line"

    pricelist_discount1 = fields.Float(string='Discount 1', default = 0.0)
    pricelist_discount2 = fields.Float(string='Discount 2', default = 0.0)
    pricelist_discount3 = fields.Float(string='Discount 3', default = 0.0)

    @api.onchange('pricelist_discount1', 'pricelist_discount2',
                  'pricelist_discount3')
    def discounts_change(self):
        discount = 100.00
        for dis in [self.pricelist_discount1,
                    self.pricelist_discount2,
                    self.pricelist_discount3]:
            discount -= discount * (dis/100.00)
        discount = 100.00 - discount
        self.discount = discount

    @api.onchange('product_id', 'product_uom_qty')
    def product_id_change(
            self, cr, uid, ids, pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
            lang=False, update_tax=True, date_order=False, packaging=False,
            fiscal_position=False, flag=False, order_id=False, context=None):
        res = super(SaleOrderLine, self).product_id_change(
            cr, uid, ids, pricelist, product, qty, uom,
            qty_uos, uos, name, partner_id, lang, update_tax, date_order,
            packaging, fiscal_position, flag, context)

        if not product:
            return res

        # ----- Keep discounts from pricelist item
        pricelist_item = self.pool['product.pricelist'].price_get(
            cr, uid, [pricelist], product, qty, partner_id, context=context)
        res['value'].update({
            'pricelist_discount1': 0.0,
            'pricelist_discount2': 0.0,
            'pricelist_discount3': 0.0,
            })
        item_obj = self.pool['product.pricelist.item']
        item_id = item_obj.get_right_item(
            cr, uid, partner_id, pricelist, product, qty, context=context)
        if item_id:
            item = item_obj.browse(cr, uid, item_id, context)
            discount = 100.00
            for dis in [item.discount1, item.discount2, item.discount3]:
                discount -= discount * (dis/100.00)
            discount = 100.00 - discount
            res['value'].update({
                'pricelist_discount1': item.discount1,
                'pricelist_discount2': item.discount2,
                'pricelist_discount3': item.discount3,
                'discount': discount,
                })
        return res

    def _prepare_order_line_invoice_line(self, cr, uid, line, account_id=False,
                                         context=None):
        res = super(SaleOrderLine, self)._prepare_order_line_invoice_line(
            cr, uid, line, account_id, context)
        if res:
            # ----- Copy discount keep from pricelist item
            res.update({
                'pricelist_discount1': line.pricelist_discount1,
                'pricelist_discount2': line.pricelist_discount2,
                'pricelist_discount3': line.pricelist_discount3,
                })
        return res
