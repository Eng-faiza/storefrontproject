from django.conf import settings
from django.db import models
# from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
# from store.models import Product


class LikedItem(models.Model):
    # user=models.ForeignKey(User, on_delete=models.CASCADE)
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content_type=models.ForeignKey(ContentType,on_delete=models.CASCADE)
    object_id=models.PositiveIntegerField()
    Content_object=GenericForeignKey()

class TaggedItemManager(models.Manager):
    def get_tags_for(self, obj_type, obj_id):
       content_type= ContentType.objects.get_for_model(obj_type)
       return TaggedItem.objects \
           .select_related('tag') \
           .filter(
               content_type=content_type, 
               object_id=obj_id)
       
class Tag(models.Model):
    label=models.CharField(max_length=255)

    def __str__(self)->str:
        return self.label


class TaggedItem(models.Model):
    objects=TaggedItemManager()
    #what tag applied to what object
    tag=models.ForeignKey(Tag,on_delete=models.CASCADE)
    #type the object(product,vedio,article) >we can find the table 
    #id of object
    content_type=models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id=models.PositiveIntegerField()
    content_object=GenericForeignKey()



