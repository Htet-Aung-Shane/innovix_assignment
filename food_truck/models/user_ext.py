from odoo import  fields,models,api

class InheritUser(models.Model):
    _inherit='res.users'

    user_type = fields.Selection([('chef',"Chef"),('manager',"Manager")])