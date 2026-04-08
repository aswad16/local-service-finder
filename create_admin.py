#!/usr/bin/env python
"""
create_admin.py — Create a superuser / admin account for LocalServe.

Usage:
    python create_admin.py

Or with env vars:
    ADMIN_USER=admin ADMIN_PASS=secret123 ADMIN_EMAIL=admin@example.com python create_admin.py
"""
import os
import sys
import django

# Bootstrap Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'localservice.settings')
django.setup()

from users.models import CustomUser


def create_admin():
    username = os.environ.get('ADMIN_USER') or input('Admin username [admin]: ').strip() or 'admin'
    email = os.environ.get('ADMIN_EMAIL') or input('Admin email [admin@localserve.com]: ').strip() or 'admin@localserve.com'

    if os.environ.get('ADMIN_PASS'):
        password = os.environ['ADMIN_PASS']
    else:
        import getpass
        password = getpass.getpass('Admin password: ')
        confirm = getpass.getpass('Confirm password: ')
        if password != confirm:
            print('❌ Passwords do not match.')
            sys.exit(1)

    if CustomUser.objects.filter(username=username).exists():
        print(f'⚠️  User "{username}" already exists.')
        overwrite = input('Update password and promote to admin? [y/N]: ').strip().lower()
        if overwrite == 'y':
            user = CustomUser.objects.get(username=username)
            user.set_password(password)
            user.role = 'admin'
            user.is_staff = True
            user.is_superuser = True
            user.is_verified = True
            user.save()
            print(f'✅ User "{username}" updated and promoted to admin.')
        else:
            print('Aborted.')
        return

    user = CustomUser.objects.create_superuser(
        username=username,
        email=email,
        password=password,
        role='admin',
        is_verified=True,
    )
    print(f'✅ Admin user "{username}" created successfully!')
    print(f'   Email:    {email}')
    print(f'   Role:     {user.role}')
    print(f'   Login at: http://localhost:8000/users/login/')
    print(f'   Admin at: http://localhost:8000/adminpanel/')


if __name__ == '__main__':
    create_admin()
