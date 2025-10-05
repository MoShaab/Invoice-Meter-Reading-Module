# -*- coding: utf-8 -*-
{
    'name': 'Invoice Meter Reading',
    'version': '1.0.0',
    'category': 'Accounting',
    'summary': 'Add meter reading columns to invoices',
    'description': """
        Invoice Meter Reading Module
        =============================
        
        This module extends the Odoo Accounting module to add meter reading functionality.
        
        Features:
        ---------
        * Previous meter reading (automatically retrieved from last invoice)
        * New meter reading (manual entry for current period)
        * Actual consumption (calculated difference)
        * Auto-populate quantity from actual consumption
        * Validation to prevent incorrect readings
        
        Use Cases:
        ----------
        * Utility billing (electricity, water, gas)
        * Propane/LPG delivery tracking
        * Any consumption-based billing
    """,
    'author': 'MoShaab',
    'website': 'https://github.com/MoShaab/Invoice-Meter-Reading-Module',
    'depends': ['account'],
    'data': [
        'security/ir.model.access.csv',
        'views/account_move_views.xml',
        'report/invoice_report_templates.xml',
    ],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
