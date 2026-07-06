# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ImportIranHolidaysWizard(models.TransientModel):
    _name = "import.iran.holidays.wizard"
    _description = "Import Iranian Public Holidays"

    year = fields.Integer(
        string="سال شمسی",
        required=True,
        default=lambda self: self._default_year(),
    )

    month = fields.Integer(
        string="ماه",
        required=True,
        default=lambda self: self._default_month(),
    )

    apply_all_calendars = fields.Boolean(
        string="اعمال روی همه ساعات کاری",
        default=True,
        help="در صورت فعال بودن، تعطیلات برای تمام ساعات کاری موجود در سیستم اعمال می‌شود.",
    )

    calendar_ids = fields.Many2many(
        "resource.calendar",
        relation="holiday_import_calendar_rel",
        column1="wizard_id",
        column2="calendar_id",
        string="ساعات کاری",
    )

    note = fields.Html(
        compute="_compute_note",
        sanitize=False,
    )

    @api.model
    def _default_year(self):
        # بعداً از روی تاریخ شمسی امروز محاسبه می‌شود
        return 1405

    @api.model
    def _default_month(self):
        # بعداً از روی تاریخ شمسی امروز محاسبه می‌شود
        return 1

    @api.depends()
    def _compute_note(self):
        for wizard in self:
            wizard.note = """
            <div class="alert alert-info mb-0">
                <strong>راهنما</strong><br/>
                در صورت فعال بودن گزینه <b>«اعمال روی همه ساعات کاری»</b>،
                تعطیلات برای تمام ساعات کاری موجود در سیستم ایجاد یا به‌روزرسانی خواهد شد.
                <br/><br/>
                در غیر این صورت می‌توانید یک یا چند ساعت کاری را انتخاب کنید.
            </div>
            """

    @api.constrains("month")
    def _check_month(self):
        for wizard in self:
            if wizard.month < 1 or wizard.month > 12:
                raise ValidationError("ماه باید عددی بین ۱ تا ۱۲ باشد.")

    def action_import(self):
        self.ensure_one()

        if self.apply_all_calendars:
            calendars = self.env["resource.calendar"].search([])
        else:
            calendars = self.calendar_ids

            if not calendars:
                raise ValidationError(
                    "حداقل یک ساعت کاری را انتخاب کنید."
                )

        self.env["holiday.import.service"].import_month(
            year=self.year,
            month=self.month,
            calendars=calendars,
        )

        return {
            "type": "ir.actions.act_window_close",
        }