from odoo import models, fields, api

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    meter_previous = fields.Float(string='Previous', digits=(12, 2))
    meter_new = fields.Float(string='New', digits=(12, 2))
    meter_actual = fields.Float(string='Actual', compute='_compute_meter_actual', store=True, digits=(12, 2))

    @api.depends('meter_new', 'meter_previous')
    def _compute_meter_actual(self):
        # Calculate actual consumption.
        for line in self:
            line.meter_actual = (line.meter_new or 0.0) - (line.meter_previous or 0.0)

    @api.onchange('meter_actual')
    def _onchange_meter_actual(self):
        # Auto-populate quantity from actual.
        if self.meter_actual > 0:
            self.quantity = self.meter_actual

    @api.onchange('meter_new', 'meter_previous')
    def _onchange_meter_readings(self):
        # Trigger when readings change.
        self._compute_meter_actual()
        if self.meter_actual > 0:
            self.quantity = self.meter_actual

    @api.onchange('product_id')
    def _onchange_product_id(self):
        # Auto-fill previous reading based on last invoice.
        if self.move_id.partner_id and self.product_id:
            last_line = self.search([
                ('move_id.partner_id', '=', self.move_id.partner_id.id),
                ('move_id.state', '=', 'posted'),
                ('product_id', '=', self.product_id.id),
                ('meter_new', '>', 0)
            ], order='id desc', limit=1)
            if last_line:
                self.meter_previous = last_line.meter_new
