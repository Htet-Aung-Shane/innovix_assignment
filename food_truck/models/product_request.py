from odoo import models, fields, api, _
import datetime
from datetime import date, timedelta


class ProductRequest(models.Model):
    _name = "innovix.product.request"
    _description = "Products Request Developed By Htet Aung Shane"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    product_id = fields.Many2one(
        "product.template",
        string="Product",
        tracking=True,
        index=True,
    )
    quantity = fields.Float(
        "Requested Quantity",
        tracking=True,
        index=True,
    )
    created_date = fields.Datetime("Created Date", default=fields.Datetime.now)
    requested_user = fields.Many2one("res.partner", string="Requested User")
    active = fields.Boolean(default=True)

    @api.model
    def create(self, vals):
        vals["requested_user"] = self.env.user.partner_id.id
        return super(ProductRequest, self).create(vals)
