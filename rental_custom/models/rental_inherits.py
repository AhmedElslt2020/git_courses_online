from odoo import models, fields, api, tools


class RentalInherits(models.Model):
    _inherit = "sale.rental.report"

    ref = fields.Char(string='Reference')
    # by ahmed gamal
    # override _select to add a new field
    def _select(self):
        return """
            sol.id,
            sol.order_id,
            sol.product_id,
            %s,
            sol.product_uom,
            sol.order_partner_id AS partner_id,
            rp.ref as ref,
            sol.salesman_id AS user_id,
            pt.categ_id,
            p.product_tmpl_id,
            generate_series(sol.pickup_date::date, sol.return_date::date, '1 day'::interval)::date date,
            %s AS price,
            sol.company_id,
            sol.state,
            sol.currency_id
        """ % (self._quantity(), self._price())

    # By Ahmed Gamel
    # Override _from to add new relation with sol
    def _from(self):
        return """
            sale_order_line AS sol
            join res_partner AS rp on rp.id = sol.order_partner_id
            join product_product AS p on p.id=sol.product_id
            join product_template AS pt on p.product_tmpl_id=pt.id
            join uom_uom AS u on u.id=sol.product_uom
            join uom_uom AS u2 on u2.id=pt.uom_id
        """
