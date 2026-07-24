"""
WSGI config for myproject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

application = get_wsgi_application()
app = application


def init_db():
    try:
        from django.core.management import call_command
        from django.contrib.auth import get_user_model

        # Run database migrations to ensure tables exist in writable location
        call_command('migrate', interactive=False)

        # Ensure default superuser account exists
        User = get_user_model()
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')

        # Ensure default farm polygon and details records exist
        from myapp.models import Polygon, Details
        polygon, _ = Polygon.objects.get_or_create(
            polygon_id='67969e9650f5a45f841b8c23',
            defaults={'name': 'Main Farm Field'}
        )
        Details.objects.get_or_create(
            polygon=polygon,
            defaults={'api_key': ''}
        )
    except Exception as e:
        print(f"Error initializing database: {e}")


# Initialize database schema and default credentials on startup
init_db()