# Generated by Django 5.0.1 on 2024-01-20 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0002_alter_blog_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Newsletter_emails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
    ]
