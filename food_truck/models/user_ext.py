from odoo import  fields,models,api

class InheritUser(models.Model):
    _inherit='res.users'

    user_type = fields.Selection([('chef',"Chef"),('manager',"Manager")], default='manager', inverse="_inverse_user_type")

    hide_menu_access_ids = fields.Many2many('ir.ui.menu', 'ir_ui_hide_menu_rel', 'uid', 'menu_id',
                                            string='Hide Access Menu')
    @api.depends('user_type')
    def _inverse_user_type(self):
        if self.user_type == 'chef':
            self._add_chef_menus()
        else:
            self.hide_menu_access_ids=[(5,0,0)]
    def _add_chef_menus(self):
        # Get menu IDs for Sale, Inventory, and Purchase menus
        sale_menu_id = self.env.ref('sale.sale_menu_root').id
        inventory_menu_id = self.env.ref('stock.menu_stock_root').id
        purchase_menu_id = self.env.ref('purchase.menu_purchase_root').id

        # Add menu IDs to hide_menu_access_ids
        self.hide_menu_access_ids = [(4, menu_id) for menu_id in [sale_menu_id, inventory_menu_id, purchase_menu_id]]