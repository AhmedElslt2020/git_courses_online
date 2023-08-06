from email.policy import default


from odoo import models, fields, api, tools


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    confirmed_user_id = fields.Many2one('res.users')
    my_field = fields.Char()
    # origin = fields.Char(default='sad') this is field in odoo want to make default






    def action_confirm(self):
        super(SaleOrder,self).action_confirm()
        self.confirmed_user_id = self.env.user.id

        print("equaliiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii",self.confirmed_user_id.name)


    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder,self)._prepare_invoice()
        invoice_vals['so_confirmed_user_id'] = self.confirmed_user_id.id

        return invoice_vals



    # @api.model
    # def create(self, vals):
    #     # print("odoo mates",vals)
    #     vals['origin'] = "ahmed"
    #     print("odoo mates",vals)
    #
    #     return super(SaleOrder, self).create(vals)

