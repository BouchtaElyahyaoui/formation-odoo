# -*- coding: utf-8 -*-
from odoo import api, fields, models


class HrEmployee(models.Model):
    _name = "hr.employee"
    _description = "Hr employee"
    _inherit = 'hr.employee'
    instances_ids = fields.Many2one('instance.request', string="Instances")

