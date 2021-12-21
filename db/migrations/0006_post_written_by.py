# Generated by Django 4.0 on 2021-12-21 12:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('db', '0005_post_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='written_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='posts', to='auth.user'),
        ),
    ]
