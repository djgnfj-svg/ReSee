# Generated by Django 4.0 on 2022-01-01 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Reviewer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studylist',
            name='review_count',
            field=models.IntegerField(default=0),
        ),
    ]