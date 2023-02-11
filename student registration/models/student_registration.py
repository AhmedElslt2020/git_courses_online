from datetime import date
from odoo import models, fields, api
from datetime import datetime


class StudentRegistration(models.Model):
    _name = "student.registration"

    name = fields.Char(string="Name", readonly=True)
    student_id = fields.Many2one("res.partner", domain="[('is_student','=',True)]")
    phone = fields.Char(related="student_id.phone")
    check_box = fields.Boolean()
    date = fields.Date(required=True)
    age = fields.Integer(compute='calc_age_student', store=True)
    date = fields.Date(required=True)
    amounte = fields.Monetary(currency_field="currency_id")
    amount = fields.Monetary('Amount', required=True)
    currency_id = fields.Many2one("res.currency", related="company_id.currency_id")
    company_id = fields.Many2one("res.company")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('invoiced', 'Invoiced'),
        ('canceled', 'Canceled'),

    ], default="draft")
    customer_invoice_ids = fields.Many2many('account.move')
    count_invoices = fields.Integer("Count Invoices", compute="_compute_count_invoices")

    @api.depends('customer_invoice_ids')
    def _compute_count_invoices(self):
        for request in self:
            request.count_invoices = len(request.customer_invoice_ids)

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('student.registration')
        return super(StudentRegistration, self).create(vals)

    # @api.onchange("student_id")
    # def depend_student_id(self):
    #     for record in self:
    #        if record.student_id:
    #            record.check_box = True
    #        else:
    #            record.check_box = False

    # @api.onchange("student_id")
    # def depend_students_id(self):
    #     self.phone = self.student_id.phone

    # @api.depends('date')
    # def calc_age_student(self):
    #     for rec in self:
    #        today = date.today()
    #        if rec.date:
    #            rec.age = today.year - rec.date.year
    #        else:
    #            rec.age = 1

    @api.depends('student_id.birth_date')
    def calc_age_student(self):
        for rec in self:
            today = date.today()
            if rec.student_id.birth_date:
                rec.age = today.year - rec.student_id.birth_date.year
            else:
                rec.age = 1

    def change_state(self):
        if self.state == 'draft':
            self.state = 'confirmed'
        elif self.state == 'confirmed':
            self.state = 'invoiced'

    def change_cancel(self):
        if self.state in ['draft', 'confirmed', 'invoiced']:
            self.state = 'canceled'

    #new invoice

    def view_invoices(self):
        """Action view for invoices of a customer"""
        self.ensure_one()
        result = {
            "type": "ir.actions.act_window",
            "res_model": "account.move",
            "domain": [('id', 'in', self.customer_invoice_ids.ids),
                       ('move_type', 'in', self.env['account.move'].get_sale_types())],
            "context": {"create": False},
            "name": "Customer Invoices",
            'view_mode': 'tree,form',
        }
        return result

    def prepare_customer_invoice(self):
        """Prepares customer invoices based on lines on request"""
        customer_invoice = self.env['account.move']
        invoice_lines = []
        student_serice = self.env.ref('knowledge_bi.product_student_reg_service')
        invoice_lines.append((0, 0, {
            'name': student_serice.name,
            'display_name': student_serice.name,
            'price_unit': self.amount,
            'quantity': 1,
            'product_id': student_serice.id or False,
        }))

        customer_bill_vals = {
            'invoice_date': datetime.now().date(),
            'move_type': 'out_invoice',
            'state': 'draft',
            'partner_id': self.student_id.id,
            'invoice_line_ids': invoice_lines,
        }
        customer_invoice += self.env['account.move'].create(customer_bill_vals)
        return customer_invoice

    def action_create_invoice(self):
        """Create a new invoice"""
        customer_invoice = self.prepare_customer_invoice()
        if customer_invoice:
            self.customer_invoice_ids = [(6, 0, customer_invoice.ids)]





