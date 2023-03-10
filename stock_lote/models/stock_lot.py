from odoo import api, models


class StockLot(models.Model):
    _inherit = 'stock.production.lot'

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        ctx = self.env.context
        if ctx.get('product_id'):
            domain = [
                ('product_id', '=', ctx['product_id']),
                ('on_hand', '=', True),
            ]
            lot_ids = self.env['stock.quant'].search(domain).mapped('lot_id').ids
            args = [('id', 'in', lot_ids)] + args
        elif ctx.get('origin') and ctx.get('default_product_id'):
            domain = [
                ('order_id.name', '=', ctx['origin']),
                ('product_id', '=', ctx['default_product_id']),
            ]
            lot_ids = self.env['sale.order.line'].search(domain).mapped('lot_id').ids
            args = [('id', 'in', lot_ids)] + args

        return super(StockLot, self).name_search(name, args, operator, limit)

    def name_get(self):
        ctx = self.env.context
        res_old = super(StockLot, self).name_get()
        if ctx.get('product_id'):
            domain = [
                ('product_id', '=', ctx['product_id']),
                ('on_hand', '=', True),
            ]
            stock_quant_objs = self.env['stock.quant'].search(domain)
            map_lote = {
                stock_quant.lot_id.id: stock_quant.available_quantity
                for stock_quant in stock_quant_objs
            }

            res = []
            for (key, name) in res_old:
                if key in map_lote:
                    res.append((key, '%s (Disp: %s)' % (name, map_lote[key])))
                else:
                    res.append((key, name))
            return res

        return res_old
