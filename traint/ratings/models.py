from django.db import models
import numpy as np # for faster avg rating calculations 
# for dress images
from django.conf import settings
from django.core.files.storage import FileSystemStorage # for dress images
from django.db.models import Avg
from django.contrib.auth.models import User
import os 

def image_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/images/dresses/<filename>
    return u'dresses/{0}'.format(filename)

image_storage = FileSystemStorage(
    # Physical file location ROOT
    location=u'{0}/images/'.format(settings.MEDIA_ROOT),
    # Url for file
    base_url=u'{0}images/'.format(settings.MEDIA_URL),
)

# Create your models here.
class Dress(models.Model):
    name = models.CharField(max_length = 30, blank=True, null=True, default='')
    image = models.ImageField(upload_to=image_directory_path, storage=image_storage) # will specify where the image is
    price = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True) # date dress was  added 

    def avg_rating(self):
        all_ratings = map(lambda x: x.rating, self.rating_set.all())
        avg = np.mean(list(all_ratings))
        #print(avg)
        return avg
        

    def __unicode__(self):
        return self.name

class Rating(models.Model):
    CHOICES = [(1, 'Bad'), (2, 'Dislike'), (3, 'OK'), (4, 'Like'), (5, 'Love')] # having numbers helps with clustering - would eventually 
     # want to replace with stars 
    dress = models.ForeignKey(Dress, models.CASCADE)
    rating = models.PositiveIntegerField(choices=CHOICES)
    user_name = models.CharField(max_length=100) # needed for the preferences algorithm


# Credits: https://www.codementor.io/jadianes/build-data-products-django-machine-learning-clustering-user-preferences-du107s5mk
class Cluster(models.Model):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(User)

    def get_members(self):
        return "\n".join([u.username for u in self.users.all()])