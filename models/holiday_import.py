# -*- coding: utf-8 -*-

import logging

from odoo import api, models

_logger = logging.getLogger(__name__)


class HolidayImport(models.AbstractModel):
    _name = "holiday.import.service"
    _description = "Iran Holiday Import Service"

    # -------------------------------------------------------------------------
    # Public API
    # -------------------------------------------------------------------------

    @api.model
    def import_month(
        self,
        year,
        month,
        calendars=None,
        work_entry_type=None,
    ):
        """
        Import a month from the official API.

        Parameters
        ----------
        year : int
            Jalali year.

        month : int
            Jalali month.

        calendars : resource.calendar recordset
            Working calendars that holidays should be applied to.

            If None or empty, all calendars will be used.

        work_entry_type : hr.work.entry.type
            Optional work entry type.
        """

        if not calendars:
            calendars = self.env["resource.calendar"].search([])

        data = self._fetch_month(year, month)

        holidays = self._extract_holidays(data)

        self._sync_holidays(
            holidays=holidays,
            calendars=calendars,
            work_entry_type=work_entry_type,
        )

    # -------------------------------------------------------------------------
    # API
    # -------------------------------------------------------------------------

    def _fetch_month(self, year, month):
        """
        Call the official API.

        Returns raw JSON.
        """
        raise NotImplementedError()

    # -------------------------------------------------------------------------
    # JSON
    # -------------------------------------------------------------------------

    def _extract_holidays(self, data):
        """
        Convert API JSON to a simplified list.

        Returns:

        [
            {
                "name": "...",
                "date": date,
                ...
            }
        ]
        """
        raise NotImplementedError()

    # -------------------------------------------------------------------------
    # Sync
    # -------------------------------------------------------------------------

    def _sync_holidays(
        self,
        holidays,
        calendars,
        work_entry_type=None,
    ):
        """
        Synchronize holidays with resource.calendar.leaves.
        """
        raise NotImplementedError()