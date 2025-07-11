# Generated by Django 5.2.2 on 2025-06-25 09:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0003_alter_aiconfiguration_ai_model'),
    ]

    operations = [
        migrations.CreateModel(
            name='AIModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(help_text="Identifier used in APIs, e.g., 'gemini-2.0-flash'", max_length=100, unique=True)),
                ('name', models.CharField(help_text="Human-readable name, e.g., 'Gemini 2.0 Flash'", max_length=100)),
                ('is_custom', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AlterField(
            model_name='aiconfiguration',
            name='ai_model',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='configurations', to='chatbot.aimodel'),
        ),
    ]
