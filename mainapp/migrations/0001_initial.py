# Generated by Django 2.2 on 2021-08-07 06:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('username', models.CharField(blank=True, max_length=254, null=True, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('name', models.CharField(blank=True, max_length=254, null=True)),
                ('user_type', models.CharField(blank=True, choices=[('client', 'Client'), ('employee', 'Employee')], max_length=100, null=True, verbose_name='User Type')),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('width', models.PositiveIntegerField()),
                ('height', models.PositiveIntegerField()),
                ('length', models.PositiveIntegerField()),
                ('size', models.CharField(choices=[('-----', '-----'), ('Small', 'Small'), ('Medium', 'Medium'), ('Large', 'Large'), ('X-large', 'X-large'), ('2X-large', '2X-large'), ('3X=large', '3X-large')], default='-----', max_length=100)),
                ('occupied', models.BooleanField(default=False, null=True)),
                ('daily_charge', models.PositiveIntegerField()),
                ('weekly_charge', models.PositiveIntegerField()),
                ('monthly_charge', models.PositiveIntegerField()),
                ('access_code', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pic', models.ImageField(default='profiles/default.jpg', upload_to='profiles/')),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True)),
                ('address', models.CharField(blank=True, max_length=20, null=True)),
                ('nok_fullname', models.CharField(blank=True, max_length=100, null=True)),
                ('nok_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('nok_number', models.CharField(blank=True, max_length=100, null=True)),
                ('nok_relationship', models.CharField(blank=True, max_length=100, null=True)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=200)),
                ('start_date', models.DateTimeField(auto_now=True)),
                ('end_date', models.DateTimeField(null=True)),
                ('address', models.CharField(max_length=200)),
                ('pickup', models.BooleanField(default=False)),
                ('payment_mode', models.CharField(max_length=200)),
                ('account_number', models.CharField(max_length=30)),
                ('total_cost', models.PositiveIntegerField(null=True)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='mainapp.Profile')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='unit', to='mainapp.Unit')),
            ],
        ),
    ]
