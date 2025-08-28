#!/usr/bin/env python3
"""
Cyber Services Database Seeder
Automatically populates cyber services in the database
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import CyberService
from datetime import datetime

def seed_cyber_services():
    """Seed the database with cyber services"""
    app = create_app()
    
    with app.app_context():
        try:
            print("🌱 Seeding Cyber Services...")
            
            # Define all available cyber services
            services = [
                # KRA Services
                {
                    'name': 'Application of KRA PIN',
                    'slug': 'kra-pin-application',
                    'description': 'Get your KRA PIN number for tax purposes. This is a mandatory requirement for all Kenyan citizens and residents for tax compliance.',
                    'short_description': 'Get your KRA PIN number for tax purposes.',
                    'price': 250.00,
                    'category': 'KRA',
                    'subcategory': 'PIN Application',
                    'estimated_duration': '24-48 hours',
                    'requirements': 'Valid ID, Phone number, Email address',
                    'benefits': 'Official KRA PIN certificate, Tax compliance, Business registration eligibility',
                    'instructions': 'Provide your ID details and contact information. We will process your KRA PIN application and deliver the certificate.',
                    'is_featured': True,
                    'sort_order': 1
                },
                {
                    'name': 'Creating KRA Account',
                    'slug': 'kra-account-creation',
                    'description': 'Create your KRA iTax account for online tax services. Access to file returns, make payments, and manage your tax affairs online.',
                    'short_description': 'Create your KRA iTax account for online tax services.',
                    'price': 50.00,
                    'category': 'KRA',
                    'subcategory': 'Account Creation',
                    'estimated_duration': '2-4 hours',
                    'requirements': 'KRA PIN, Phone number, Email address',
                    'benefits': 'Online tax filing, Payment processing, Tax management portal access',
                    'instructions': 'We will create your iTax account and provide you with login credentials.',
                    'is_featured': True,
                    'sort_order': 2
                },
                {
                    'name': 'Filing KRA Returns - Individual',
                    'slug': 'kra-returns-individual',
                    'description': 'File your individual tax returns with KRA. Ensure compliance with tax regulations and avoid penalties.',
                    'short_description': 'File your individual tax returns with KRA.',
                    'price': 200.00,
                    'category': 'KRA',
                    'subcategory': 'Tax Filing',
                    'estimated_duration': '24-48 hours',
                    'requirements': 'KRA PIN, Income details, Deductions information',
                    'benefits': 'Tax compliance, Avoid penalties, Tax refund processing',
                    'instructions': 'Provide your income and deduction details. We will file your returns and handle any follow-up.',
                    'is_featured': False,
                    'sort_order': 3
                },
                {
                    'name': 'Filing KRA Returns - Company',
                    'slug': 'kra-returns-company',
                    'description': 'File company tax returns with KRA. Ensure your business meets all tax obligations.',
                    'short_description': 'File company tax returns with KRA.',
                    'price': 150.00,
                    'category': 'KRA',
                    'subcategory': 'Tax Filing',
                    'estimated_duration': '48-72 hours',
                    'requirements': 'Company KRA PIN, Financial statements, Business details',
                    'benefits': 'Business tax compliance, Avoid penalties, Professional filing',
                    'instructions': 'Provide your company financial details. We will file your returns and handle compliance.',
                    'is_featured': False,
                    'sort_order': 4
                },
                {
                    'name': 'Changing KRA Details',
                    'slug': 'kra-details-update',
                    'description': 'Update your KRA registration details including address, phone number, and other personal information.',
                    'short_description': 'Update your KRA registration details.',
                    'price': 300.00,
                    'category': 'KRA',
                    'subcategory': 'Details Update',
                    'estimated_duration': '24-48 hours',
                    'requirements': 'KRA PIN, New details, Supporting documents',
                    'benefits': 'Updated records, Accurate tax correspondence, Compliance',
                    'instructions': 'Provide your new details and supporting documents. We will update your KRA records.',
                    'is_featured': False,
                    'sort_order': 5
                },
                {
                    'name': 'KRA Waiver Application',
                    'slug': 'kra-waiver-application',
                    'description': 'Apply for KRA penalty waiver. Reduce or eliminate penalties for late filing or payment.',
                    'short_description': 'Apply for KRA penalty waiver.',
                    'price': 300.00,
                    'category': 'KRA',
                    'subcategory': 'Waiver',
                    'estimated_duration': '5-7 days',
                    'requirements': 'KRA PIN, Penalty details, Justification letter',
                    'benefits': 'Penalty reduction, Cost savings, Compliance restoration',
                    'instructions': 'Provide penalty details and justification. We will prepare and submit your waiver application.',
                    'is_featured': False,
                    'sort_order': 6
                },
                {
                    'name': 'Resetting KRA Password',
                    'slug': 'kra-password-reset',
                    'description': 'Reset your KRA iTax account password. Regain access to your tax management portal.',
                    'short_description': 'Reset your KRA iTax account password.',
                    'price': 50.00,
                    'category': 'KRA',
                    'subcategory': 'Password Reset',
                    'estimated_duration': '2-4 hours',
                    'requirements': 'KRA PIN, Registered phone number',
                    'benefits': 'Account access restored, Security maintained, Quick resolution',
                    'instructions': 'We will reset your password and provide new login credentials.',
                    'is_featured': False,
                    'sort_order': 7
                },
                
                # HELB Services
                {
                    'name': 'Creating HELB Account',
                    'slug': 'helb-account-creation',
                    'description': 'Create your HELB account for student loan services. Access to loan applications and management.',
                    'short_description': 'Create your HELB account for student loan services.',
                    'price': 50.00,
                    'category': 'HELB',
                    'subcategory': 'Account Creation',
                    'estimated_duration': '2-4 hours',
                    'requirements': 'ID Number, Phone number, Email address',
                    'benefits': 'Loan application access, Account management, Student services',
                    'instructions': 'We will create your HELB account and provide login credentials.',
                    'is_featured': True,
                    'sort_order': 8
                },
                {
                    'name': 'HELB Application - TVET',
                    'slug': 'helb-application-tvet',
                    'description': 'Apply for HELB loan for TVET students. Financial support for technical and vocational education.',
                    'short_description': 'Apply for HELB loan for TVET students.',
                    'price': 500.00,
                    'category': 'HELB',
                    'subcategory': 'Loan Application',
                    'estimated_duration': '5-7 days',
                    'requirements': 'ID Number, Institution details, Parent/Guardian details',
                    'benefits': 'Educational funding, Low interest rates, Flexible repayment',
                    'instructions': 'Provide your educational and financial details. We will process your HELB application.',
                    'is_featured': False,
                    'sort_order': 9
                },
                {
                    'name': 'HELB Application - Undergraduate',
                    'slug': 'helb-application-undergraduate',
                    'description': 'Apply for HELB loan for undergraduate students. Financial support for university education.',
                    'short_description': 'Apply for HELB loan for undergraduate students.',
                    'price': 500.00,
                    'category': 'HELB',
                    'subcategory': 'Loan Application',
                    'estimated_duration': '5-7 days',
                    'requirements': 'ID Number, University details, Parent/Guardian details',
                    'benefits': 'University funding, Low interest rates, Flexible repayment terms',
                    'instructions': 'Provide your university and financial details. We will process your HELB application.',
                    'is_featured': False,
                    'sort_order': 10
                },
                
                # Business Services
                {
                    'name': 'Registration of Business Name',
                    'slug': 'business-name-registration',
                    'description': 'Register your business name with the Registrar of Companies. Legal business identity and protection.',
                    'short_description': 'Register your business name with the Registrar of Companies.',
                    'price': 500.00,
                    'category': 'Business',
                    'subcategory': 'Registration',
                    'estimated_duration': '5-7 days',
                    'requirements': 'Business name, Owner details, Business description',
                    'benefits': 'Legal business identity, Name protection, Business credibility',
                    'instructions': 'Provide your business details. We will register your business name and provide the certificate.',
                    'is_featured': True,
                    'sort_order': 11
                },
                {
                    'name': 'Registration of Company',
                    'slug': 'company-registration',
                    'description': 'Register a limited liability company. Full legal entity with shareholder protection.',
                    'short_description': 'Register a limited liability company.',
                    'price': 1000.00,
                    'category': 'Business',
                    'subcategory': 'Registration',
                    'estimated_duration': '7-10 days',
                    'requirements': 'Company name, Directors details, Shareholders information',
                    'benefits': 'Limited liability protection, Professional status, Investment attraction',
                    'instructions': 'Provide company and director details. We will register your company and provide all documents.',
                    'is_featured': True,
                    'sort_order': 12
                },
                
                # NTSA Services
                {
                    'name': 'Renewal of Driving License',
                    'slug': 'driving-license-renewal',
                    'description': 'Renew your driving license with NTSA. Maintain your driving privileges and compliance.',
                    'short_description': 'Renew your driving license with NTSA.',
                    'price': 200.00,
                    'category': 'NTSA',
                    'subcategory': 'License Renewal',
                    'estimated_duration': '3-5 days',
                    'requirements': 'Current license, ID Number, Passport photo',
                    'benefits': 'Valid driving license, Legal compliance, Insurance eligibility',
                    'instructions': 'Provide your current license and ID details. We will renew your driving license.',
                    'is_featured': False,
                    'sort_order': 13
                },
                {
                    'name': 'Application of Digital Driving License',
                    'slug': 'digital-driving-license',
                    'description': 'Apply for digital driving license with NTSA. Modern, secure, and convenient driving credential.',
                    'short_description': 'Apply for digital driving license with NTSA.',
                    'price': 400.00,
                    'category': 'NTSA',
                    'subcategory': 'Digital License',
                    'estimated_duration': '5-7 days',
                    'requirements': 'ID Number, Passport photo, Previous license (if any)',
                    'benefits': 'Digital convenience, Enhanced security, Modern credential',
                    'instructions': 'Provide your details and photo. We will process your digital driving license application.',
                    'is_featured': False,
                    'sort_order': 14
                }
            ]
            
            # Check if services already exist
            existing_count = CyberService.query.count()
            if existing_count > 0:
                print(f"ℹ️  {existing_count} cyber services already exist in database")
                print("🔄 Updating existing services...")
                
                # Update existing services
                for service_data in services:
                    existing_service = CyberService.query.filter_by(slug=service_data['slug']).first()
                    if existing_service:
                        # Update existing service
                        for key, value in service_data.items():
                            setattr(existing_service, key, value)
                        existing_service.updated_at = datetime.utcnow()
                        print(f"✅ Updated: {service_data['name']}")
                    else:
                        # Create new service
                        new_service = CyberService(**service_data)
                        db.session.add(new_service)
                        print(f"➕ Added: {service_data['name']}")
            else:
                print("🆕 No existing services found. Creating all services...")
                
                # Create all services
                for service_data in services:
                    new_service = CyberService(**service_data)
                    db.session.add(new_service)
                    print(f"➕ Created: {service_data['name']}")
            
            # Commit all changes
            db.session.commit()
            
            # Final count
            final_count = CyberService.query.count()
            print(f"🎉 Successfully seeded {final_count} cyber services!")
            
            # Show categories
            categories = db.session.query(CyberService.category).distinct().all()
            print(f"📂 Categories: {', '.join([cat[0] for cat in categories])}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error seeding cyber services: {e}")
            db.session.rollback()
            return False

if __name__ == "__main__":
    success = seed_cyber_services()
    if success:
        print("🎯 Cyber services seeding completed successfully!")
    else:
        print("💥 Cyber services seeding failed!") 