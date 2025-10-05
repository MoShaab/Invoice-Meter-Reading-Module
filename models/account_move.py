# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class AccountMoveLine(models.Model):
    """
    Extends account.move.line to add meter reading fields.
    These fields track meter readings for utility billing.
    """
    _inherit = 'account.move.line'

    meter_previous = fields.Float(
        string='Previous Reading',
        digits=(12, 2),
        help='Previous meter reading from the last invoice for this partner'
    )
    
    meter_new = fields.Float(
        string='New Reading',
        digits=(12, 2),
        help='Current meter reading for this billing period'
    )
    
    meter_actual = fields.Float(
        string='Actual Consumption',
        compute='_compute_meter_actual',
        store=True,
        digits=(12, 2),
        help='Calculated difference between new and previous readings'
    )

    @api.depends('meter_new', 'meter_previous')
    def _compute_meter_actual(self):
        """Calculate actual consumption."""
        for line in self:
            if line.meter_new and line.meter_previous:
                line.meter_actual = line.meter_new - line.meter_previous
            else:
                line.meter_actual = 0.0

    @api.onchange('meter_actual')
    def _onchange_meter_actual(self):
        """Auto-populate quantity from actual consumption."""
        if self.meter_actual > 0:
            self.quantity = self.meter_actual

    @api.constrains('meter_new', 'meter_previous')
    def _check_meter_readings(self):
        """Validate that new reading >= previous reading."""
        for line in self:
            if line.meter_new and line.meter_previous:
                if line.meter_new < line.meter_previous:
                    raise ValidationError(
                        'New meter reading cannot be less than previous reading.\n'
                        f'Previous: {line.meter_previous}, New: {line.meter_new}'
                    )

    @api.model_create_multi
    def create(self, vals_list):
        """Auto-retrieve previous reading from last invoice."""
        lines = super(AccountMoveLine, self).create(vals_list)
        
        for line in lines:
            if line.move_id.move_type in ['out_invoice', 'out_refund'] and line.product_id:
                partner = line.move_id.partner_id
                
                if partner and not line.meter_previous:
                    last_invoice_line = self.search([
                        ('move_id.partner_id', '=', partner.id),
                        ('move_id.move_type', 'in', ['out_invoice', 'out_refund']),
                        ('move_id.state', '=', 'posted'),
                        ('product_id', '=', line.product_id.id),
                        ('id', '!=', line.id),
                        ('meter_new', '>', 0)
                    ], order='move_id.invoice_date desc', limit=1)
                    
                    if last_invoice_line:
                        line.meter_previous = last_invoice_line.meter_new
        
        return lines


class AccountMove(models.Model):
    """Extends account.move for invoice validation."""
    _inherit = 'account.move'

    def action_post(self):
        """Validate meter readings before posting."""
        for move in self:
            for line in move.invoice_line_ids:
                if line.meter_new and line.meter_previous:
                    if line.meter_new < line.meter_previous:
                        raise ValidationError(
                            f'Cannot post invoice: New meter reading ({line.meter_new}) '
                            f'is less than previous reading ({line.meter_previous}) '
                            f'for product {line.product_id.name}'
                        )
        
        return super(AccountMove, self).action_post()
