from django.db import models
class Server(models.Model):
    password = models.CharField(max_length=500,null=False)
    ipaddress = models.CharField(max_length=15,null=False)
    port = models.IntegerField(max_length=3,null=False)
    clients = models.IntegerField(max_length=5,null=False)

    class Meta:
        db_table = "server"