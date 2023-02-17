# -*- coding: utf-8 -*-
from odoo import api, fields, models


class OdooVersion(models.Model):
    _name = "odoo.version"
    _description = "Odoo Version"
    name = fields.Char(string='Version')
