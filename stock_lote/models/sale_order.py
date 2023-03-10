# -*- coding: utf-8 -*-

from odoo import fields, models
from dateutil.relativedelta import relativedelta


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _get_reward_line_values(self, program):
        self.ensure_one()
        self = self.with_context(lang=self.partner_id.lang, program=program)
        program = program.with_context(lang=self.partner_id.lang)
        if program.reward_type == 'discount':
            return self._get_reward_values_discount(program)
        elif program.reward_type == 'product':
            return [self._get_reward_values_product(program)]

    def _get_paid_order_lines(self):
        program = self.env.context.get('program')
        sale_order_lines = super(SaleOrder, self)._get_paid_order_lines()
        if program and program.rule_expiration_date:
            now = fields.Datetime.now()
            dt_from = now + relativedelta(months=program.rule_expiration_from)
            dt_to = now + relativedelta(months=program.rule_expiration_to)
            sale_order_lines = sale_order_lines.filtered(lambda line: line.lot_id and dt_from <= line.lot_id.expiration_date < dt_to)

        return sale_order_lines
