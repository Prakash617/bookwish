from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator 

# Create your models here.
class BookReadingPointTable(models.Model):
    date = models.DateField()
    user = models.ForeignKey("user_accounts.CustomUser", on_delete=models.CASCADE, related_name="book_reader", null=True)
    level = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])

class PhysicalPointTable(models.Model):
    date = models.DateField()
    user = models.ForeignKey("user_accounts.CustomUser", on_delete=models.CASCADE, related_name="workout", null=True)
    level = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])

class MeditationPointTable(models.Model):
    date = models.DateField()
    user = models.ForeignKey("user_accounts.CustomUser", on_delete=models.CASCADE, related_name="meditation", null=True)
    level = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])

class RelationshipPointTable(models.Model):
    date = models.DateField()
    user = models.ForeignKey("user_accounts.CustomUser", on_delete=models.CASCADE, related_name="relation", null=True)
    level = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])





# Weekly Tables
class WeeklyBookReadingPointTable(models.Model):
    date = models.DateField()
    user = models.ForeignKey("user_accounts.CustomUser", on_delete=models.CASCADE, related_name="weekly_book_reader", null=True)
    level = models.IntegerField()

class WeeklyMeditationPointTable(models.Model):
    date = models.DateField()
    user = models.ForeignKey("user_accounts.CustomUser", on_delete=models.CASCADE, related_name="weekly_meditation", null=True)
    level = models.IntegerField()

class WeeklyPhysicalPointTable(models.Model):
    date = models.DateField()
    user = models.ForeignKey("user_accounts.CustomUser", on_delete=models.CASCADE, related_name="weekly_workout", null=True)
    level = models.IntegerField()

class WeeklyRelationshipPointTable(models.Model):
    date = models.DateField()
    user = models.ForeignKey("user_accounts.CustomUser", on_delete=models.CASCADE, related_name="weekly_relation", null=True)
    level = models.IntegerField()

