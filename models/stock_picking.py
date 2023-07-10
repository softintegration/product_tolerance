# -*- coding: utf-8 -*- 

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare, float_is_zero, float_round


class Picking(models.Model):
    _inherit = "stock.picking"

    def _action_done(self):
        if self.env.user.has_group('product_tolerance.group_product_tolerance'):self._check_tolerance()
        return super(Picking, self)._action_done()

    def _check_tolerance(self):
        for pick in self:
            tolerance_record_domain = [('picking_type_id', '=', pick.picking_type_id.id), (
            'product_id', 'in', pick.move_line_ids.mapped("product_id").mapped("product_tmpl_id").ids)]
            if not self.env['product.template.tolerance.line'].search_count(tolerance_record_domain):
                continue
            # if we are here so we have at least one line that must undergo a tolerance check
            for move in pick.move_lines:
                tolerance_rule = self.env['product.template.tolerance.line'].search([('product_id','=',move.product_id.product_tmpl_id.id),
                                                                                     ('picking_type_id','=',pick.picking_type_id.id)],limit=1)
                if not tolerance_rule:
                    continue
                # we have to consider all the picking done backorders
                # FIXME: can this case happen really (picking not validated with validated backorders)?
                quantity_done = move.quantity_done + sum(backorder_move.quantity_done for backorder_move in pick.backorder_ids.mapped("move_lines")
                                                       if backorder_move.product_id.id == move.product_id.id
                                                       and backorder_move.product_uom.id == move.product_uom.id)
                # we have to consider all the parent pickings
                quantity_done += sum(parent_move.quantity_done for parent_move in pick._parent_pickings().mapped("move_lines")
                                                       if parent_move.product_id.id == move.product_id.id
                                                       and parent_move.product_uom.id == move.product_uom.id)
                ordered_qty = move.product_uom_qty+sum(backorder_move.product_uom_qty for backorder_move in pick.backorder_ids.mapped("move_lines")
                                                       if backorder_move.product_id.id == move.product_id.id
                                                       and backorder_move.product_uom.id == move.product_uom.id)
                ordered_qty += sum(parent_move.product_uom_qty for parent_move in pick._parent_pickings().mapped("move_lines")
                                                       if parent_move.product_id.id == move.product_id.id
                                                       and parent_move.product_uom.id == move.product_uom.id)
                move.product_id.product_tmpl_id._check_tolerance(move.picking_type_id.id,ordered_qty,quantity_done)






            # we have to get all the backorders of this picking



    def _parent_pickings(self):
        self.ensure_one()
        parent_picking = self.backorder_id
        parent_pickings = self.env['stock.picking']
        while parent_picking:
            parent_pickings |= parent_picking
            parent_picking = parent_picking.backorder_id
        return parent_pickings