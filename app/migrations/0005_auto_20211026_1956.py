# Generated by Django 3.2 on 2021-10-26 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_orderplaced_total_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=20)),
                ('lname', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=20)),
                ('phone', models.IntegerField()),
                ('message', models.CharField(max_length=200)),
            ],
        ),
        migrations.AlterField(
            model_name='orderplaced',
            name='status',
            field=models.CharField(choices=[('accepted', 'accepted'), ('packed', 'packed'), ('on_the_way ', 'on_the_way'), ('delevered', 'delevered'), ('cancel', 'cancel')], default='pending', max_length=50),
        ),
    ]
