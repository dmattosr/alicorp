# -*- coding: utf-8 -*-

from odoo import api, fields, models


class CouponProgram(models.Model):
    _inherit = 'coupon.program'

    rule_expiration = fields.Boolean('Vencimiento de lote')
    rule_expiration_from = fields.Integer('Mes Inicio')
    rule_expiration_to = fields.Integer('Mes Final')

    @api.onchange('rule_expiration_from')
    def _onchange_rule_expiration_from(self):
        if self.rule_expiration_from < 0:
            self.rule_expiration_from = False
            return {'warning': {
                'title': 'Cuidado',
                'message': 'El valor de "Mes Inicio" es incorrecto'
            }}

        if self.rule_expiration_from > self.rule_expiration_to:
            self.rule_expiration_to = self.rule_expiration_from + 1

    @api.onchange('rule_expiration_to')
    def _onchange_rule_expiration_to(self):
        if self.rule_expiration_to < 0:
            self.rule_expiration_to = False
            return {'warning': {
                'title': 'Cuidado',
                'message': 'El valor de "Mes Final" es incorrecto'
            }}

        if self.rule_expiration_from > self.rule_expiration_to:
            self.rule_expiration_from = max(0, self.rule_expiration_to - 1)

    def _keep_only_most_interesting_auto_applied_global_discount_program(self):
        expiration = self.filtered(lambda program: program.rule_expiration)
        others = self - expiration
        others = super(CouponProgram, others)._keep_only_most_interesting_auto_applied_global_discount_program()
        return self.search([('id', 'in', expiration.ids + others.ids)])
