from django.db import models

class Client(models.Model):
    nick = models.CharField(max_length=50,null=False)
    address = models.CharField(max_length=15,null=False)
    port = models.IntegerField(max_length=5,null=False)
    status = models.CharField(max_length=50,null=False)
    server = models.CharField(max_length=50,null=False,db_column="cli_ser_id")

    class Meta:
        db_table = "clients"
        constraints = [
            # CONSTRAINT `ser_port_CK` CHECK (`port` between 0 and 65535)
            models.CheckConstraint(
                check=models.Q(port__gte=0) & models.Q(port__lte=65535),
                name="cli_port_CK"
            ),

            # CONSTRAINT `ser_address_REGEXP` CHECK (`address` regexp '^[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}$')
            models.CheckConstraint(
                check=models.Q(
                    address__iregex=r'^[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}$'
                ),
                name="cli_address_REGEXP"
            ),
        ]