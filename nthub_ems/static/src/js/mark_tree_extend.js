/** @odoo-module */
import { ListController } from "@web/views/list/list_controller";
import { registry } from '@web/core/registry';
import { listView } from '@web/views/list/list_view';

export class MarkListController extends ListController {
   setup() {
       super.setup();
   }

   //   that name xml js
   OnTestClick() {
       this.actionService.doAction({
          type: 'ir.actions.act_window',
          res_model: 'multiple.marks',
          name:'Generate Subject',
          view_mode: 'form',
          view_type: 'form',
          views: [[false, 'form']],
          target: 'new',
          res_id: false,
      });
   }
}
//add name in the tree in view model  dont forget it add("button_academic_in_tree"
registry.category("views").add("button_in_tree", {
   ...listView,
   Controller: MarkListController,
   //   that name xml js
   buttonTemplate: "button_mark.ListView.Buttons",
});

