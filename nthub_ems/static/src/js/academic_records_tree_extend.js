/** @odoo-module */
import { ListController } from "@web/views/list/list_controller";
import { registry } from '@web/core/registry';
import { listView } from '@web/views/list/list_view';

export class AcademicRecordsListController extends ListController {
   setup() {
       super.setup();
   }

   OnClick() {
       this.actionService.doAction({
          type: 'ir.actions.act_window',
          res_model: 'multiple.academic.records',
          name:'Classes Distribution',
          view_mode: 'form',
          view_type: 'form',
          views: [[false, 'form']],
          target: 'new',
          res_id: false,
      });
   }

   OnClickCommittees() {
       this.actionService.doAction({
          type: 'ir.actions.act_window',
          res_model: 'multiple.academic.records',
          name:'Committees Distribution',
          view_mode: 'form',
          view_type: 'form',
          views: [[false, 'form']],
          target: 'new',
          res_id: false,
          context: '{"default_is_committees": True}'
      });
   }
}

registry.category("views").add("button_academic_in_tree", {
   ...listView,
   Controller: AcademicRecordsListController,

   buttonTemplate: "button_academic.ListView.Buttons",
});


