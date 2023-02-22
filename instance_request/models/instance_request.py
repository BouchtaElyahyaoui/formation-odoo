# -*- coding: utf-8 -*-
import datetime

from odoo import api, fields, models
from odoo.exceptions import UserError


class InstanceRequest(models.Model):
    _name = "instance.request"  # odoo will create a postgres table (hospital_patient
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "All instance requests"
    name = fields.Char(string='Designation', tracking=True)
    address_ip = fields.Char(string='IP Address')
    active = fields.Boolean(string='Actif', default=True)
    cpu = fields.Char(string='CPU', )
    ram = fields.Char(string='RAM')
    disk = fields.Char(string='DISK')
    url = fields.Char(string='URL')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submited', 'Submited'),
        ('inprogress', 'In Progress'),
        ('done', 'Done')
    ], string='Statut'
        , default="draft", tracking=True)
    limit_date = fields.Date(string='Processing Deadline', tracking=True)
    treat_date = fields.Date(string='Processing Date')
    treat_duration = fields.Float(compute="_compute_treat_duration", string='Processing Period', store=1)
    partner_id = fields.Many2one('res.partner', string="Partner")
    tl_id = fields.Many2one('hr.employee', string="Employee")
    # tl_user_id = fields.Many2one('hr.employee', string="")
    odoo_id = fields.Many2one('odoo.version', string="Odoo Version")
    perimeters_ids = fields.One2many('perimeter', 'instance_id', string="Perimeters")
    request_line_ids = fields.One2many('hr.employee', 'instances_ids', string="lines")
    nb_lines = fields.Integer(string="Nb lines", compute="_compute_nb_lines")
    perimeters = fields.Integer(compute='_compute_perimeters', string="Number of Perimeters")

    @api.depends('request_line_ids')
    def _compute_nb_lines(self):
        for r in self:
            r.nb_lines = len(r.request_line_ids)

    @api.depends('perimeters_ids')
    def _compute_perimeters(self):
        for r in self:
            print(len(r.perimeters_ids))
            r.perimeters = len(r.perimeters_ids)

    @api.depends('treat_date')
    def _compute_treat_duration(self):
        for r in self:
            if r.treat_date:
                d1 = datetime.datetime.strptime(r.treat_date.strftime("%Y-%m-%d"), "%Y-%m-%d")
                d2 = datetime.datetime.strptime(datetime.datetime.today().strftime("%Y-%m-%d"), "%Y-%m-%d")
                r.treat_duration = abs((d2 - d1).days)

    _sql_constraints = [
        ("uniq_ip_address", "unique(address_ip)", "Address Ip already in use")
    ]

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('instance.request')
        res = super(InstanceRequest, self).create(vals)
        return res

    def write(self, vals):
        print('Write method is being triggered', vals.get('limit_date'))
        if vals.get('limit_date') and type(vals.get('limit_date')) == str:
            if datetime.datetime.strptime(vals.get('limit_date'), '%Y-%m-%d') < datetime.datetime.today():
                raise UserError("You can not choose a date less than today's date !")
            users = self.env.ref('instance_request.group_instance_request_responsable').users
            for user in users:
                self.activity_schedule(
                    'mail.mail_activity_instance_limit_date_changed',
                    user_id=user.id,
                    note='The limit date is assigned to all the users of responsable group',
                    date_deadline=datetime.datetime.strptime(vals.get('limit_date'), '%Y-%m-%d')
                )
        return super(InstanceRequest, self).write(vals)

    def unlink(self):
        if self.state != 'draft':
            raise UserError("You can only delete records in 'draft' state !")
        else:
            return super().unlink()

    def action_brouillon(self):
        for record in self:
            record.state = 'draft'

    def action_soumise(self):
        for record in self:
            record.state = 'submited'
        users = self.env.ref('instance_request.group_instance_request_admin').users
        for user in users:
            self.activity_schedule(
                'mail.mail_activity_instance_created',
                user_id=user.id,
                note='Your instance is being created'
            )

    def action_en_traitement(self):
        for record in self:
            record.state = 'inprogress'
            template = self.env.ref("instance_request.instance_request_creation_progress")
            template.send_mail(record.id,
                               email_values={'email_to': record.create_uid.email, 'email_from': self.env.user.email})

    def action_traitée(self):
        for record in self:
            record.state = 'done'
            record.limit_date = datetime.datetime.today()
            template = self.env.ref("instance_request.instance_request_creation")
            template.send_mail(record.id,
                               email_values={'email_to': record.create_uid.email, 'email_from': self.env.user.email})
