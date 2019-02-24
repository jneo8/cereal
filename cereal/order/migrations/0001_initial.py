# Generated by Django 2.1.7 on 2019-02-24 07:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('customer', models.IntegerField()),
                ('shipping', models.IntegerField()),
                ('created_at', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=300)),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.Order')),
            ],
        ),
    ]