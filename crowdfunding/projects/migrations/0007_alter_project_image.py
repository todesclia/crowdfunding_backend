# Generated by Django 5.1 on 2024-12-02 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_alter_project_is_open'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='image',
            field=models.URLField(blank=True, null=True),
        ),
    ]
