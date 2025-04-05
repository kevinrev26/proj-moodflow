from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SearchSerializer
from .scraper.playstore_scraper import scrape_play_store_search

class SearchAPIView(APIView):
    def get(self, request):
        serializer = SearchSerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        term = serializer.validated_data['term']

        result = scrape_play_store_search(term)

        return Response({'results': result})