# -*- coding: utf-8 -*-

{
    "name": "Iran Public Holidays",
    "summary": "Import and synchronize Iranian public holidays.",
    "description": """
Iran Public Holidays

Features:
- Import official Iranian public holidays
- Synchronize holidays with Time.ir
- Apply holidays to one or more Working Hours
- Automatic monthly synchronization
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
    ],

    "data": [
        "security/ir.model.access.csv",

        "views/import_holidays_views.xml",

        "data/ir_cron.xml",
    ],
}