from django.shortcuts import render, redirect, get_object_or_404
from .models import Polygon, Details, tools, Crop, ResourceItem
from .forms import PolygonForm, RegistrationForm
import requests
import json
from datetime import datetime, timedelta
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm


@login_required
def dashboard(request):
    # Try to get the polygon/details associated with the current user.
    # Falls back to the first available Details entry or creates a default polygon.
    details = Details.objects.first()
    if details is None:
        polygon, _ = Polygon.objects.get_or_create(
            polygon_id='67969e9650f5a45f841b8c23',
            defaults={'name': 'Main Farm Field'}
        )
        details, _ = Details.objects.get_or_create(
            polygon=polygon,
            defaults={'api_key': getattr(settings, 'AGRO_API_KEY', '') or ''}
        )

    polygon_id = details.polygon.polygon_id
    api = details.api_key or getattr(settings, 'AGRO_API_KEY', '')

    # Fetch weather data from AgroMonitoring
    weather_data = None
    try:
        result = requests.get(
            f"http://api.agromonitoring.com/agro/1.0/polygons/{polygon_id}?appid={api}",
            timeout=5
        )
        result.raise_for_status()
        center = result.json().get('center', [0, 0])
        weather_resp = requests.get(
            f"https://api.agromonitoring.com/agro/1.0/weather/forecast"
            f"?lat={center[1]}&lon={center[0]}&appid={api}",
            timeout=5
        )
        weather_resp.raise_for_status()
        weather_data = weather_resp.json()
    except requests.exceptions.RequestException as e:
        print(f"Weather API error: {e}")

    # Fetch news data
    news_data = []
    news_api_key = settings.NEWS_API_KEY
    if news_api_key:
        try:
            news_url = (
                f"https://newsapi.org/v2/top-headlines"
                f"?country=in&category=business&apiKey={news_api_key}"
            )
            news_response = requests.get(news_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
            news_response.raise_for_status()
            news_data = news_response.json().get('articles', [])[:3]
        except requests.exceptions.RequestException as e:
            print(f"News API error: {e}")

    context = {
        "weather": weather_data,
        "news": news_data,
    }
    return render(request, 'myapp/dashboard.html', context)


@login_required
def services(request):
    return render(request, 'myapp/services.html')


@login_required
def Tool(request):
    products = tools.objects.all()
    return render(request, 'myapp/tools.html', {'products': products})


def about(request):
    return render(request, 'myapp/about.html')


@login_required
def resources_view(request):
    """Renders the resources page with categorised items from the DB."""
    categories = []
    for category_slug, category_name in ResourceItem.CATEGORY_CHOICES:
        items = ResourceItem.objects.filter(category=category_slug)
        categories.append({
            'slug': category_slug,
            'name': category_name,
            'items': items,
        })
    context = {'categories': categories}
    return render(request, 'myapp/resources.html', context)


@login_required
def market(request):
    crops = Crop.objects.prefetch_related('historical_prices').all().order_by('name')
    return render(request, 'myapp/market.html', {'crops': crops})


@login_required
def trade(request):
    return render(request, 'myapp/trade.html')


def login_page(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'myapp/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


def privacy(request):
    return render(request, 'myapp/privacy.html')


def TandC(request):
    return render(request, 'myapp/TandC.html')


def FAQs(request):
    return render(request, 'myapp/FAQs.html')


def add_polygon(request):
    if request.method == 'POST':
        form = PolygonForm(request.POST)
        if form.is_valid():
            polygon = form.save()
            Details.objects.get_or_create(
                polygon=polygon,
                defaults={'api_key': getattr(settings, 'AGRO_API_KEY', '') or ''}
            )
            return redirect('polygon_list')
    else:
        form = PolygonForm()
    return render(request, 'myapp/add_polygon.html', {'form': form})


def polygon_list(request):
    polygons = Polygon.objects.all()
    return render(request, 'myapp/polygon_list.html', {'polygons': polygons})


@login_required
def news(request):
    """Fetches recent farmer-related news from the past 30 days."""
    news_api_key = settings.NEWS_API_KEY
    articles = []

    if news_api_key:
        from_date = (datetime.utcnow() - timedelta(days=30)).strftime('%Y-%m-%d')
        url = (
            f"https://newsapi.org/v2/everything"
            f"?q=farmer&from={from_date}&sortBy=popularity&apiKey={news_api_key}"
        )
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            raw_articles = response.json().get('articles', [])

            for article in raw_articles:
                articles.append({
                    'title': article.get('title', ''),
                    'description': article.get('description', ''),
                    'image': article.get('urlToImage', ''),
                    'published_at': article.get('publishedAt', ''),
                    'url': article.get('url', '#'),
                })
        except requests.exceptions.RequestException as e:
            print(f"News API error: {e}")
            messages.error(request, "Could not load news at this time.")

    return render(request, 'myapp/news.html', {'articles': articles})


def get_agro_data(request, polygon_id):
    api_key = settings.AGRO_API_KEY
    url = f'https://api.agromonitoring.com/data?api_key={api_key}&polygon_id={polygon_id}'
    try:
        response = requests.get(url, timeout=5)
        data = response.json() if response.status_code == 200 else None
    except requests.exceptions.RequestException:
        data = None
    return render(request, 'myapp/agro_data.html', {'data': data})


def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegistrationForm()

    return render(request, 'myapp/register.html', {'form': form})


def fetch_weather_data(polygon_id):
    api_key = settings.AGRO_API_KEY
    url = f'https://api.agromonitoring.com/data?api_key={api_key}&polygon_id={polygon_id}'
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None


def weather_dashboard(request):
    polygon = Polygon.objects.first()
    data = fetch_weather_data(polygon.polygon_id) if polygon else None
    return render(request, 'myapp/weather_dashboard.html', {'data': data})


def main_dashboard(request):
    polygon = Polygon.objects.first()
    data = fetch_weather_data(polygon.polygon_id) if polygon else None
    return render(request, 'myapp/main_dashboard.html', {'data': data})


@login_required
def details(request, polygon_id):
    polygon, _ = Polygon.objects.get_or_create(
        polygon_id=polygon_id,
        defaults={'name': f'Farm Field ({polygon_id[:8]})'}
    )
    details_obj = Details.objects.filter(polygon=polygon).first()
    if not details_obj:
        details_obj = Details.objects.create(
            polygon=polygon,
            api_key=getattr(settings, 'AGRO_API_KEY', '') or ''
        )

    api = details_obj.api_key or getattr(settings, 'AGRO_API_KEY', '')

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Convert dates to Unix timestamps
    now = timezone.now()
    if end_date:
        try:
            end_datetime = datetime.strptime(end_date, '%Y-%m-%d')
            end_datetime = timezone.make_aware(end_datetime, timezone.get_current_timezone())
            end_timestamp = int(end_datetime.timestamp())
        except ValueError:
            end_timestamp = int(details_obj.end_date.timestamp())
    else:
        end_timestamp = int(details_obj.end_date.timestamp())

    if start_date:
        try:
            start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
            start_datetime = timezone.make_aware(start_datetime, timezone.get_current_timezone())
            start_timestamp = int(start_datetime.timestamp())
        except ValueError:
            start_timestamp = int(details_obj.start_date.timestamp())
    else:
        start_timestamp = int(details_obj.start_date.timestamp())

    context = None
    if api:
        try:
            result = requests.get(
                f"http://api.agromonitoring.com/agro/1.0/polygons/{polygon_id}?appid={api}",
                timeout=5
            )
            result.raise_for_status()
            ndvi = requests.get(
                f"http://api.agromonitoring.com/agro/1.0/ndvi/history"
                f"?start={start_timestamp}&end={end_timestamp}&polyid={polygon_id}&appid={api}",
                timeout=5
            )
            center = result.json().get('center', [77.2090, 28.6139])
            weather = requests.get(
                f"https://api.agromonitoring.com/agro/1.0/weather/forecast"
                f"?lat={center[1]}&lon={center[0]}&appid={api}",
                timeout=5
            )
            soil = requests.get(
                f"http://api.agromonitoring.com/agro/1.0/soil?polyid={polygon_id}&appid={api}",
                timeout=5
            )
            uv_index = requests.get(
                f"http://api.agromonitoring.com/agro/1.0/uvi?polyid={polygon_id}&appid={api}",
                timeout=5
            )

            uv_index_data = uv_index.json() if uv_index.status_code == 200 else {}
            uv_index_value = uv_index_data.get('uvi', 5.4)
            uv_dt = uv_index_data.get('dt')
            uv_index_date = (
                datetime.utcfromtimestamp(uv_dt).strftime('%Y-%m-%d %H:%M:%S')
                if uv_dt else now.strftime('%Y-%m-%d %H:%M:%S')
            )

            context = {
                "api_data_json": result.json(),
                "ndvi_data_json": ndvi.json() if ndvi.status_code == 200 else [],
                "start_date": start_date or (now - timedelta(days=30)).strftime('%Y-%m-%d'),
                "end_date": end_date or now.strftime('%Y-%m-%d'),
                "polygon_id": polygon_id,
                "weather": weather.json() if weather.status_code == 200 else [],
                "soil": soil.json() if soil.status_code == 200 else {},
                "uv_index_value": uv_index_value,
                "uv_index_date": uv_index_date,
            }
        except Exception as e:
            print(f"AgroAPI request error: {e}")

    # Fallback to realistic farm demonstration data if API key is missing or call fails
    if not context or "api_data_json" not in context:
        mock_api_data = {
            "id": polygon_id,
            "name": polygon.name,
            "center": [77.2090, 28.6139],
            "area": 12.45,
            "geo_json": {
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [77.2050, 28.6100],
                        [77.2130, 28.6100],
                        [77.2130, 28.6180],
                        [77.2050, 28.6180],
                        [77.2050, 28.6100]
                    ]]
                }
            }
        }
        mock_ndvi_data = [
            {
                "dt": int((now - timedelta(days=i * 5)).timestamp()),
                "type": "sentinel-2",
                "dc": 1600000000,
                "cl": 0,
                "data": {
                    "std": 0.04,
                    "p25": 0.45,
                    "num": 1000,
                    "min": round(0.35 + (i * 0.02) % 0.15, 2),
                    "max": round(0.75 + (i * 0.01) % 0.1, 2),
                    "median": round(0.60 + (i * 0.01) % 0.1, 2),
                    "p75": round(0.70 + (i * 0.01) % 0.1, 2),
                    "mean": round(0.58 + (i * 0.015) % 0.15, 2)
                }
            } for i in range(6, 0, -1)
        ]
        mock_weather = [
            {
                "dt": int((now + timedelta(hours=i * 3)).timestamp()),
                "main": {"temp": 298.15 + i % 3, "humidity": 60 + i % 10, "pressure": 1012},
                "weather": [{"main": "Clear", "description": "clear sky", "icon": "01d"}],
                "clouds": {"all": 10},
                "wind": {"speed": 3.6, "deg": 140}
            } for i in range(5)
        ]
        mock_soil = {
            "dt": int(now.timestamp()),
            "t10": 295.15,
            "moisture": 0.32,
            "t0": 297.45
        }

        context = {
            "api_data_json": mock_api_data,
            "ndvi_data_json": mock_ndvi_data,
            "start_date": start_date or (now - timedelta(days=30)).strftime('%Y-%m-%d'),
            "end_date": end_date or now.strftime('%Y-%m-%d'),
            "polygon_id": polygon_id,
            "weather": mock_weather,
            "soil": mock_soil,
            "uv_index_value": 5.4,
            "uv_index_date": now.strftime('%Y-%m-%d %H:%M:%S'),
        }

    return render(request, "myapp/details.html", context)


@method_decorator(csrf_exempt, name='dispatch')
class ChatbotView(View):
    """
    Chatbot powered by Google Gemini AI.
    Uses the correct generateContent endpoint (not the crypto exchange).
    """

    def get(self, request):
        return render(request, 'chatbot/chat_popup.html')

    def post(self, request):
        try:
            data = json.loads(request.body)
            message = data.get('message', '')

            api_key = settings.GEMINI_API_KEY
            if not api_key:
                return JsonResponse(
                    {"error": "Gemini API key not configured. Set GEMINI_API_KEY in .env"},
                    status=503
                )

            # Correct Google Gemini AI endpoint
            url = (
                f"https://generativelanguage.googleapis.com/v1beta/models/"
                f"gemini-pro:generateContent?key={api_key}"
            )
            payload = {
                "contents": [
                    {
                        "parts": [{"text": message}]
                    }
                ]
            }
            response = requests.post(url, json=payload, timeout=15)
            response_data = response.json()

            # Extract the text from the Gemini response structure
            try:
                bot_response = (
                    response_data['candidates'][0]['content']['parts'][0]['text']
                )
            except (KeyError, IndexError):
                bot_response = "Sorry, I could not understand that."

            return JsonResponse({'message': bot_response})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
