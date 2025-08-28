#!/usr/bin/env python3
"""
Run the commission schema migration
"""

from fix_commission_schema import migrate_commission_schema

if __name__ == "__main__":
    print("Starting commission schema migration...")
    migrate_commission_schema()
    print("Migration completed!") 