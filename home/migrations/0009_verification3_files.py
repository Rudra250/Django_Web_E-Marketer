# Generated by Django 4.2.1 on 2023-06-22 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_remove_verification3_senderpassword'),
    ]

    operations = [
        migrations.AddField(
            model_name='verification3',
            name='files',
            field=models.FileField(default='N/A', upload_to='files/'),
        ),
    ]