# -*- coding: utf-8 -*- 

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare, float_is_zero, float_round


class ProductTemplate(models.Model):
    _inherit = "product.template"

    tolerance_line_ids = fields.One2many('product.template.tolerance.line', 'product_id')

    def _check_tolerance(self, picking_type_id, ordred_qty, qty_done, uom=False):
        self.ensure_one()
        if float_compare(qty_done, ordred_qty, precision_rounding=uom and uom.rounding or self.uom_id.rounding) > 0:
            tolerance_line = self.tolerance_line_ids.filtered(lambda ln: ln.picking_type_id.id == picking_type_id)
            if not tolerance_line:
                return
            diff_ratio_rate = ((qty_done - ordred_qty) / ordred_qty) * 100
            precision_rounding = self.env.company.tolerance_precision and 1/(10**self.env.company.tolerance_precision) or 1/(10**2)
            if float_compare(diff_ratio_rate, tolerance_line[0].tolerance_ratio,
                             precision_rounding=precision_rounding) > 0:
                raise UserError(_("You have exceeded the tolerance (%s%s) of the product %s !")%(
                        int(tolerance_line[0].tolerance_ratio),'%', self.display_name))


class ProductTemplateToleranceLine(models.Model):
    _name = 'product.template.tolerance.line'

    product_id = fields.Many2one('product.template', string='Product', required=False, ondelete='cascade')
    picking_type_id = fields.Many2one('stock.picking.type', string='Operation', required=True)
    tolerance_ratio = fields.Float(string='Tolerance %', default=0.0)
