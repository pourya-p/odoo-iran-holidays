# -*- coding: utf-8 -*-

from odoo import fields, models


class ResourceCalendarLeaves(models.Model):
    _inherit = "resource.calendar.leaves"

    holiday_source = fields.Char(
        string="منبع تعطیلی",
        readonly=True,
        copy=False,
        index=True,
        help="نام سرویسی که این تعطیلی را ایجاد کرده است.",
    )

    holiday_source_id = fields.Integer(
        string="شناسه تعطیلی",
        readonly=True,
        copy=False,
        index=True,
        help="شناسه یکتای تعطیلی در سرویس دریافت اطلاعات.",
    )