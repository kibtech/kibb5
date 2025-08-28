# Manual Commissions Fix

## Problem
The system was encountering a foreign key constraint violation when trying to create manual commissions:
```
(psycopg2.errors.ForeignKeyViolation) insert or update on table "commissions" violates foreign key constraint "commissions_order_id_fkey"
DETAIL: Key (order_id)=(1) is not present in table "orders".
```

## Root Cause
The `Commission` model required an `order_id` that references an existing order, but for manual commissions, there's no actual order. The code was trying to use `order_id=1` as a fallback, but no order with ID=1 existed.

## Solution

### 1. Updated Commission Model
- Made `order_id` nullable to allow manual commissions without orders
- Added `commission_type` field to distinguish between 'order' and 'manual' commissions
- Added `description` field for manual commission descriptions

### 2. Updated Database Schema
- Created migration script to add new columns
- Made `order_id` nullable in existing database
- Added default values for existing records

### 3. Updated Backend Code
- Modified admin commission routes to use new fields
- Updated regular commission creation to include type and description
- Fixed all commission creation points (orders, cyber services, mpesa)

### 4. Updated Frontend
- Enhanced wallet page to display manual commissions properly
- Added support for commission types and descriptions
- Improved commission display with better labels

## Files Modified

### Backend
- `app/models.py` - Updated Commission model
- `app/admin/commissions.py` - Fixed manual commission creation
- `app/orders/routes.py` - Updated order commission creation
- `app/cyber_services/routes.py` - Updated cyber service commission creation
- `app/mpesa/routes.py` - Updated mpesa commission creation

### Frontend
- `frontend/src/pages/WalletPage.js` - Enhanced commission display

### Migration Scripts
- `fix_commission_schema.py` - Database migration script
- `setup_manual_commissions.py` - Complete setup script
- `run_migration.py` - Simple migration runner

## How to Apply the Fix

### Option 1: Run the Setup Script (Recommended)
```bash
python setup_manual_commissions.py
```

### Option 2: Run Migration Only
```bash
python run_migration.py
```

### Option 3: Manual Steps
1. Run the database migration:
   ```bash
   python fix_commission_schema.py
   ```

2. Restart your application

## Testing

After applying the fix, you can test manual commissions by:

1. **Through Admin Panel:**
   - Go to Admin → Commissions
   - Add manual commission to a user
   - Verify it appears in their wallet

2. **Through API:**
   ```bash
   POST /api/admin/commissions/manual-add
   {
     "user_id": 1,
     "amount": 100,
     "description": "Test manual commission"
   }
   ```

3. **Check Wallet Page:**
   - Login as the user
   - Go to Wallet page
   - Verify manual commission appears with proper description

## Features

### Manual Commissions
- ✅ Can be created without requiring an order
- ✅ Include descriptions for clarity
- ✅ Properly tracked in wallet balance
- ✅ Display correctly in frontend

### Order Commissions
- ✅ Continue to work as before
- ✅ Include order references
- ✅ Proper descriptions with order numbers

### Admin Features
- ✅ Add manual commissions
- ✅ Remove manual commissions
- ✅ View all commission types
- ✅ Filter by user

## Database Schema Changes

```sql
-- New columns added to commissions table
ALTER TABLE commissions ADD COLUMN commission_type VARCHAR(20) DEFAULT 'order';
ALTER TABLE commissions ADD COLUMN description TEXT;

-- Made order_id nullable
ALTER TABLE commissions ALTER COLUMN order_id DROP NOT NULL;
```

## Commission Types

- **order**: Commission from actual orders (has order_id)
- **manual**: Manual commission added by admin (no order_id)

## Benefits

1. **No More Foreign Key Errors**: Manual commissions don't require existing orders
2. **Better Tracking**: Clear distinction between order and manual commissions
3. **Improved UX**: Better descriptions and labels in frontend
4. **Admin Flexibility**: Easy to add/remove manual commissions
5. **Data Integrity**: Proper schema design with nullable order_id

## Troubleshooting

If you encounter issues:

1. **Check Database Connection**: Ensure your database is accessible
2. **Verify Migration**: Run `python fix_commission_schema.py` to ensure schema is updated
3. **Check Permissions**: Ensure admin user has `manage_commissions` permission
4. **Restart Application**: After migration, restart your Flask app

## Support

If you need help with this fix, check:
- Database logs for migration errors
- Application logs for commission creation errors
- Admin panel permissions for commission management 