from django.db import models

# Create your models here.
class Customer(models.Model):

    name = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    equipment = models.CharField(max_length=50)
    issue = models.TextField()
    date_of_booking = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name