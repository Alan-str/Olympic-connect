from django.db import models

def upload_to(instance, filename):
    # Personnalisez le nom de fichier ici si nécessaire
    return 'events/thumbnails/{filename}'.format(filename=filename)

class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    price_solo = models.DecimalField(max_digits=10, decimal_places=2)
    price_duo = models.DecimalField(max_digits=10, decimal_places=2)
    price_family = models.DecimalField(max_digits=10, decimal_places=2)
    thumbnail = models.ImageField(upload_to=upload_to)  # Utilisation de la fonction de renommage
    banner = models.ImageField(upload_to='events/banners/')

    def __str__(self):
        return self.name
