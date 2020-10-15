# Generated by Django 3.0.8 on 2020-10-15 13:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('j_title', models.CharField(max_length=100)),
                ('j_location', models.CharField(max_length=100)),
                ('j_experience', models.IntegerField()),
                ('j_type', models.CharField(choices=[('1', 'Full time'), ('2', 'Part time'), ('3', 'Internship')], max_length=10)),
                ('j_sort_description', models.TextField()),
                ('j_salary', models.CharField(max_length=100)),
                ('j_c_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.User_Employeer')),
            ],
        ),
        migrations.CreateModel(
            name='JobQualification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jq_qualification', models.TextField()),
                ('j_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobportal.Job')),
            ],
        ),
        migrations.CreateModel(
            name='JobApplication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('e_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.User_Employee')),
                ('j_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobportal.Job')),
            ],
        ),
    ]
