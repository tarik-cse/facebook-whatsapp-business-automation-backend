# Generated by Django 5.2.2 on 2025-06-10 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0006_remove_conversation_channel'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmessage',
            name='timestamp',
            field=models.CharField(default='1749531079', max_length=20),
        ),
    ]
