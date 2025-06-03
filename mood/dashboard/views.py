from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from scraper.db import get_database
from .utils import get_most_active_categories, get_percentiles, get_top_five_apps

# Create your views here.
class Summary(APIView):
    def get(self, request):
        '''
        TODO
        Top 5 categorías por media de trend_score
        '''

        db = get_database()
        categories = db.list_collection_names()
        number_of_categories = len(categories)
        total_apps = 0
        apps_most_trend_scores = get_top_five_apps(db)

        data = get_percentiles(db)
        active_categories = get_most_active_categories(data)
        for category in categories:
            total_apps = len(db[category].distinct('app_id')) + total_apps

        data = {
            "total_apps_tracked": total_apps,
            "categories": categories,
            "categories_monitored" : number_of_categories,
            "active_categories" : active_categories,
            "apps_most_trend_scores" : apps_most_trend_scores
        }
        return Response(data, status=status.HTTP_200_OK)