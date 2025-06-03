from django.urls import path
from dashboard import views

'''
Proposed endpoints
GET /api/category/<category_name>/trending
    Top apps en tendencia por categoría
GET /api/category/<category_name>/distribution
    Distribución de trend_score para la categoría
GET /api/app/<app_id>
    Detalles históricos y actuales de una app
GET /api/search?term=photo+editor
    Trigger search for a term (apps/games).
GET /api/app/{app_id}/sentiment-summary
    Aggregate sentiment analysis results.
GET /api/app/{app_id}/recommendations
    Show suggestions based on sentiment & topics.
GET /api/scrape
    Trigger background scraping 
'''

urlpatterns = [
    path('v1/summary/', views.Summary.as_view()),
    # Top apps per trend_score
    path('v1/apps/trending/', views.top_trending_apps),
    # Historical and current app details
    path("v1/app/<str:app_id>/", views.app_details)
]