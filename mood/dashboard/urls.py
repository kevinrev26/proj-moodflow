from django.urls import path
from dashboard import views

'''
Proposed endpoints
GET /api/summary
GET /api/categories
GET /api/category/<category_name>/trending
GET /api/category/<category_name>/distribution
GET /api/apps/trending
GET /api/app/<app_id>
'''

urlpatterns = [
    path('v1/summary', views.Summary.as_view())
]