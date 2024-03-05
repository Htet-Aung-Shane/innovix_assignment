from odoo import models, fields, api, _
import datetime
from datetime import date, timedelta
from random import randint
from odoo.exceptions import UserError

class ProductSet(models.Model):
    _name = "innovix.product.set"
    _description = "Products Set Developed By Htet Aung Shane"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    def _get_default_color(self):
        return randint(1, 11)
    
    no = fields.Char (
        'Set Number', size=16, copy=False,
        readonly=True, store=True,
        tracking=True,
        index=True,
        default=lambda self:
        self.env['ir.sequence'].next_by_code('innovix.product.set')) 
    name = fields.Char('Name')
    image = fields.Binary()
    color = fields.Integer(string='Color', default=_get_default_color)
    active = fields.Boolean(default=True)
    product_ids = fields.Many2many('product.template', string="Product Line")
    created_date = fields.Datetime('Created Date',default=fields.Datetime.now)

class SaleExtension(models.Model):
    _inherit ="sale.order"

    innovix_sale_order = fields.Char(
        'Innovix Sale Order', size=20, copy=False,
        readonly=True, store=True,
        tracking=True,
        index=True,
        inverse="_inverse_innovix_sale_order",
        default=lambda self:
        self.env['ir.sequence'].next_by_code('innovix.sale.order'))
    
    set_id = fields.Many2one('innovix.product.set', string="Product Set", inverse="_inverse_set_id")

    @api.onchange('set_id')
    def _inverse_set_id(self):
        if self.set_id:
            product_lines = []
            for product in self.set_id.product_ids:
                product_lines.append((0, 0, {
                    'product_id': product.id,
                    'name': product.name,
                    'price_unit': product.list_price
                }))
            # if self.order_line:
            #     self.order_line.unlink()  # Comment this code since we use onchange and have to take more time
            self.order_line = product_lines

    @api.depends('innovix_sale_order')
    def _inverse_innovix_sale_order(self):
        if self.innovix_sale_order:
            self.name = self.innovix_sale_order

    def action_confirm(self):
        super(SaleExtension, self).action_confirm()
        for order in self:
            order.partner_id.spend_amount += order.amount_total
            print('hello spent ammount>>>',order.partner_id.spend_amount)
            if order.partner_id.spend_amount >= 50000:
                order._generate_free_food_set_invoice()

    def action_cancel(self):
        super(SaleExtension, self).action_cancel()
        for order in self:
            order.partner_id.spend_amount -= order.amount_total
            print('hello spent ammount>>>',order.partner_id.spend_amount)

    def _generate_free_food_set_invoice(self):
        print('generate free')
        free_food_set = self.env['innovix.product.set'].search([('name', '=', 'Free Food Set')])
        if not free_food_set:
            raise UserError(_("Product Set (Free Food Set) does not exist yet. Please create first "))
        product_lines = []
        for product in free_food_set.product_ids:            
            product_lines.append((0, 0, {
                'product_id': product.id,
                'name': product.name,
                'price_unit': 0.0,  
            }))
        invoice_vals = {
            'partner_id': self.partner_id.id,
            'invoice_line_ids': product_lines,
            'move_type': 'out_invoice',  # Customer invoice
        }
        invoice = self.env['account.move'].create(invoice_vals)
        # Confirm the invoice
        invoice.action_post()


class CustomerExtension(models.Model):
    _inherit ="res.partner"

    spend_amount = fields.Float(string="Total Spend Amount")