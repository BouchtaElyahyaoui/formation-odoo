{
    'name': 'Instance Request Module',
    'author': 'Bouchta Elyahyaoui',
    'website': 'www.odoo.com',
    'summary': 'This is our fist sumary',
    'depends': ['mail'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/instance_request.xml',
        'views/odoo_version.xml',
        'data/data.xml',
        'data/mail_template.xml'
    ]
}
