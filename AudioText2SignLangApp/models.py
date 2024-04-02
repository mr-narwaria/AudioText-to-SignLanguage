from django.db import models

# Create your models here.


# my modeles
class Contact(models.Model):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=12)
    email = models.EmailField(max_length=50)
    desc = models.TextField(max_length=254)
    date = models.DateField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return self.name
