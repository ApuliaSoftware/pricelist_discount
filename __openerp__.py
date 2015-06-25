# -*- coding: utf-8 -*-
##############################################################################
#
# OpenERP, Open Source Management Solution
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

{
    "name": "Pricelist discounts",
    "description": 'Adds discounts to pricelist management',
    "version": "0.1",
    "depends": [
        "sale",
        "account",
        "product",
        ],
    "category": "Sales",
    "author": "Andrea Cometa",
    "url": "http://www.apuliasoftware.it",
    "data": [
        "sale/sale_view.xml",
        "account/invoice_view.xml",
        "pricelist/pricelist_view.xml",
     ],
    "installable": True,
    "auto_install": False,
    "certificate": "",
    'images': [],
}
