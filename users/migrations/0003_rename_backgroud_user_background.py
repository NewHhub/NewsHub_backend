# Generated by Django 4.1.5 on 2023-04-02 15:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_avatar_user_backgroud'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='backgroud',
            new_name='background',
        ),
    ]
