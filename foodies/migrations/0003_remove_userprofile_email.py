# Generated by Django 2.1.5 on 2020-03-21 13:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodies', '0002_userprofile_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='email',
        ),
    ]
