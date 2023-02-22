# -*- coding: utf-8 -*-
from odoo import api, fields, models


class Perimetr(models.Model):
    _name = "perimeter"
    _description = "Our Perimeters"
    name = fields.Char(string='Name')
    instance_id = fields.Many2one('instance.request', string="Instance Request")


