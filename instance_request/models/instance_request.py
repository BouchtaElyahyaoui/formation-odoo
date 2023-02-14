from odoo import api, fields, models


class InstanceRequest(models.Model):
    _name = "instance.request" # odoo will create a postgres table (hospital_patient
    _description = "All instance requests"
    name = fields.Char(string='Designation')
    address_ip = fields.Char(string='Adresse IP')
    active = fields.Boolean(string='Actif',default=True)
    cpu = fields.Char(string='cpu')
    ram = fields.Char(string='ram')
    disk = fields.Char(string='disk')
    url = fields.Char(string='url')
    state = fields.Selection([
        ('brouillon', 'Brouillon'),
        ('soumise', 'Soumise'),
        ('en traitement', 'En Traitement'),
        ('traitée','Traitée')
    ],string='Statut'
    ,default="brouillon")
    limit_date = fields.Date(string='Date limite de traitement')
    treat_date = fields.Date(string='Date de Traitement')
    treat_duration = fields.Float(string='Durée de traitement')
