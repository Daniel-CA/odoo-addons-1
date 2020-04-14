# -*- coding: utf-8 -*-
# © 2016 Ignacio Ibeas - Acysos S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import models


class AccountPaymentTerm(models.Model):
    _inherit = "account.payment.term"

    def compute(self, value, date_ref=False):
        result = super(AccountPaymentTerm, self).compute(value, date_ref)
        if 'invoice' in self._context:
            invoice = self._context.get('invoice')
            if invoice.retention_date_due and invoice.retention_amount > 0 \
                and invoice.with_retention:
                new_result = [[]]
                for term in result[0]:
                    if invoice.type in ['out_invoice', 'out_refund']:
                        newamt = term[1] - invoice.retention_amount
                    else:
                        newamt = term[1] + invoice.retention_amount
                    new_result[0].append((term[0], newamt))
                if invoice.type in ['out_invoice', 'out_refund']:
                    retention_amount = invoice.retention_amount
                else:
                    retention_amount = -invoice.retention_amount
                new_result[0].append((invoice.retention_date_due,
                                      retention_amount))
                return new_result
        return result
