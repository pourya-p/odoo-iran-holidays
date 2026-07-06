# -*- coding: utf-8 -*-

import logging

import requests

from odoo import api, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class HolidayImportService(models.AbstractModel):
    _name = "holiday.import.service"
    _description = "Iran Public Holiday Import Service"

    API_URL = "https://api.time.ir/v1/event/fa/events/calendar"

    # -------------------------------------------------------------------------
    # Public API
    # -------------------------------------------------------------------------

    @api.model
    def import_month(self, year, month, calendars=None):
        """
        Imports and synchronizes a Jalali month.
        """

        if not calendars:
            calendars = self.env["resource.calendar"].search([
                ("company_id", "=", self.env.company.id),
            ])

            if not calendars:
                raise UserError(
                    "هیچ ساعت کاری برای شرکت فعال یافت نشد."
                )

        data = self._fetch_month(year, month)

        holidays = self._extract_holidays(data)

        self._sync_holidays(
            holidays=holidays,
            calendars=calendars,
        )

    # -------------------------------------------------------------------------
    # API
    # -------------------------------------------------------------------------

    def _fetch_month(self, year, month):
        """
        Fetches a month from the Time.ir API.
        """

        params = {
            "year": year,
            "month": month,
            "day": 0,
            "base1": 0,
            "base2": 1,
            "base3": 2,
        }

        try:
            response = requests.get(
                self.API_URL,
                params=params,
                timeout=20,
            )

            response.raise_for_status()

        except requests.RequestException:
            _logger.exception("Unable to connect to Time.ir API.")

            raise UserError(
                "امکان برقراری ارتباط با سرویس دریافت تعطیلات وجود ندارد."
            )

        return response.json()

    # -------------------------------------------------------------------------
    # JSON
    # -------------------------------------------------------------------------

    def _extract_holidays(self, data):
        """
        Extracts only public holidays from the API response.
        """

        holidays = []

        for event in data.get("data", {}).get("event_list", []):

            if not event.get("is_holiday"):
                continue

            holidays.append({
                "id": event["id"],
                "name": event["title"],
                "date": (
                    f"{event['gregorian_year']:04d}-"
                    f"{event['gregorian_month']:02d}-"
                    f"{event['gregorian_day']:02d}"
                ),
            })

        return holidays

    # -------------------------------------------------------------------------
    # Synchronization
    # -------------------------------------------------------------------------

    def _sync_holidays(self, holidays, calendars):
        """
        Synchronizes holidays with resource.calendar.leaves.
        """

        Leave = self.env["resource.calendar.leaves"]

        for calendar in calendars:

            for holiday in holidays:

                leave = Leave.search([
                    ("calendar_id", "=", calendar.id),
                    ("holiday_source", "=", "time_ir"),
                    ("holiday_source_id", "=", holiday["id"]),
                ], limit=1)

                values = {
                    "name": holiday["name"],
                    "calendar_id": calendar.id,
                    "date_from": f"{holiday['date']} 00:00:00",
                    "date_to": f"{holiday['date']} 23:59:59",
                    "holiday_source": "time_ir",
                    "holiday_source_id": holiday["id"],
                }

                if leave:
                    leave.write(values)
                else:
                    Leave.create(values)

    @api.model
    def cron_import_current_month(self):
        """
        Imports public holidays for the current Jalali month.
        """
        import jdatetime

        today = jdatetime.date.today()

        calendars = self.env["resource.calendar"].search([
            ("company_id", "=", self.env.company.id),
        ])

        self.import_month(
            year=today.year,
            month=today.month,
            calendars=calendars,
        )