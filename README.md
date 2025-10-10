# Invoice Meter Reading Module

## Overview
Custom Odoo module that adds meter reading functionality to customer invoices for utility billing scenarios.

## Features
- ✅ **Previous Reading**: Auto-retrieved from last posted invoice
- ✅ **New Reading**: Manual entry for current period
- ✅ **Actual Consumption**: Automatically calculated (New - Previous)
- ✅ **Auto-populate Quantity**: Quantity field auto-fills from actual consumption
- ✅ **Validation**: Prevents posting if new reading < previous reading
- ✅ **Report Integration**: Meter columns appear on printed invoices

## Use Cases
- Electricity billing
- Water utility billing
- Gas consumption tracking
- Propane/LPG delivery
- Any consumption-based billing

## Installation

### Prerequisites
- Odoo 16.0 or higher (tested on 19.0)
- Accounting module installed

### Steps
1. Copy module to your Odoo addons directory
2. Restart Odoo service
3. Update Apps List: `Apps → Update Apps List`
4. Search for "Invoice Meter Reading"
5. Click Install

## Usage

### Creating Invoices with Meter Readings

1. **Create Invoice**: `Accounting → Customers → Invoices → Create`
2. **Add Product**: Select customer and add invoice line with product
3. **Previous Reading**: Auto-fills from last invoice (if exists)
4. **Enter New Reading**: Type current meter reading in "New" column
5. **Auto-calculation**: 
   - "Actual" column calculates automatically (New - Previous)
   - "Quantity" auto-fills from "Actual" value
6. **Save & Post**: Post invoice to finalize readings

### Example Flow

**Month 1 - January**
- Previous: 0 (first invoice)
- New: 1000
- Actual: 1000
- Quantity: 1000
- → Invoice Posted

**Month 2 - February**
- Previous: 1000 (auto-filled)
- New: 1500
- Actual: 500
- Quantity: 500
- → Invoice Posted

**Month 3 - March**
- Previous: 1500 (auto-filled)
- New: 2100
- Actual: 600
- Quantity: 600
- → Invoice Posted

## Technical Details

### Models Extended
- `account.move.line`: Added meter reading fields and logic
- `account.move`: Added posting validation

### New Fields
- `meter_previous` (Float): Previous meter reading
- `meter_new` (Float): Current meter reading
- `meter_actual` (Float, Computed): Consumption amount

### Key Methods
- `_compute_meter_actual()`: Calculates consumption
- `_onchange_meter_actual()`: Auto-populates quantity
- `_check_meter_readings()`: Validates readings
- `_onchange_product_id`: Verify previous reading auto-fills when new inovice is created
- `action_post()`: Final validation before posting



## Development

### Module Structure


### Testing
1. Install module in test database
2. Create customer and product
3. Create first invoice with new reading
4. Post invoice
5. Create second invoice - verify previous reading auto-fills
6. Test validation by entering new reading < previous

## Support
For issues, questions, or contributions, please open an issue on GitHub.

## License
LGPL-3

## Author
**MoShaab**  
GitHub: https://github.com/MoShaab/Invoice-Meter-Reading-Module

