from django.urls import path
from dashboard import views

'''
Proposed endpoints
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
    # Get active categories, top 5 most trending apps, total apps tracked
    path('v1/summary/', views.Summary.as_view()),
    # Top apps per trend_score
    path('v1/apps/trending/', views.top_trending_apps),
    # Historical and current app details
    path("v1/app/<str:app_id>/", views.app_details),
    # Category details, apps and trend_scores
    path('v1/category/<str:category>/', views.category_details)
]