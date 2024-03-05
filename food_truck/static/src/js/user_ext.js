import { registry } from "@web/core/registry";
import { menuService } from "@web/webclient/menus/menu_service";

registry.category("menu").add("my_menu", {
    async start(env) {
        // Check user role or permissions
        // const userType = await env.services.session.user_context.user_type;
        menuService.addMenuItemClass("menu_sale", "d-none");
        // If user is a chef, hide the Sale menu
        // if (userType === "chef") {
        //     menuService.addMenuItemClass("menu_sale", "d-none"); // Use the correct menu item ID or class
        // }
    },
});
