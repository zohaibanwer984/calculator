from django.db import models

class Histroy(models.Model):
    value_1 = models.FloatField()
    value_2 = models.FloatField()
    value_3 = models.FloatField()
    operator = models.CharField(max_length=1, default='+')
