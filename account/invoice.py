# -*- coding: utf-8 -*-
##############################################################################
#    
#    Copyright (C) 2015
#    Francesco OpenCode Apruzzese (<f.apruzzese@andreacometa.it>)
#    All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
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


from osv import fields, osv


class account_invoice_line(osv.osv):

    _inherit = "account.invoice.line"

    _columns = {
        'pricelist_discount1': fields.float('Discount 1'),
        'pricelist_discount2': fields.float('Discount 2'),
        'pricelist_discount3': fields.float('Discount 3'),
    }
    _defaults = {
        'pricelist_discount1': 0.0,
        'pricelist_discount2': 0.0,
        'pricelist_discount3': 0.0,
    }

    def discounts_change(self, cr, uid, ids, d1, d2, d3, context=None):
        res = {'value': {'discount': 0.0}}
        discount = 100.00
        for dis in [d1, d2, d3]:
            discount -= discount * (dis/100.00)
        discount = 100.00 - discount
        res['value']['discount'] = discount
        return res
