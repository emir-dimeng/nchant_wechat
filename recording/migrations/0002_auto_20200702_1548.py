# Generated by Django 3.0.7 on 2020-07-02 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recording', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='voice',
            name='voice_name',
            field=models.CharField(default='none', max_length=100),
        ),
        migrations.AlterField(
            model_name='voice',
            name='voice_record',
            field=models.FileField(upload_to='C:\\Users\\Aubrey\\Desktop\\semester3\\code\\project-NChant\\nchant\\media'),
        ),
    ]