from odoo import models, api, tools


class Menu(models.Model):
    _inherit = 'ir.ui.menu'

    @api.model
    def _visible_menu_ids(self, debug=False):
        print('hello')
        menus = super(Menu, self)._visible_menu_ids(debug)        
        if self.env.user.hide_menu_access_ids:
            for rec in self.env.user.hide_menu_access_ids:
                print('menu>>>',rec.id)
                inventory_menu_id = self.env.ref('stock.menu_stock_root').id
                print('inventory menu>>>',inventory_menu_id)
                menus.discard(rec.id)
            return menus
        return menus
