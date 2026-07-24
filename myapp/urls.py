from django.urls import path
from . import views

urlpatterns = [
    # Core routes
    path('', views.dashboard, name='dashboard'),

    # Authentication routes
    path('login/', views.login_page, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # Application routes
    path('services/', views.services, name='services'),
    path('tools/', views.Tool, name='tools'),
    path('about/', views.about, name='about'),
    path('resources/', views.resources_view, name='resources'),
    path('market/', views.market, name='market'),
    path('trade/', views.trade, name='trade'),
    path('privacy/', views.privacy, name='privacy'),
    path('TandC/', views.TandC, name='TandC'),
    path('FAQs/', views.FAQs, name='FAQs'),
    path('news/', views.news, name='news'),

    # Polygon / farm data routes
    path('add_polygon/', views.add_polygon, name='add_polygon'),
    path('polygons/', views.polygon_list, name='polygon_list'),
    path('agro_data/<str:polygon_id>/', views.get_agro_data, name='get_agro_data'),
    path('details/<str:polygon_id>/', views.details, name='details'),

    # Chatbot
    path('chatbot/', views.ChatbotView.as_view(), name='chatbot'),
]