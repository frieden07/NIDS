"""
Module Name: System.

This module defines the database model for NIDS   system.

"""

from django.db import models
from django.contrib.auth.models import User


class Charts(models.Model):
    chartId = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    year = models.CharField(max_length=20)
    month = models.CharField(max_length=20)
    scannedCount = models.IntegerField(default=0)
    detectedCount = models.IntegerField(default=0)


class Intrusions(models.Model):
    intrusionId = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    packetDetails = models.JSONField(default=dict)
    intrusionType = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    severity = models.CharField(max_length=10)
    description = models.TextField(blank=True)
    notificationDetail = models.JSONField(default=dict)


class Alerts(models.Model):
    alertId = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    intrusion = models.ForeignKey(Intrusions, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    severity = models.CharField(max_length=20)
