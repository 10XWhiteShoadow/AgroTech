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
        if ResourceItem.objects.count() < 15:
            ResourceItem.objects.all().delete()
            sample_resources = [
                # seeds
                {'category': 'seeds', 'title': 'High-Yield Hybrid Wheat Seeds (HD-3086)', 'link': '#', 'img_url': 'https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=800&auto=format&fit=crop', 'price_range': '₹1,200 - ₹1,500 / bag'},
                {'category': 'seeds', 'title': 'Organic Basmati Paddy Seeds (Pusa 1121)', 'link': '#', 'img_url': 'https://images.unsplash.com/photo-1586201375761-83865001e31c?w=800&auto=format&fit=crop', 'price_range': '₹2,000 - ₹2,400 / bag'},
                {'category': 'seeds', 'title': 'Hybrid Yellow Maize Seeds (Pioneer 3302)', 'link': '#', 'img_url': 'https://images.unsplash.com/photo-1551754655-cd27e38d2076?w=800&auto=format&fit=crop', 'price_range': '₹1,800 - ₹2,100 / bag'},
                {'category': 'seeds', 'title': 'High-Oil Soybean Seeds (JS 335)', 'link': '#', 'img_url': 'https://images.unsplash.com/photo-1592982537447-6f2a6a0c7c18?w=800&auto=format&fit=crop', 'price_range': '₹2,200 - ₹2,600 / bag'},
                {'category': 'seeds', 'title': 'Organic Vegetable Kitchen Garden Kit (12 Variety)', 'link': '#', 'img_url': 'https://images.unsplash.com/photo-1595246140625-573b715d11dc?w=800&auto=format&fit=crop', 'price_range': '₹450 - ₹600 / kit'},
                # fertilizers
                {'category': 'fertilizers', 'title': 'Organic Vermicompost Soil Fertilizer', 'link': '#', 'img_url': 'https://images.unsplash.com/photo-1615811361523-6bd03d7748e7?w=800&auto=format&fit=crop', 'price_range': '₹400 - ₹650 / 50kg'},
                {'category': 'fertilizers', 'title': 'Bio-NPK Liquid Fertilizer Concentrate', 'link': '#', 'img_url': 'https://images.unsplash.com/photo-1628352081506-83c43123ed6d?w=800&auto=format&fit=crop', 'price_range': '₹850 - ₹1,100 / Litre'},
                {'category': 'fertilizers', 'title': 'Neem Cake Powder Soil Conditioner', 'link': '#', 'img_url': 'https://images.unsplash.com/photo-1585336261026-61e778a29b68?w=800&auto=format&fit=crop', 'price_range': '₹550 - ₹750 / 50kg'},
                {'category': 'fertilizers', 'title': 'Water Soluble NPK 19:19:19 Spray', 'link': '#', 'img_url': 'https://images.unsplash.com/photo-1590682680695-43b964a3ae17?w=800&auto=format&fit=crop', 'price_range': '₹180 - ₹250 / kg'},
                {'category': 'fertilizers', 'title': 'Micronutrient Mixture (Zinc, Boron, Iron)', 'link': '#', 'img_url': 'https://images.unsplash.com/photo-1563514227147-6d2ff665a6a0?w=800&auto=format&fit=crop', 'price_range': '₹320 - ₹450 / kg'},
                # pest_control
                {'category': 'pest_control', 'title': 'Neem Oil Bio-Pesticide (10000 PPM)', 'link': '#', 'img_url': 'https://images.unsplash.com/photo-1585336261026-61e778a29b68?w=800&auto=format&fit=crop', 'price_range': '₹650 - ₹850 / Litre'},
                {'category': 'pest_control', 'title': 'Yellow & Blue Sticky Traps for Insects (Pack of 25)', 'link': '#', 'img_url': 'https://images.unsplash.com/photo-1611080626919-7cf5a9dbab5b?w=800&auto=format&fit=crop', 'price_range': '₹350 - ₹500 / pack'},
                {'category': 'pest_control', 'title': 'Trichoderma Viride Bio-Fungicide Powder', 'link': '#', 'img_url': 'https://images.unsplash.com/photo-1615811361523-6bd03d7748e7?w=800&auto=format&fit=crop', 'price_range': '₹240 - ₹350 / kg'},
                {'category': 'pest_control', 'title': 'Pheromone Trap for Cotton Pink Bollworm', 'link': '#', 'img_url': 'https://images.unsplash.com/photo-1508614589041-895b88991e3e?w=800&auto=format&fit=crop', 'price_range': '₹150 - ₹220 / unit'},
                {'category': 'pest_control', 'title': 'Solar Powered LED Insect Killer Trap', 'link': '#', 'img_url': 'https://images.unsplash.com/photo-1563514227147-6d2ff665a6a0?w=800&auto=format&fit=crop', 'price_range': '₹2,800 - ₹3,500 / unit'},
                # livestock
                {'category': 'livestock', 'title': 'High-Protein Cattle Feed Supplement', 'link': '#', 'img_url': 'https://images.unsplash.com/photo-1546445317-29f4545f9d52?w=800&auto=format&fit=crop', 'price_range': '₹1,500 - ₹1,800 / 50kg'},
                {'category': 'livestock', 'title': 'Automatic Stainless Steel Livestock Bowl', 'link': '#', 'img_url': 'https://images.unsplash.com/photo-1500595046743-cd271d694d30?w=800&auto=format&fit=crop', 'price_range': '₹800 - ₹1,200'},
                {'category': 'livestock', 'title': 'Chelated Mineral Mixture for Dairy Cows', 'link': '#', 'img_url': 'https://images.unsplash.com/photo-1570042707222-772922119ef0?w=800&auto=format&fit=crop', 'price_range': '₹650 - ₹900 / 5kg'},
                {'category': 'livestock', 'title': 'Heavy Duty Electric Chaff Cutter Machine', 'link': '#', 'img_url': 'https://images.unsplash.com/photo-1589923188900-85dae523342b?w=800&auto=format&fit=crop', 'price_range': '₹16,500 - ₹22,000'},
                {'category': 'livestock', 'title': 'Automatic Poultry Nipple Drinking System', 'link': '#', 'img_url': 'https://images.unsplash.com/photo-1548550023-2bdb3c5beed7?w=800&auto=format&fit=crop', 'price_range': '₹1,200 - ₹1,800 / set'},
                # storage
                {'category': 'storage', 'title': 'Hermetic Grain Storage Bags (Super Grain Bag)', 'link': '#', 'img_url': 'https://images.unsplash.com/photo-1595246140625-573b715d11dc?w=800&auto=format&fit=crop', 'price_range': '₹180 - ₹250 / bag'},
                {'category': 'storage', 'title': 'Heavy Duty Galvanized Steel Grain Silo', 'link': '#', 'img_url': 'https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=800&auto=format&fit=crop', 'price_range': '₹45,000 - ₹80,000'},
                {'category': 'storage', 'title': 'Solar Powered Micro Cold Storage Unit (2 MT)', 'link': '#', 'img_url': 'https://images.unsplash.com/photo-1563514227147-6d2ff665a6a0?w=800&auto=format&fit=crop', 'price_range': '₹1,80,000 - ₹2,40,000'},
                {'category': 'storage', 'title': 'Heavy Duty Crop Harvest Plastic Crates (Set of 6)', 'link': '#', 'img_url': 'https://images.unsplash.com/photo-1615811361523-6bd03d7748e7?w=800&auto=format&fit=crop', 'price_range': '₹1,400 - ₹1,800 / set'},
                {'category': 'storage', 'title': 'Heavy Duty Tarpaulin Waterproof Sheet (24ft x 18ft)', 'link': '#', 'img_url': 'https://images.unsplash.com/photo-1592982537447-6f2a6a0c7c18?w=800&auto=format&fit=crop', 'price_range': '₹2,200 - ₹2,800'}
            ]
            for r in sample_resources:
                ResourceItem.objects.create(**r)

        # Seed Crops & Historical Prices if table is empty
        if Crop.objects.count() < 12:
            Crop.objects.all().delete()
            sample_crops = [
                {'name': 'Wheat (Sharbati)', 'current_price': 2450.00, 'trend': 'UP', 'description': 'High-grade premium wheat cultivated across MP & Punjab mandis.'},
                {'name': 'Basmati Rice (Pusa 1121)', 'current_price': 4850.00, 'trend': 'STABLE', 'description': 'Premium long-grain aromatic Basmati rice export variety.'},
                {'name': 'Chickpea (Chana Desi)', 'current_price': 5200.00, 'trend': 'UP', 'description': 'High demand pulse benchmark across Rajasthan & MP markets.'},
                {'name': 'Yellow Maize (Corn)', 'current_price': 2100.00, 'trend': 'UP', 'description': 'Industrial starch & high grade livestock feed corn.'},
                {'name': 'Soybean (Yellow)', 'current_price': 4300.00, 'trend': 'DOWN', 'description': 'Central India commercial oilseed crop.'},
                {'name': 'Mustard Seed (Rai)', 'current_price': 5400.00, 'trend': 'UP', 'description': 'High oil yield mustard harvested in Northern India.'},
                {'name': 'Cotton (Medium Staple)', 'current_price': 6200.00, 'trend': 'UP', 'description': 'Commercial fiber crop from Gujarat & Maharashtra.'},
                {'name': 'Sugarcane (CO 0238)', 'current_price': 350.00, 'trend': 'STABLE', 'description': 'State advisory mill gate price per quintal.'},
                {'name': 'Turmeric (Rajapuri)', 'current_price': 14500.00, 'trend': 'UP', 'description': 'High-curcumin spice crop from Nizamabad mandi.'},
                {'name': 'Red Gram (Tur/Arhar)', 'current_price': 7100.00, 'trend': 'UP', 'description': 'Key pulse commodity with active trading volume.'},
                {'name': 'Potato (Jyoti Fresh)', 'current_price': 1450.00, 'trend': 'STABLE', 'description': 'Fresh harvest table potato from UP & West Bengal.'},
                {'name': 'Onion (Red Nashik)', 'current_price': 1850.00, 'trend': 'DOWN', 'description': 'Major horticulture commodity from Lasalgaon mandi.'},
                {'name': 'Tomato (Hybrid)', 'current_price': 1800.00, 'trend': 'DOWN', 'description': 'Fresh farm-gate vegetable produce.'},
                {'name': 'Groundnut (In Shell)', 'current_price': 5850.00, 'trend': 'UP', 'description': 'Saurashtra region oilseed crop.'},
                {'name': 'Green Gram (Moong)', 'current_price': 7400.00, 'trend': 'STABLE', 'description': 'Summer pulse crop under MSP support.'}
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