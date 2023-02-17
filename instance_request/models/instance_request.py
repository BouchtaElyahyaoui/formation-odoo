# -*- coding: utf-8 -*-
from odoo import api, fields, models


class InstanceRequest(models.Model):
    _name = "instance.request"  # odoo will create a postgres table (hospital_patient
    _description = "All instance requests"
    name = fields.Char(string='Designation')
    address_ip = fields.Char(string='IP Address')
    active = fields.Boolean(string='Actif', default=True)
    cpu = fields.Char(string='CPU')
    ram = fields.Char(string='RAM')
    disk = fields.Char(string='DISK')
    url = fields.Char(string='URL')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submited', 'Submited'),
        ('inprogress', 'In Progress'),
        ('done', 'Done')
    ], string='Statut'
        , default="draft")
    limit_date = fields.Date(string='Processing Deadline')
    treat_date = fields.Date(string='Processing Date')
    treat_duration = fields.Float(string='Processing Period')


    def action_brouillon(self):
        for record in self:
            record.state = 'draft'

    def action_soumise(self):
        for record in self:
            record.state = 'submited'

    def action_en_traitement(self):
        for record in self:
            record.state = 'inprogress'

    def action_traitée(self):
        for record in self:
            record.state = 'done'
