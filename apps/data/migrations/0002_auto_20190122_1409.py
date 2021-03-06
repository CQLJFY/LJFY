# Generated by Django 2.1.5 on 2019-01-22 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Points2018',
            fields=[
                ('wkbgeometry', models.TextField(verbose_name='坐标')),
                ('code', models.CharField(blank=True, max_length=15, null=True, verbose_name='编码')),
                ('observe_time', models.DateTimeField(blank=True, null=True, verbose_name='测量时间')),
                ('geometry_id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': '点位数据',
                'verbose_name_plural': '点位数据',
                'db_table': 'points_2018',
                'managed': False,
            },
        ),
        migrations.AlterModelOptions(
            name='checkinformation',
            options={'managed': False, 'verbose_name': '检查内容', 'verbose_name_plural': '检查内容'},
        ),
    ]
