# Copyright 2022 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class AccountMove(models.Model):

    _inherit = "account.move"

    def action_post(self):
        res = super().action_post()
        for move in self:
            order = move.invoice_line_ids.mapped("purchase_line_id.order_id")
            if order and order.company_id.enable_purchase_mis_cash_flow_forecast:
                order.with_delay()._generate_mis_cash_flow_forecast_lines()
        return res

    def button_cancel(self):
        super().button_cancel()
        for move in self:
            order = move.invoice_line_ids.mapped("purchase_line_id.order_id")
            if order and order.company_id.enable_purchase_mis_cash_flow_forecast:
                order._compute_forecast_uninvoiced_amount()
                order.with_delay()._generate_mis_cash_flow_forecast_lines()

    def button_draft(self):
        super().button_draft()
        for move in self:
            order = move.invoice_line_ids.mapped("purchase_line_id.order_id")
            if order and order.company_id.enable_purchase_mis_cash_flow_forecast:
                order._compute_forecast_uninvoiced_amount()
                order.with_delay()._generate_mis_cash_flow_forecast_lines()

    @api.model
    def create(self, vals_list):
        moves = super().create(vals_list)
        for move in moves:
            order = move.invoice_line_ids.mapped("purchase_line_id.order_id")
            if order and order.company_id.enable_purchase_mis_cash_flow_forecast:
                order._compute_forecast_uninvoiced_amount()
                order.with_delay()._generate_mis_cash_flow_forecast_lines()
        return moves
