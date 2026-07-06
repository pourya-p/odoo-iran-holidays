# Iran Public Holidays for Odoo 16

Import and synchronize official Iranian public holidays into Odoo Working Hours using the Time.ir API.

## Features

- Import official Iranian public holidays
- Apply holidays to one or more Working Hours
- Import holidays into all Working Hours
- Automatic monthly synchronization using a scheduled action
- Update existing holidays instead of creating duplicates

## Requirements

- Odoo 16 Community or Enterprise
- Python 3.10+
- requests

## Installation

1. Copy the module into your custom addons directory.
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Update the Apps List.
4. Install **Iran Public Holidays**.

## Usage

Go to:

```
Employees
→ Configuration
→ Import Iran Public Holidays
```

Choose:

- Jalali Year
- Jalali Month
- All Working Hours or selected Working Hours

Then click **Import Holidays**.

## Automatic Synchronization

The module creates a Scheduled Action that periodically synchronizes holidays from the Time.ir API.

## Data Source

Holiday data is provided by:

https://api.time.ir

## License

LGPL-3