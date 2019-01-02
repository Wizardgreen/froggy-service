# Generated by Django 2.1.4 on 2019-01-02 03:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Case',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('case_id', models.CharField(max_length=6, verbose_name='Id')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('content', models.TextField(verbose_name='Content')),
                ('location', models.CharField(max_length=255, verbose_name='Location')),
                ('username', models.CharField(max_length=50, verbose_name='Username')),
                ('mobile', models.CharField(max_length=10, verbose_name='Mobile')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('open_date', models.DateField(auto_now=True, verbose_name='Open Date')),
                ('close_date', models.DateField(auto_now=True, null=True, verbose_name='Close Date')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated')),
            ],
            options={
                'verbose_name': 'Case',
                'verbose_name_plural': 'Case',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='CaseHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('case_id', models.CharField(max_length=6, verbose_name='Id')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('content', models.TextField(verbose_name='Content')),
                ('location', models.CharField(max_length=255, verbose_name='Location')),
                ('username', models.CharField(max_length=50, verbose_name='Username')),
                ('mobile', models.CharField(max_length=10, verbose_name='Mobile')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('open_date', models.DateField(auto_now=True, verbose_name='Open Date')),
                ('close_date', models.DateField(auto_now=True, null=True, verbose_name='Close Date')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated')),
            ],
            options={
                'verbose_name': 'Case History',
                'verbose_name_plural': 'Case History',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated')),
            ],
            options={
                'verbose_name': 'User Region',
                'verbose_name_plural': 'User Region',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated')),
            ],
            options={
                'verbose_name': 'Case Status',
                'verbose_name_plural': 'Case Status',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated')),
            ],
            options={
                'verbose_name': 'Case Type',
                'verbose_name_plural': 'Case Type',
                'ordering': ('id',),
            },
        ),
        migrations.AddField(
            model_name='casehistory',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cases.Region', verbose_name='User Region'),
        ),
        migrations.AddField(
            model_name='casehistory',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cases.Status', verbose_name='Case Status'),
        ),
        migrations.AddField(
            model_name='casehistory',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cases.Type', verbose_name='Case Type'),
        ),
        migrations.AddField(
            model_name='case',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cases.Region', verbose_name='User Region'),
        ),
        migrations.AddField(
            model_name='case',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cases.Status', verbose_name='Case Status'),
        ),
        migrations.AddField(
            model_name='case',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cases.Type', verbose_name='Case Type'),
        ),
    ]
