from django.db import models

class App(models.Model):
    app_id = models.CharField(primary_key=True, max_length=100)  # com.package.name
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=100)

class AppSnapshot(models.Model):
    app = models.ForeignKey(App, on_delete=models.CASCADE, related_name='snapshots')
    top_type = models.CharField(max_length=50)  # top_free, top_paid, etc.
    current_rank = models.IntegerField()
    previous_rank = models.IntegerField()
    trend_score = models.FloatField()
    snapshot_time = models.DateTimeField(auto_now_add=True)
    score = models.FloatField()
    ratings = models.IntegerField()

class SentimentSummary(models.Model):
    app = models.OneToOneField(App, on_delete=models.CASCADE)
    positive_pct = models.FloatField()
    neutral_pct = models.FloatField()
    negative_pct = models.FloatField()
    keywords = models.JSONField()  # {"camera": 40, "ads": 15, ...}
    updated_at = models.DateTimeField(auto_now=True)

