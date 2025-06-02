from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from scraper.db import get_database

# Create your views here.
class Summary(APIView):
    def get(self, request):
        '''
        TODO
        Número total de apps monitoreadas
        Categorías activas
        Categorías con más apps en tendencia (🔥)
        Apps con mayor trend_score global
        Top 5 categorías por media de trend_score
        '''

        db = get_database()
        categories = db.list_collection_names()



        data = {
            "name" : "testing_without_serializer",
            "categories": categories,
        }
        return Response(data, status=status.HTTP_200_OK)