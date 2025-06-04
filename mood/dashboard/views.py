from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timezone
from google_play_scraper import app
from scraper.db import get_database
from scraper.constants import TABS
from .models import App, AppSnapshot
from .serializers import AppSerializer, AppSnapshotSerializer

from .utils import get_most_active_categories, get_percentiles, get_top_apps

# Create your views here.
class Summary(APIView):
    def get(self, request):
        db = get_database()
        categories = db.list_collection_names()
        number_of_categories = len(categories)
        total_apps = 0
        apps_most_trend_scores = get_top_apps(db)

        data = get_percentiles(db)
        active_categories = get_most_active_categories(data)
        for category in categories:
            total_apps = len(db[category].distinct('app_id')) + total_apps
        
        data = {
            "total_apps_tracked": total_apps,
            "categories": categories,
            "categories_monitored" : number_of_categories,
            "active_categories" : active_categories,
            "apps_most_trend_scores" : apps_most_trend_scores,
        }
        return Response(data, status=status.HTTP_200_OK)
    
@api_view(['GET'])
def top_trending_apps(_):
    db = get_database()
    top_apps = get_top_apps(db, 10)
    for app in top_apps:
        # Saving data app if new in the ranking, also adding the snapshot over time
        app_defaults = {
            "title" : app["title"],
            "category" : app["category"],
        }

        obj, created_app = App.objects.get_or_create(app_id=app['app_id'], defaults=app_defaults)
        if created_app:
            obj.save()
        
        #Creating snapshot
        now = datetime.now(timezone.utc)
        AppSnapshot.objects.create(
            app=obj,
            top_type=app["top_type"],
            previous_rank=app["previous_rank"],
            current_rank=app["current_rank"],
            trend_score=app["trend_score"],
            score=app["score"],
            ratings=app["ratings"],
            snapshot_time=now
        )

    return Response({'top_apps': top_apps}, status=status.HTTP_200_OK)

@api_view(['GET'])
def app_details(_, app_id):
    metadata = app(app_id)
    app_obj = App.objects.filter(app_id=app_id).first()
    if not app_obj:
        return Response({"msg": "App not found"}, status=status.HTTP_204_NO_CONTENT)

    app_serializer = AppSerializer(app_obj)
    snapshots = AppSnapshot.objects.filter(app=app_obj).order_by('-snapshot_time')

    snapshots_serializer = AppSnapshotSerializer(snapshots, many=True)

    return Response(
        {
            'app': app_serializer.data,
            'snapshots': snapshots_serializer.data,
            'description' : metadata.get('description'),
            'icon_url': metadata.get('icon'),
        }, status=status.HTTP_200_OK)

@api_view(['GET'])
def category_details(_, category):
    db = get_database()
    collection = db[category]
    
    if collection is None:
        Response({"msg": "Category not found"}, status=status.HTTP_204_NO_CONTENT)

    # For top apps
    pipeline = [
        {
            "$setWindowFields": {
                "partitionBy": "$top_type",
                "sortBy" : {"trend_score": -1},
                "output": {
                    "rank": {"$documentNumber": {}}
                }
            }
        },
        {"$match": {"rank": {"$lte": 10}}}
    ]

    top_apps = list(collection.aggregate(pipeline))
    for app in top_apps:
        del app['_id']

    # for trend_scores
    pipeline = [
        {"$match": {
            "category": category,
            "trend_score": {"$gt": 0}
        }},
        {"$group": {
            "_id": "$top_type",
            "scores": {"$push": "$trend_score"}
        }}
    ]

    results = collection.aggregate(pipeline)

    trend_scores_by_type = {doc['_id']: doc['scores'] for doc in results}
    return Response({"top": top_apps, "scores" : trend_scores_by_type}, status=status.HTTP_200_OK)
