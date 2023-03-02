from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    lot_id = fields.Many2one('stock.lot', 'Lote/Nº de serie')

    @api.onchange('product_id')
    def _onchange_product_id(self):
        self.lot_id = False
        self.product_uom_qty = 0

    @api.onchange('product_uom_qty')
    def _onchange_product_uom_qty(self):
        if not self.product_uom_qty or self.product_uom_qty < 0:
            return

        '''
        if not self.product_id:
            return {'warning': {
                'title': 'Cuidado',
                'message': 'Debe seleccionar un producto'
            }}

        if not self.lot_id:
            return {'warning': {
                'title': 'Cuidado',
                'message': 'Debe seleccionar un producto Lote/Nº de serie'
            }}
        '''

        domain = [
            ('product_id', '=', self.product_id.id),
            ('lot_id', '=', self.lot_id.id),
        ]
        stock_quant_obj = self.env['stock.quant'].search(domain, limit=1)
        if self.product_id and self.lot_id and stock_quant_obj.quantity < self.product_uom_qty:
            self.product_uom_qty = 0
            return {'warning': {
                'title': 'Cuidado',
                'message': 'La cantidad ingresada supera el stock disponible'
            }}
