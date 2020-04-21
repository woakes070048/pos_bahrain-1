# -*- coding: utf-8 -*-
# Copyright (c) 2018, 	9t9it and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import flt
from erpnext.setup.utils import get_exchange_rate


def validate(doc, method):
    if (
        doc.is_pos
        and not doc.is_return
        and not doc.amended_from
        and doc.offline_pos_name
        and frappe.db.exists(
            "Sales Invoice",
            {"offline_pos_name": doc.offline_pos_name, "name": ("!=", doc.name)},
        )
    ):
        frappe.throw("Cannot create duplicate offline POS invoice")
    for payment in doc.payments:
        if payment.amount:
            bank_method = frappe.get_cached_value(
                "Mode of Payment", payment.mode_of_payment, "pb_bank_method"
            )
            if bank_method and not payment.pb_reference_no:
                frappe.throw(
                    "Reference Number necessary in payment row #{}".format(payment.idx)
                )
            if bank_method == "Cheque" and not payment.pb_reference_date:
                frappe.throw(
                    "Reference Date necessary in payment row #{}".format(payment.idx)
                )


def before_save(doc, method):
    set_cost_center(doc)


def on_submit(doc, method):
    for payment in doc.payments:
        if not payment.mop_currency:
            currency = frappe.db.get_value(
                "Mode of Payment", payment.mode_of_payment, "alt_currency"
            )
            conversion_rate = (
                get_exchange_rate(
                    currency, frappe.defaults.get_user_default("currency")
                )
                if currency
                else 1.0
            )
            frappe.db.set_value(
                "Sales Invoice Payment",
                payment.name,
                "mop_currency",
                currency or frappe.defaults.get_user_default("currency"),
            )
            frappe.db.set_value(
                "Sales Invoice Payment",
                payment.name,
                "mop_conversion_rate",
                conversion_rate,
            )
            frappe.db.set_value(
                "Sales Invoice Payment",
                payment.name,
                "mop_amount",
                flt(payment.base_amount) / flt(conversion_rate),
            )


def set_cost_center(doc):
    if doc.pb_set_cost_center:
        for row in doc.items:
            row.cost_center = doc.pb_set_cost_center
