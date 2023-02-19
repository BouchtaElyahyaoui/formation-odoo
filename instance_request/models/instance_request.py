# -*- coding: utf-8 -*-
from odoo import api, fields, models


class InstanceRequest(models.Model):
    _name = "instance.request"  # odoo will create a postgres table (hospital_patient
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "All instance requests"
    name = fields.Char(string='Designation',tracking=True)
    address_ip = fields.Char(string='IP Address')
    active = fields.Boolean(string='Actif', default=True)
    cpu = fields.Char(string='CPU',)
    ram = fields.Char(string='RAM')
    disk = fields.Char(string='DISK')
    url = fields.Char(string='URL')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submited', 'Submited'),
        ('inprogress', 'In Progress'),
        ('done', 'Done')
    ], string='Statut'
        , default="draft",tracking=True)
    limit_date = fields.Date(string='Processing Deadline',tracking=True)
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
            template = self.env.ref("instance_request.instance_request_creation_progress")
            template.send_mail(record.id,
                               email_values={'email_to': record.create_uid.email, 'email_from': self.env.user.email})



    def action_traitée(self):
        for record in self:
            record.state = 'done'
            template = self.env.ref("instance_request.instance_request_creation")
            template.send_mail(record.id,
                               email_values={'email_to': record.create_uid.email, 'email_from': self.env.user.email})
