from django.db import models
class Status(models.Model):
    name = models.CharField(max_length=50,null=False,primary_key=True)

    class Meta:
        db_table = "status"