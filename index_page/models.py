# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Comments(models.Model):
    reviewer_name = models.CharField(primary_key=True, max_length=255)  # The composite primary key (reviewer_name, review_time) found, that is not supported. The first column is selected.
    review_time = models.CharField(max_length=255)
    song_name = models.CharField(max_length=255)
    review_prov = models.CharField(max_length=255)
    zan = models.CharField(max_length=255, blank=True, null=True)
    review = models.CharField(max_length=301)

    class Meta:
        managed = False
        db_table = 'comments'
        unique_together = (('reviewer_name', 'review_time'),)


class Songs(models.Model):
    list_name = models.CharField(primary_key=True, max_length=255)  # The composite primary key (list_name, rank) found, that is not supported. The first column is selected.
    rank = models.IntegerField()
    song_name = models.CharField(max_length=255, blank=True, null=True)
    rank_ration = models.CharField(max_length=255)
    singer = models.CharField(max_length=255)
    song_time = models.CharField(max_length=255)
    img_url = models.CharField(max_length=255)
    info_list = models.CharField(max_length=255)
    song_url = models.CharField(max_length=255)
    comment_num = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'songs'
