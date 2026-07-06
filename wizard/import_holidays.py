# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import UserError


class ImportIranHolidaysWizard(models.TransientModel):
    _name = "import.iran.holidays.wizard"
    _description = "Import Iranian Public Holidays Wizard"

    year = fields.Integer(
        string="سال شمسی",
        required=True,
        default=lambda self: self._default_year(),
    )

    month = fields.Selection(
        selection=[
            ("1", "فروردین"),
            ("2", "اردیبهشت"),
            ("3", "خرداد"),
            ("4", "تیر"),
            ("5", "مرداد"),
            ("6", "شهریور"),
            ("7", "مهر"),
            ("8", "آبان"),
            ("9", "آذر"),
            ("10", "دی"),
            ("11", "بهمن"),
            ("12", "اسفند"),
        ],
        string="ماه",
        required=True,
        default=lambda self: str(self._default_month()),
    )

    apply_all_calendars = fields.Boolean(
        string="اعمال روی همه ساعات کاری",
        default=True,
        help="در صورت فعال بودن، تعطیلات برای تمام ساعات کاری موجود در سیستم اعمال می‌شود.",
    )

    calendar_ids = fields.Many2many(
        comodel_name="resource.calendar",
        relation="holiday_import_calendar_rel",
        column1="wizard_id",
        column2="calendar_id",
        string="ساعات کاری",
        help="در صورتی که گزینه «اعمال روی همه ساعات کاری» غیرفعال باشد، تعطیلات فقط روی ساعات کاری انتخاب‌شده اعمال می‌شوند.",
    )

    note = fields.Html(
        string="راهنما",
        sanitize=False,
        readonly=True,
        default=lambda self: """
            <div class="alert alert-info mb-0">
                <strong>راهنما</strong>
                <br/>
                اگر گزینه <strong>«اعمال روی همه ساعات کاری»</strong> فعال باشد،
                تعطیلات برای تمام ساعات کاری <strong>شرکت فعال</strong> ایجاد یا
                به‌روزرسانی می‌شوند.
                <br/><br/>
                اگر قصد دارید تعطیلات فقط برای ساعات کاری خاصی اعمال شوند،
                این گزینه را غیرفعال کرده و یک یا چند ساعت کاری را انتخاب کنید.
                <br/><br/>
                برای اعمال تعطیلات در شرکت دیگر، ابتدا شرکت فعال را از منوی انتخاب
                شرکت تغییر دهید.
            </div>
        """,
    )

    # -------------------------------------------------------------------------
    # Defaults
    # -------------------------------------------------------------------------

    @api.model
    def _default_year(self):
        """
        Returns the default Jalali year.
        """

        # TODO:
        # Calculate current Jalali year automatically.
        return 1405

    @api.model
    def _default_month(self):
        """
        Returns the default Jalali month.
        """

        # TODO:
        # Calculate current Jalali month automatically.
        return 1

    # -------------------------------------------------------------------------
    # Constraints
    # -------------------------------------------------------------------------

    @api.constrains("month")
    def _check_month(self):
        """
        Validates the selected month.
        """

        for wizard in self:
            month = int(wizard.month)

            if month < 1 or month > 12:
                raise UserError("ماه انتخاب‌شده معتبر نیست.")

    # -------------------------------------------------------------------------
    # Actions
    # -------------------------------------------------------------------------

    def action_import(self):
        """
        Imports holidays into the selected working schedules.
        """

        self.ensure_one()

        if self.apply_all_calendars:
            calendars = self.env["resource.calendar"].search([
                ("company_id", "=", self.env.company.id),
            ])

            if not calendars:
                raise UserError(
                    "هیچ ساعت کاری برای شرکت فعال یافت نشد."
                )
        else:
            calendars = self.calendar_ids

            if not calendars:
                raise UserError(
                    "حداقل یک ساعت کاری را انتخاب کنید."
                )

        self.env["holiday.import.service"].import_month(
            year=self.year,
            month=int(self.month),
            calendars=calendars,
        )

        return {
            "type": "ir.actions.act_window_close",
        }