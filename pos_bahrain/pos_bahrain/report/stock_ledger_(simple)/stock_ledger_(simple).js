// Copyright (c) 2019, 	9t9it and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports['Stock Ledger (Simple)'] = {
  filters: [
    {
      fieldname: 'company',
      label: __('Company'),
      fieldtype: 'Link',
      options: 'Company',
      default: frappe.defaults.get_user_default('Company'),
      reqd: 1,
    },
    {
      fieldname: 'from_date',
      label: __('From Date'),
      fieldtype: 'Date',
      default: frappe.datetime.add_months(frappe.datetime.get_today(), -1),
      reqd: 1,
    },
    {
      fieldname: 'to_date',
      label: __('To Date'),
      fieldtype: 'Date',
      default: frappe.datetime.get_today(),
      reqd: 1,
    },
    {
      fieldname: 'warehouse',
      label: __('Warehouse'),
      fieldtype: 'Link',
      options: 'Warehouse',
    },
    {
      fieldname: 'item_code',
      label: __('Item'),
      fieldtype: 'Link',
      options: 'Item',
      get_query: function() {
        return {
          query: 'erpnext.controllers.queries.item_query',
        };
      },
    },
    {
      fieldname: 'item_group',
      label: __('Item Group'),
      fieldtype: 'Link',
      options: 'Item Group',
    },
    {
      fieldname: 'batch_no',
      label: __('Batch No'),
      fieldtype: 'Link',
      options: 'Batch',
    },
    {
      fieldname: 'brand',
      label: __('Brand'),
      fieldtype: 'Link',
      options: 'Brand',
    },
    {
      fieldname: 'voucher_no',
      label: __('Voucher #'),
      fieldtype: 'Data',
    },
    {
      fieldname: 'include_uom',
      label: __('Include UOM'),
      fieldtype: 'Link',
      options: 'UOM',
    },
    {
      fieldname: 'default_supplier',
      label: __('Default Supplier'),
      fieldtype: 'Link',
      options: 'Supplier',
    },
  ],
};
