from django.urls import path
from dashboard import views

'''
Proposed endpoints
GET /api/categories
    Lista de todas las categorías activas
GET /api/category/<category_name>/trending
    Top apps en tendencia por categoría
GET /api/category/<category_name>/distribution
    Distribución de trend_score para la categoría
GET /api/apps/trending
    Apps destacadas globales en trend_score
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
    path('v1/summary', views.Summary.as_view())
]