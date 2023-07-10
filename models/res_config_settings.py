# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    group_product_tolerance = fields.Boolean("Manage tolerance in qty transferred per products", implied_group='product_tolerance.group_product_tolerance')
