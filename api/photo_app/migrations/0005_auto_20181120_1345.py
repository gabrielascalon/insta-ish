# Generated by Django 2.1.2 on 2018-11-20 13:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photo_app', '0004_auto_20181120_1328'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Comments',
            new_name='Comment',
        ),
        migrations.RenameModel(
            old_name='Followers',
            new_name='Follower',
        ),
        migrations.RenameModel(
            old_name='Likes',
            new_name='Like',
        ),
    ]