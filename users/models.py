from django.db import models

from dr_martens.time_stamp_model import TimeStampModel

class User(TimeStampModel):
    username          = models.CharField(max_length=50)
    user_id           = models.CharField(max_length=50, unique=True)
    password          = models.CharField(max_length=256)
    mobile_number     = models.CharField(max_length=30)
    email             = models.CharField(max_length=50)
    point             = models.IntegerField()
    birthday          = models.DateTimeField()
    gender            = models.IntegerField()
    profile_image_url = models.CharField(max_length=1000, null=True)
    class Meta:
        db_table = "users"
