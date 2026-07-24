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
        from myapp.models import Polygon, Details, tools, ResourceItem, Crop, HistoricalPrice
        from datetime import date, timedelta

        polygon, _ = Polygon.objects.get_or_create(
            polygon_id='67969e9650f5a45f841b8c23',
            defaults={'name': 'Main Farm Field'}
        )
        Details.objects.get_or_create(
            polygon=polygon,
            defaults={'api_key': ''}
        )

        # Seed tools if table is empty
        if tools.objects.count() == 0:
            sample_tools = [
                {
                    'title': 'Heavy Duty Farm Tractor',
                    'collection': 'Power Machinery',
                    'badge': 'Best Seller',
                    'rating': 5,
                    'old_price': 650000,
                    'new_price': 599000,
                    'img_url': 'https://images.unsplash.com/photo-1592982537447-6f2a6a0c7c18?w=800&auto=format&fit=crop',
                    'link': '#'
                },
                {
                    'title': 'Solar Powered Irrigation Pump',
                    'collection': 'Irrigation & Water',
                    'badge': 'Eco Friendly',
                    'rating': 5,
                    'old_price': 45000,
                    'new_price': 38500,
                    'img_url': 'https://images.unsplash.com/photo-1563514227147-6d2ff665a6a0?w=800&auto=format&fit=crop',
                    'link': '#'
                },
                {
                    'title': 'Multi-Crop Power Tiller',
                    'collection': 'Soil Tillage',
                    'badge': 'Top Rated',
                    'rating': 4,
                    'old_price': 85000,
                    'new_price': 76000,
                    'img_url': 'https://images.unsplash.com/photo-1589923188900-85dae523342b?w=800&auto=format&fit=crop',
                    'link': '#'
                },
                {
                    'title': 'Digital Soil NPK & Moisture Tester',
                    'collection': 'Precision Ag Tech',
                    'badge': 'Smart Tech',
                    'rating': 5,
                    'old_price': 12000,
                    'new_price': 8999,
                    'img_url': 'https://images.unsplash.com/photo-1615811361523-6bd03d7748e7?w=800&auto=format&fit=crop',
                    'link': '#'
                },
                {
                    'title': 'Agricultural Crop Spraying Drone',
                    'collection': 'Aerial Farm Drones',
                    'badge': 'New Arrival',
                    'rating': 5,
                    'old_price': 320000,
                    'new_price': 285000,
                    'img_url': 'https://images.unsplash.com/photo-1508614589041-895b88991e3e?w=800&auto=format&fit=crop',
                    'link': '#'
                },
                {
                    'title': 'Automatic Drip Irrigation Kit',
                    'collection': 'Irrigation & Water',
                    'badge': 'Popular',
                    'rating': 4,
                    'old_price': 18000,
                    'new_price': 14500,
                    'img_url': 'https://images.unsplash.com/photo-1590682680695-43b964a3ae17?w=800&auto=format&fit=crop',
                    'link': '#'
                }
            ]
            for t in sample_tools:
                tools.objects.create(**t)

        # Seed ResourceItems if table is empty
        if ResourceItem.objects.count() == 0:
            sample_resources = [
                {'category': 'seeds', 'title': 'High-Yield Hybrid Wheat Seeds (HD-3086)', 'link': '#', 'img_url': 'https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=800&auto=format&fit=crop', 'price_range': '₹1,200 - ₹1,500 / bag'},
                {'category': 'seeds', 'title': 'Organic Basmati Paddy Seeds (Pusa 1121)', 'link': '#', 'img_url': 'https://images.unsplash.com/photo-1586201375761-83865001e31c?w=800&auto=format&fit=crop', 'price_range': '₹2,000 - ₹2,400 / bag'},
                {'category': 'fertilizers', 'title': 'Organic Vermicompost Soil Fertilizer', 'link': '#', 'img_url': 'https://images.unsplash.com/photo-1615811361523-6bd03d7748e7?w=800&auto=format&fit=crop', 'price_range': '₹400 - ₹650 / 50kg'},
                {'category': 'fertilizers', 'title': 'Bio-NPK Liquid Fertilizer Concentrate', 'link': '#', 'img_url': 'https://images.unsplash.com/photo-1628352081506-83c43123ed6d?w=800&auto=format&fit=crop', 'price_range': '₹850 - ₹1,100 / Litre'},
                {'category': 'pest_control', 'title': 'Neem Oil Bio-Pesticide (10000 PPM)', 'link': '#', 'img_url': 'https://images.unsplash.com/photo-1585336261026-61e778a29b68?w=800&auto=format&fit=crop', 'price_range': '₹650 - ₹850 / Litre'},
                {'category': 'pest_control', 'title': 'Yellow Sticky Traps for Insects (Pack of 25)', 'link': '#', 'img_url': 'https://images.unsplash.com/photo-1611080626919-7cf5a9dbab5b?w=800&auto=format&fit=crop', 'price_range': '₹350 - ₹500 / pack'},
                {'category': 'livestock', 'title': 'High-Protein Cattle Feed Supplement', 'link': '#', 'img_url': 'https://images.unsplash.com/photo-1546445317-29f4545f9d52?w=800&auto=format&fit=crop', 'price_range': '₹1,500 - ₹1,800 / 50kg'},
                {'category': 'livestock', 'title': 'Automatic Livestock Drinking Bowl', 'link': '#', 'img_url': 'https://images.unsplash.com/photo-1500595046743-cd271d694d30?w=800&auto=format&fit=crop', 'price_range': '₹800 - ₹1,200'},
                {'category': 'storage', 'title': 'Hermetic Grain Storage Bags (Super Grain Bag)', 'link': '#', 'img_url': 'https://images.unsplash.com/photo-1595246140625-573b715d11dc?w=800&auto=format&fit=crop', 'price_range': '₹180 - ₹250 / bag'},
                {'category': 'storage', 'title': 'Heavy Duty Galvanized Steel Grain Silo', 'link': '#', 'img_url': 'https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=800&auto=format&fit=crop', 'price_range': '₹45,000 - ₹80,000'}
            ]
            for r in sample_resources:
                ResourceItem.objects.create(**r)

        # Seed Crops & Historical Prices if table is empty
        if Crop.objects.count() == 0:
            sample_crops = [
                {'name': 'Wheat (Sharbati)', 'current_price': 2450.00, 'trend': 'UP', 'description': 'High-grade wheat cultivated in Central India.'},
                {'name': 'Basmati Rice (1121)', 'current_price': 4850.00, 'trend': 'STABLE', 'description': 'Premium long-grain aromatic Basmati rice.'},
                {'name': 'Yellow Maize', 'current_price': 2100.00, 'trend': 'UP', 'description': 'High quality corn used for livestock feed and processing.'},
                {'name': 'Soybean', 'current_price': 4300.00, 'trend': 'DOWN', 'description': 'Oilseed crop with steady market demand.'},
                {'name': 'Cotton (Medium Staple)', 'current_price': 6200.00, 'trend': 'UP', 'description': 'Commercial fiber crop harvested across Western India.'},
                {'name': 'Tomato (Hybrid)', 'current_price': 1800.00, 'trend': 'DOWN', 'description': 'Fresh agricultural produce.'}
            ]
            today = date.today()
            for c_data in sample_crops:
                crop = Crop.objects.create(**c_data)
                base_price = float(crop.current_price)
                for d in range(7, 0, -1):
                    HistoricalPrice.objects.create(
                        crop=crop,
                        date=today - timedelta(days=d*3),
                        price=round(base_price * (1 + (d % 3 - 1) * 0.02), 2)
                    )
    except Exception as e:
        print(f"Error initializing database: {e}")


# Initialize database schema and default credentials on startup
init_db()