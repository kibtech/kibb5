#!/usr/bin/env python3
"""
Fix SQLAlchemy Queries for 2.0 Compatibility
============================================
Update all .query. patterns to use db.session.query() for SQLAlchemy 2.0 compatibility.
"""

import os
import re

def fix_file(file_path):
    """Fix SQLAlchemy queries in a single file"""
    print(f"🔧 Fixing {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Track changes
    changes_made = 0
    
    # Fix Model.query.get() -> db.session.get(Model, id)
    pattern1 = r'(\w+)\.query\.get\(([^)]+)\)'
    replacement1 = r'db.session.get(\1, \2)'
    new_content, count = re.subn(pattern1, replacement1, content)
    changes_made += count
    
    # Fix Model.query.filter_by() -> db.session.query(Model).filter_by()
    pattern2 = r'(\w+)\.query\.filter_by\(([^)]+)\)'
    replacement2 = r'db.session.query(\1).filter_by(\2)'
    new_content, count = re.subn(pattern2, replacement2, new_content)
    changes_made += count
    
    # Fix Model.query.filter() -> db.session.query(Model).filter()
    pattern3 = r'(\w+)\.query\.filter\(([^)]+)\)'
    replacement3 = r'db.session.query(\1).filter(\2)'
    new_content, count = re.subn(pattern3, replacement3, new_content)
    changes_made += count
    
    # Fix Model.query.order_by() -> db.session.query(Model).order_by()
    pattern4 = r'(\w+)\.query\.order_by\(([^)]+)\)'
    replacement4 = r'db.session.query(\1).order_by(\2)'
    new_content, count = re.subn(pattern4, replacement4, new_content)
    changes_made += count
    
    # Fix Model.query.limit() -> db.session.query(Model).limit()
    pattern5 = r'(\w+)\.query\.limit\(([^)]+)\)'
    replacement5 = r'db.session.query(\1).limit(\2)'
    new_content, count = re.subn(pattern5, replacement5, new_content)
    changes_made += count
    
    # Fix Model.query.all() -> db.session.query(Model).all()
    pattern6 = r'(\w+)\.query\.all\(\)'
    replacement6 = r'db.session.query(\1).all()'
    new_content, count = re.subn(pattern6, replacement6, new_content)
    changes_made += count
    
    # Fix Model.query.first() -> db.session.query(Model).first()
    pattern7 = r'(\w+)\.query\.first\(\)'
    replacement7 = r'db.session.query(\1).first()'
    new_content, count = re.subn(pattern7, replacement7, new_content)
    changes_made += count
    
    # Fix Model.query.count() -> db.session.query(Model).count()
    pattern8 = r'(\w+)\.query\.count\(\)'
    replacement8 = r'db.session.query(\1).count()'
    new_content, count = re.subn(pattern8, replacement8, new_content)
    changes_made += count
    
    # Fix Model.query.get_or_404() -> db.session.get_or_404(Model, id)
    pattern9 = r'(\w+)\.query\.get_or_404\(([^)]+)\)'
    replacement9 = r'db.session.get_or_404(\1, \2)'
    new_content, count = re.subn(pattern9, replacement9, new_content)
    changes_made += count
    
    # Write back if changes were made
    if changes_made > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"   ✅ Fixed {changes_made} query patterns")
        return changes_made
    else:
        print(f"   ⚠️ No changes needed")
        return 0

def main():
    """Main function to fix all Python files"""
    print("🚀 Starting SQLAlchemy 2.0 Query Fix...")
    print("=" * 50)
    
    # Files to fix
    files_to_fix = [
        'app/wishlist/routes.py',
        'app/wallet/routes.py',
        'app/services/otp_service.py',
        'app/reviews/routes.py',
        'app/products/routes.py',
        'app/orders/routes.py',
        'app/notifications/routes.py',
        'app/mpesa/routes.py',
        'app/cyber_services/routes.py',
        'app/admin/users.py',
        'app/admin/system_monitor.py',
        'app/models.py'
    ]
    
    total_changes = 0
    
    for file_path in files_to_fix:
        if os.path.exists(file_path):
            changes = fix_file(file_path)
            total_changes += changes
        else:
            print(f"⚠️ File not found: {file_path}")
    
    print("\n" + "=" * 50)
    print(f"✅ Fixed {total_changes} total query patterns across {len(files_to_fix)} files")
    print("🎉 SQLAlchemy 2.0 compatibility update complete!")

if __name__ == "__main__":
    main() 