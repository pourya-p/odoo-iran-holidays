# -*- coding: utf-8 -*-

{
    "name": "Iran Public Holidays",
    "summary": "Import and synchronize Iranian public holidays.",
    "description": """
    Iran Public Holidays
    
    This module imports official Iranian public holidays into Odoo working schedules.
    
    Features:
    - Import holidays for a selected month
    - Synchronize holidays with the official API
    - Automatic monthly synchronization
    - Support multiple working schedules
    - Optional Work Entry Type support
    """,
    "version": "16.0.1.0.0",
    "author": "Pourya Parhoode",
    "website": "https://github.com/pourya-p/odoo-iran-holidays",
    "license": "LGPL-3",
    "category": "Human Resources",
    "application": False,
    "installable": True,

    "depends": [
        "hr",
        "resource",
    ],

    "data": [
        "security/ir.model.access.csv",

        "views/import_holidays_views.xml",

        "data/ir_cron.xml",
    ],
}