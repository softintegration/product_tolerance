# -*- coding: utf-8 -*- 

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare, float_is_zero, float_round


class Company(models.Model):
    _inherit = "res.company"

    tolerance_precision = fields.Integer("Tolerance precision", default=2)