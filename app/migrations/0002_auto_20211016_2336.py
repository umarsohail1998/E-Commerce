# Generated by Django 3.2 on 2021-10-16 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='User',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='customer',
            old_name='User',
            new_name='user',
        ),
        migrations.AlterField(
            model_name='customer',
            name='state',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='orderplaced',
            name='status',
            field=models.CharField(choices=[('accepted', 'accepted'), ('packed', 'packed'), ('on the way ', 'on the way'), ('delevered', 'delevered'), ('cancel', 'cancel')], default='accepted', max_length=50),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('C', 'cookware'), ('E', 'electronics'), ('D', 'dinning'), ('k', 'kitchentools')], max_length=4),
        ),
    ]