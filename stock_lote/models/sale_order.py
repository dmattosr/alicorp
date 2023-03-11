# -*- coding: utf-8 -*-

from odoo import fields, models
from dateutil.relativedelta import relativedelta


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _get_reward_line_values(self, program):
        self = self.with_context(program=program)
        return super(SaleOrder, self)._get_reward_line_values(program)

    def _get_paid_order_lines(self):
        program = self.env.context.get('program')
        sale_order_lines = super(SaleOrder, self)._get_paid_order_lines()
        if program:
            if program.rule_expiration:
                now = fields.Datetime.now()
                dt_from = now + relativedelta(months=program.rule_expiration_from)
                dt_to = now + relativedelta(months=program.rule_expiration_to)
                sale_order_lines = sale_order_lines.filtered(lambda line: line.lot_id and dt_from <= line.lot_id.expiration_date < dt_to)
            else:
                sale_order_lines = sale_order_lines.filtered(lambda line: not line.lot_id)
        return sale_order_lines

    def _create_new_no_code_promo_reward_lines(self):
        '''Apply new programs that are applicable (is copy)'''
        self.ensure_one()
        order = self
        programs = order._get_applicable_no_code_promo_program()
        programs = programs._keep_only_most_interesting_auto_applied_global_discount_program()
        for program in programs:
            values = True
            if program.promo_applicability == 'on_next_order':
                order.state != 'cancel' and order._create_reward_coupon(program)
            elif program.discount_line_product_id.id not in self.order_line.mapped('product_id').ids:
                values = self._get_reward_line_values(program)
                if values:
                    self.write({'order_line': [(0, False, value) for value in values]})
            if values:
                order.no_code_promo_program_ids |= program
