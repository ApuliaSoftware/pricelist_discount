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
from datetime import date, datetime, time, timedelta


class product_pricelist_item(models.Model):
    _inherit = "product.pricelist.item"

    discount1 = fields.Float(string='Discount 1', default = 0.0)
    discount2 = fields.Float(string='Discount 2', default = 0.0)
    discount3 = fields.Float(string='Discount 3', default = 0.0)

    @api.one
    def get_right_item(self, partner, pricelist_id, product_id, qty):
        # ----- Init item (return it)
        item = False

        # ----- Get date
        date = self._context.get('date') or fields.Date.context_today(self)

        # ----- Recursive function to create categories list
        # ----------------------------------------------------------------------
        # ----------------------------------------------------------------------
        def _create_parent_category_list(id, lst):
            if not id:
                return []
            parent = product_category_tree.get(id)
            if parent:
                lst.append(parent)
                return _create_parent_category_list(parent, lst)
            else:
                return lst
        # ----------------------------------------------------------------------
        # ----------------------------------------------------------------------

        # ----- Product info
        product_obj = self.pool['product.product']
        product_category_obj = self.pool['product.category']
        product_ids = [product_id, ]
        products = product_obj.browse(self._cr, self._uid, product_ids, context=self._context)
        products_dict = dict([(item.id, item) for item in products])
        tmpl_id = products_dict[product_id].product_tmpl_id and \
            products_dict[product_id].product_tmpl_id.id or False
        product_category_ids = product_category_obj.search(self._cr, self._uid, [])
        product_categories = product_category_obj.read(
            self._cr, self._uid, product_category_ids, ['parent_id'])
        product_category_tree = dict(
            [(item['id'], item['parent_id'][0])
             for item in product_categories if item['parent_id']])
        categ_id = products_dict[product_id].categ_id and \
            products_dict[product_id].categ_id.id or False
        categ_ids = _create_parent_category_list(categ_id, [categ_id])
        if categ_ids:
            categ_where = '(categ_id IN (' + ','.join(map(str, categ_ids)) + '))'
        else:
            categ_where = '(categ_id IS NULL)'
        # ----- Partner info
        if partner:
            partner_where = 'base <> -2 OR %s IN (SELECT name FROM product_supplierinfo WHERE product_id = %s) '
            partner_args = (partner, tmpl_id)
        else:
            partner_where = 'base <> -2 '
            partner_args = ()
        # ----- Pricelist info
        pricelist_ids = pricelist_id and [pricelist_id] or []
        if not pricelist_ids:
            pricelist_ids = self.pool['product.pricelist'].search(
                self._cr, self._uid, [], context=self._context)
        pricelist_version_ids = self.pool['product.pricelist.version'].search(
            self._cr, self._uid, [('pricelist_id', 'in', pricelist_ids),
                      '|',
                      ('date_start', '=', False),
                      ('date_start', '<=', date),
                      '|',
                      ('date_end', '=', False),
                      ('date_end', '>=', date),
                      ])
        if len(pricelist_ids) != len(pricelist_version_ids):
            return item
        # ----- Now we can search the value!
        self._cr.execute(
            'SELECT i.id '
            'FROM product_pricelist_item AS i, '
                'product_pricelist_version AS v, product_pricelist AS pl '
            'WHERE (product_tmpl_id IS NULL OR product_tmpl_id = %s) '
                'AND (product_id IS NULL OR product_id = %s) '
                'AND (' + categ_where + ' OR (categ_id IS NULL)) '
                'AND (' + partner_where + ') '
                'AND price_version_id = %s '
                'AND (min_quantity IS NULL OR min_quantity <= %s) '
                'AND i.price_version_id = v.id AND v.pricelist_id = pl.id '
            'ORDER BY sequence',
            (tmpl_id, product_id) + partner_args + (pricelist_version_ids[0],
                                                    qty))
        query_res = self._cr.dictfetchall()
        if query_res:
            item = query_res[0]['id']
        return item
