# Generated by Django 4.1.1 on 2022-09-11 10:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('business', '0002_alter_business_options_alter_business_table_and_more'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(db_index=True, max_length=255, unique=True, verbose_name='email')),
                ('first_name', models.CharField(default='', max_length=255, verbose_name='first name')),
                ('last_name', models.CharField(default='', max_length=255, verbose_name='last name')),
                ('role', models.CharField(choices=[('global_admin', 'Global Admin'), ('global_manager', 'Global Manager'), ('business_admin', 'Business Admin'), ('business_manager', 'Business Manager')], max_length=20, verbose_name='role')),
                ('role_permissions', models.CharField(choices=[('global_admin', 'Global Admin'), ('global_manager', 'Global Manager'), ('business_admin', 'Business Admin'), ('business_manager', 'Business Manager')], max_length=20, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('business', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='business.business', verbose_name='Business')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
        ),
    ]