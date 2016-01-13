from django.db import models


class Client(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def natural_key(self):
        return self.first_name, self.last_name


class Reservation(models.Model):
    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, related_name='reservations')
    number = models.IntegerField()
    comment = models.TextField()

    # def natural_key(self):
    #     return (self.id, self.client, self.number, self.comment) + self.client.natural_key()


